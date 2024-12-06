'''Setup script.'''

import os
import setuptools


with open(f'{os.path.dirname(os.path.abspath(__file__))}/requirements.txt') as requirements:
    with open(f'{os.path.dirname(os.path.abspath(__file__))}/README.md') as readme:
        setuptools.setup(
            name='testbox',
            version='1.0.4',
            description='Test/TAS framework for DOSBox',
            long_description=readme.read(),
            long_description_content_type='text/markdown',
            author='Vladimir Chebotarev',
            author_email='vladimir.chebotarev@gmail.com',
            license='MIT',
            classifiers=[
                'Development Status :: 5 - Production/Stable',
                'Intended Audience :: Developers',
                'License :: OSI Approved :: MIT License',
                'Operating System :: OS Independent',
                'Programming Language :: Python :: 3 :: Only',
            ],
            keywords=['dosbox', 'test', 'tas'],
            project_urls={
                'Documentation': 'https://github.com/excitoon/testbox/blob/master/README.md',
                'Source': 'https://github.com/excitoon/testbox',
                'Tracker': 'https://github.com/excitoon/testbox/issues',
            },
            url='https://github.com/excitoon/testbox',
            packages=['testbox'],
            scripts=[],
            install_requires=requirements.read().splitlines(),
        )
