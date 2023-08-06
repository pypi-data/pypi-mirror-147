from distutils.core import setup
setup(
  name = 'bahiart_gym',      
  packages = ['bahiart_gym'],   
  version = '1.0.1',     
  license='agpl-3.0',        
  description = 'A toolkit to develop openAI Gym environments on top of the RCSSSERVER3D simulator',   
  author = 'Gabriel Mascarenhas, Marco A. C. Simões, Rafael Fonseca',                  
  author_email = 'teambahiart@gmail.com',     
  url = 'https://bitbucket.org/bahiart3d/bahiart-gym/',   
  download_url = 'https://bitbucket.org/bahiart3d/bahiart-gym/downloads/BahiaRT_GYM_v1.0.0.zip',    
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
