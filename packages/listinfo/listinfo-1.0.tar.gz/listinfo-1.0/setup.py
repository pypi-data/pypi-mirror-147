from setuptools import setup


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
  name = 'listinfo',         
  packages = ['listinfo'],  
  version = '1.0',     
  license='MIT',        
  description = '''A lightweight library to get details of list and it helps to split list into lists of small size also it 
  converts list into different sized chunk.''',
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = 'SusmitPanda',                   
  author_email = 'susmit.vssut@gmail.com',     
  keywords = ['lisinfo','list statistics','split list','list tochunks'],
  install_requires=[],
  classifiers=[
    'Development Status :: 3 - Alpha',     
    'Intended Audience :: Developers',     
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',     
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],)