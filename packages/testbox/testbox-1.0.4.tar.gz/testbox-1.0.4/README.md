# TestBox

Test/TAS framework for DOSBox.

Run:

```
docker-compose -f docker-compose.example.yml run test
```

Or:

```
docker-compose -f docker-compose.example.console.yml run test
```

Tested on Ubuntu 20.10.

## Example

As test application I used "demo" version of Soko-Ban by Spectrum HoloByte. Please notice that test application is only included as an example. It is unplayable after level 2.

Test scenario includes full walkthrough of level 1.

```python
import testbox

with testbox.TestBox(['SOKOBAN.EXE'], {'cpu': {'cycles': 'max'}}) as box:
    box.wait_image('images/graphics.png', timeout=1)
    box.send_keys('C\r') # CGA mode.

    box.wait_image('images/input.png', timeout=1)
    box.send_keys('K\r') # Input from keyboard.

    box.wait_image('images/door.png', timeout=5)
    box.send_keys('\r') # Enter door.

    box.wait_image('images/lobby.png', timeout=1)
    box.send_keys('\r') # Enter elevator.

    box.wait_image('images/menu.png', timeout=5)
    box.send_keys('TEST\r') # Enter player name.

    box.wait_image('images/start.png', timeout=1)
    box.send_keys('\r') # Select single player mode.

    box.wait_image('images/elevator.png', timeout=1)
    box.send_keys('1A') # Select first floor and accept.

    for step, keys in (
        ('one', '▴◂◂◂▴▴▴◂▴◂◂▾◂◂▾▾▾▸▸▸▸▸▸▸▸▸▸▸▸▸▾▸▴◂◂'),
        ('two', '◂◂◂◂◂◂◂▴▴▴◂▴◂◂▾▾▾▴▴◂◂▾▾▾▸▸▸▸▸▸▸▸▸▸▸▸▴▸▾◂▾▸▴◂'),
        ('three', '◂◂◂◂◂◂◂▴▴▴◂◂▴◂▾▾▾▴▴◂◂▾▾▾▸▸▸▸▸▸▸▸▸▸▸▸▾▸▴◂'),
        ('four', '◂◂◂◂◂◂◂▴▴▴◂◂▴▴▴◂▾▾▾▾▾▴▴◂◂▾▾▾▸▸▸▸▸▸▸▸▸▸▸▴▸▾◂▾▸▴'),
        ('five', '◂◂◂◂◂◂◂▴▴▴◂◂▴▴▴▸▾▾◂◂▾◂◂▾▾◂◂▾▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸◂'),
        ('six', '◂◂◂◂◂◂◂▴▴▴◂◂▴◂▾▾▾▴▴◂◂▾▾▾▸▸▸▸▸▸▸▸▸▸▸▸'),
    ):
        # Checkpoint, skipping status bar.
        box.wait_image(f'images/step-{step}.png', bbox=(0, 0, 320, 191), timeout=3)

        for key in keys:
            box.send_keys(key)
            # Waiting move counter to update.
            box.wait_change(bbox=(75, 191, 110, 200), timeout=1)

    box.wait_image('images/victory.png', timeout=10) # Level 2.
```

![Test application](example/video.gif)
