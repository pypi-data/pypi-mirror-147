from io import open
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setup(name='free_proxies_useragents',
      version='1.0.0',
      author='ebankoff',
      author_email='herrnihilus@gmail.com',
      description='free proxies and useragents, created by ebankoff',
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=find_packages(),
      url='https://github.com/ebankoff/free-proxies-and-useragents',
      license='MIT',
      entry_points={
            'console_scripts': [
                'freeprx = free_proxies_useragents.freeprx:main',
            ],
      },
      python_requires='>=3.5'
      )