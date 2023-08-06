from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='ai4ipreds',
  version='0.0.1',
  description='basic linear preds',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Kshitiz khandelwal',
  author_email='kshitiz.khandelwal16@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='ai4i', 
  packages=find_packages(),
  install_requires=[''] 
)