from setuptools import setup, find_packages

setup(
  name = 'test-an-torch',
  packages = find_packages(exclude=[]),
  version = '0.0.1',
  license='MIT',
  description = 'TEST - torch',
  author = 'Flavio Schneider',
  url = 'https://github.com/archinetai/test',
  keywords = [
    'artificial intelligence',
    'deep learning',
  ],
  install_requires=[
    'torch>=1.6'
  ],
  classifiers=[],
)