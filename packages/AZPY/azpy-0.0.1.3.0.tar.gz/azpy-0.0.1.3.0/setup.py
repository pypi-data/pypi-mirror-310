from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='azpy',
  version='0.0.1.3.0',
  description='Nothing more',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Rostami',
  author_email='MHRo.R84@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='AZPY', 
  packages=find_packages(),
  install_requires=[''] 
)