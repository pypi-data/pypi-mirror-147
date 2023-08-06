from setuptools import setup, find_packages

classifiers = [
	'Development Status :: 5 - Production/Stable',
	'Intended Audience :: Education',
	'Operating System :: Microsoft :: Windows :: Windows 10',
	'License :: OSI Approved :: MIT License',
	'Programming Language :: Python :: 3'
]

setup(
  name='enginetool',
  version='0.0.1',
  description='A tool to run calculations about an engine',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Jonathon Gruener',
  author_email='jonathon14gruener@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='engine', 
  packages=find_packages(),
  install_requires=[
  'numpy',
  'matplotlib',
  'csv'
  ] 
)