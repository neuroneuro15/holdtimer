import sys
from setuptools import setup
if 'win' in sys.platform.lower():
    try:
        import py2exe
    except ImportError:
        pass

setup(
    name='holdtimer',
    version='0.1',
    packages=['holdtimer'],
    url='https://www.github.com/neuroneuro15/holdtimer',
    license='MIT',
    author='Nicholas A. Del Grosso',
    author_email='delgrosso.nick@gmail.com',
    description='A Pyglet Stopwatch for held keyboard keys.',
    install_requires=['Click', 'pyglet'],
    entry_points="""
        [console_scripts]
        holdtimer=holdtimer.timer:run
    """,
    windows=[{'script':"timer.py"}],
    options={'py2exe':{'includes': ['sip']}}
)

