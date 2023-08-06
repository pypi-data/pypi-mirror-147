from setuptools import setup, find_packages
#from distutils.core import setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
  name = 'bahiart_gym',     
  packages=find_packages(),  
  version = '1.0.3',      
  license='agpl-3.0',        
  description = 'A toolkit to develop openAI Gym environments on top of the RCSSSERVER3D simulator',
  long_description=long_description,
  long_description_content_type="text/markdown",   
  author = 'Gabriel Mascarenhas, Marco A. C. Simões, Rafael Fonseca',                  
  author_email = 'teambahiart@gmail.com',     
  url = 'https://bitbucket.org/bahiart3d/bahiart-gym/',   
  keywords = ['CUSTOM', 'ENVIRONMENT', 'GYM', 'OPTIMIZATION', 'MACHINE', 'LEARNING'],
  install_requires=[            
          'gym',
          'numpy',
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU Affero General Public License v3',   
    'Programming Language :: Python :: 3.7', 
    'Topic :: Scientific/Engineering :: Artificial Intelligence',     
  ],
)
