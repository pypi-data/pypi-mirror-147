from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  'Intended Audience :: Education',
  'Operating System :: OS Independent',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

REQUIREMENTS = open('requirements.txt', encoding='utf-8').read().splitlines()

with open('README.txt') as f:
    readme = f.read()

setup(
  name='mager',
  version='0.0.261',
  description='Assistant for tricky tasks',
  long_description=readme,
  url='https://github.com/Frank17/Mager',
  author='Frank Zhang',
  author_email='frankzhang314159@gmail.com',
  license='MIT',
  classifiers=classifiers,
  keywords=['assistant', 'helper'],
  packages=find_packages(),
  install_requires=REQUIREMENTS
)
