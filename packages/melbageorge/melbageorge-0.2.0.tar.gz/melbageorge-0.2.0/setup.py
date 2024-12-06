from setuptools import setup,find_packages
setup(
    name ="melbageorge",                           # package name
    version='0.2.0',                               # version
    description='A sample pyhton module',
    author='Melba George',
    author_email='melbageorge@gmail.com',
    packages=find_packages(),                      # Automatically find modules
    install_requires=[],
    python_requires='>=3.6'
)