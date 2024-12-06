from distutils.core import setup
setup(
  name = 'pydg1000z',
  packages = ['pydg1000z'],
  version = '0.1.1',
  license='MIT',
  description = 'Rigol DG1000Z control library (unofficial)',
  author = 'P.M Schueler',
  author_email = 'peter.schueler@gmxpro.de',
  url = 'https://github.com/PMSchueler/pydg1000z',
  download_url = 'https://github.com/PMSchueler/pydg1000z/archive/refs/tags/0.1.1.tar.gz',   
  keywords = ['RIGOL', 'WAVEFORM GENERATOR', 'DG1000Z'],
  install_requires=[
          'pylabdevs-tspspi',
          'logging',
          'datetime',
          'enum'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Science/Research',
    'Topic :: Utilities',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
  ],
)
