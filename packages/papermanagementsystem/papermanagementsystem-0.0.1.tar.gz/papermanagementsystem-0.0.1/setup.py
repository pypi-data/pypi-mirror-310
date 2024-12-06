from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: OS Independent',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='papermanagementsystem',
  version='0.0.1',
  description='A very basic store management software',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',
  author='Akshat Kala',
  author_email='itzakshat706@gmail.ccom',
  license='MIT',
  classifiers=classifiers,
  keywords='store_management_software',
  packages=find_packages(),
  install_requires=['']
)
