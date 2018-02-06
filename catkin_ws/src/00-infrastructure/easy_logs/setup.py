## ! DO NOT MANUALLY INVOKE THIS setup.py, USE CATKIN INSTEAD
from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

setup_args = generate_distutils_setup(
    packages=['easy_logs', 'easy_logs_tests', 'duckieswarm'],
    package_dir={'': 'include'},
    install_requires=['procgraph']
)

setup(**setup_args)
