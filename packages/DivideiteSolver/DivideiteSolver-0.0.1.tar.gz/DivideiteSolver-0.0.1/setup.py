from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='DivideiteSolver',
  version='0.0.1',
  description='Include function to solve expressions',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Vikas Saini',
  author_email='sainivk565@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='divideite', 
  packages=find_packages(),
  install_requires=[''] 
)