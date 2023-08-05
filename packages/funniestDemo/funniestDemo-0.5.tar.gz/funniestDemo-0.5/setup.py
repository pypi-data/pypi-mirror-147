from setuptools import setup

setup(name='funniestDemo',
    version='0.5',
    description='The funniest joke in the world',
    url='http://github.com/storborg/funniest',
    author='Jun Chen',
    author_email='junc76@gmail.com',
    license='MIT',
    packages=['funniestDemo'],
    entry_points={
        'console_scripts': [
            'funniest-joke=funniestDemo.command_line:main'
        ],
    },
    zip_safe=False)