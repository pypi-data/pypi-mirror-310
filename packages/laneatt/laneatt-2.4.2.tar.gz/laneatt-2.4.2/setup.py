from setuptools import setup

setup(
  name = 'laneatt',
  packages = ['laneatt', 'laneatt.utils'],
  package_data={'laneatt': ['config/backbones.yaml']},
  include_package_data=True,
  version = '2.4.2',
  license='MIT',
  description = 'A package to detect lane lines in images and videos',
  author = 'Paolo Reyes',
  author_email = 'paolo.alfonso.reyes@gmail.com',
  url = 'https://github.com/PaoloReyes/RealTime-LaneATT',
  download_url = 'https://github.com/PaoloReyes/RealTime-LaneATT/archive/refs/tags/LaneATT-v2.4.tar.gz',
  keywords = ['lanes', 'AI', 'greenhouse', 'detection', 'machine learning', 'laneatt', 'delimitations'],
  install_requires=[
          'filelock',
          'fsspec',
          'Jinja2',
          'joblib',
          'MarkupSafe',
          'mpmath',
          'matplotlib',
          'networkx',
          'numpy',
          'opencv-python',
          'pillow',
          'PyYAML',
          'scikit-learn',
          'scipy',
          'setuptools',
          'sympy',
          'threadpoolctl',
          'torch',
          'torchaudio',
          'torchvision',
          'tqdm',
          'triton',
          'typing_extensions',
          'wheel',
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable', # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package

    'Intended Audience :: Developers', # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',

    'License :: OSI Approved :: MIT License', # License

    'Programming Language :: Python :: 3', # Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.12',
  ],
)