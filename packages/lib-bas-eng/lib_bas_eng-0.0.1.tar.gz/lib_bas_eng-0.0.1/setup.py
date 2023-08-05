import io
from os.path import abspath, dirname, join
from setuptools import find_packages, setup


HERE = dirname(abspath(__file__))
LOAD_TEXT = lambda name: io.open(join(HERE, name), encoding='UTF-8').read()
DESCRIPTION = '\n\n'.join(LOAD_TEXT(_) for _ in [
    'README.rst'
])

setup(
  name = 'lib_bas_eng',      
  packages = ['lib_bas_eng'], 
  version = '0.0.1', 
  license='MIT', 
  description = 'First Lib by BAS',
  long_description=DESCRIPTION,
  author = 'BASKETBALL',                 
  author_email = 'ballketball999@gmail.com',     
  url = 'https://github.com/basketball999/lib_bas_eng',  
  download_url = 'https://github.com/basketball999/lib_bas_eng/archive/v0.0.1.zip',  
  keywords = ['bas'],
  classifiers=[
    'Development Status :: 3 - Alpha',     
    'Intended Audience :: Education',     
    'Topic :: Utilities',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
  ],
)