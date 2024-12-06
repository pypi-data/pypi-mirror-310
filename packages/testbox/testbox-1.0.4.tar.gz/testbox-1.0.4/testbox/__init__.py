import contextlib
import multiprocessing
import os
import tempfile
import threading
import time

import PIL.Image
import PIL.ImageChops


assert multiprocessing.get_start_method() == 'fork'


class TestBox:
    def __init__(self, test_command, configuration=None, environment=None, dosbox_path='dosbox', timeout_error=TimeoutError):
        # TODO Try rewrite as contextmanager
        self.__captures_path = None
        self.__configuration = {section: items.copy() for section, items in configuration.items()} if configuration is not None else {}
        self.__configuration.setdefault('sdl', {})['usescancodes'] = 'false'
        self.__directory = None
        self.__dosbox_path = dosbox_path
        self.__environment = environment if environment is not None else os.environ.copy()
        self.__input_file = None
        self.__output_in = None
        self.__process = None
        self.__screenshot_ready = None
        self.__test_command = test_command
        self.__thread = None
        self.__timeout_error = timeout_error

    def send_keys(self, keys):
        for key in keys:
            code = ord(key.lower())
            modifiers = 0
            if key == '▴':
                code = 273
            elif key == '▾':
                code = 274
            elif key == '▸':
                code = 275
            elif key == '◂':
                code = 276
            elif key.isupper():
                modifiers |= 1
                self.__command('KEY DOWN 304 0')
            elif '\x01' <= key <= '\x1a' and key != '\r':
                modifiers |= 0x40
                code += ord('a') - 1
                self.__command('KEY DOWN 306 0')
            self.__command(f'KEY DOWN {code} {modifiers}')
            self.__command(f'KEY UP {code} {modifiers}')
            if modifiers & 1:
                self.__command('KEY UP 304 0')
            if modifiers & 0x40:
                self.__command('KEY UP 306 0')

    def get_screenshot(self, timeout=None):
        with self.__timeout(timeout) as timeout:
            print('SCREENSHOT', file=self.__input_file, flush=True)
            if not self.__screenshot_ready.wait(timeout=timeout()):
                raise self.__timeout_error()
            self.__screenshot_ready.clear()
            name, = (x for x in os.listdir(self.__captures_path) if os.path.splitext(x)[1] == '.png')
            path = os.path.join(self.__captures_path, name)
            result = PIL.Image.open(path)
            os.remove(path)
            return result

    def wait_image(self, image=None, bbox=None, invert=False, timeout=None):
        with self.__timeout(timeout) as timeout:
            if image is None:
                expected_image = self.get_screenshot(timeout=timeout())
            elif isinstance(image, str):
                expected_image = PIL.Image.open(image)
            else:
                expected_image = image

            expected = expected_image.crop(bbox) if bbox else expected_image
            while True:
                result = self.get_screenshot(timeout=timeout())
                actual = result.crop(bbox) if bbox else result
                diff = PIL.ImageChops.difference(actual, expected).getbbox()
                if (diff is None) != invert:
                    return result

    def wait_change(self, image=None, bbox=None, timeout=None):
        return self.wait_image(image, bbox=bbox, invert=True, timeout=timeout)

    def quit(self):
        self.__command('BYE')

    @property
    def pid(self):
        return self.__process.pid

    @contextlib.contextmanager
    def __timeout(self, timeout):
        now = time.monotonic()
        def get():
            nonlocal now
            nonlocal timeout
            if timeout is not None:
                passed = time.monotonic() - now
                now += passed
                timeout -= passed
                if timeout < 0:
                    raise self.__timeout_error()
            return timeout
        yield get
        get()

    def __output_thread(self):
        with os.fdopen(self.__output_in) as output_file:
            while data := output_file.readline():
                data = data.strip()
                if data == 'SCREENSHOT':
                    self.__screenshot_ready.set()

    def __command(self, command):
        print(command, file=self.__input_file, flush=True)

    def __enter__(self):
        self.__directory = tempfile.TemporaryDirectory()
        self.__directory.__enter__()

        self.__configuration.setdefault('dosbox', {})['captures'] = 'captures'
        configuration_path = os.path.join(self.__directory.name, 'dosbox.conf')
        with open(configuration_path, 'w') as f:
            for section, items in self.__configuration.items():
                print(f'[{section}]', file=f)
                for key, value in items.items():
                    print(f'{key} = {value}', file=f)
                print(file=f)

        self.__captures_path = os.path.join(self.__directory.name, self.__configuration['dosbox']['captures'])
        os.makedirs(self.__captures_path, exist_ok=True)

        self.__output_in, output_out = os.pipe()
        input_in, input_out = os.pipe()
        self.__process = multiprocessing.Process(target=lambda: (
            os.close(input_out),
            os.dup2(input_in, 0),
            os.close(input_in),
            os.close(self.__output_in),
            os.dup2(output_out, 1),
            os.close(output_out),
            os.execlpe('stdbuf', 'stdbuf', '-oL', self.__dosbox_path, '-conf', configuration_path, *self.__test_command, self.__environment),
        ))

        self.__process.start()
        os.close(input_in)
        os.close(output_out)

        self.__screenshot_ready = threading.Event()

        self.__thread = threading.Thread(target=self.__output_thread)
        self.__thread.start()

        self.__input_file = os.fdopen(input_out, 'w')

        time.sleep(1.5) # FIXME DOSBox fails to save screenshots when its loading
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__directory.__exit__(exc_type, exc_value, traceback)
        self.__input_file.close()
        self.__process.kill()
        self.__thread.join()
