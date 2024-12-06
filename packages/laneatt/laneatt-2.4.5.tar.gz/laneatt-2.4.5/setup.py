from setuptools import setup

setup(
  name = 'laneatt',
  packages = ['laneatt', 'laneatt.utils'],
  package_data={'laneatt': ['config/backbones.yaml']},
  include_package_data=True,
  version = '2.4.5',
  license='MIT',
  description = 'A package to detect lane lines in images and videos',
  long_description = """
  LaneATT is a Python library for detecting lanes from images or videos, utilizing a state-of-the-art deep neural network. It is designed to be efficient and accurate, making it suitable for real-world applications such as autonomous vehicles, robotics, and surveillance systems.

  Features:
      Lane Detection: Accurate lane detection using a cutting-edge deep learning model
      Image/Video Support: Supports both image and video input formats
      Configurable Model: Customize the model architecture through configuration files
      ModelCheckpointing: Automatically saves model checkpoints at regular intervals
      Inference Speed: Optimized for fast inference on GPUs, ideal for real-time applications

  Usage:
      LaneATT can be used in various scenarios, such as:
          Autonomous Vehicles: Lane detection is crucial for self-driving cars to navigate roads safely.
          Surveillance Systems: Lane detection can be used to improve the accuracy of traffic monitoring systems.
          Robotics: Lane detection can help robots navigate through environments with lanes.

  To install LaneATT, run:

  pip install laneatt

  For more information, please visit [github repo](https://github.com/PaoloReyes/RealTime-LaneATT).
  """,
  author = 'Paolo Reyes',
  author_email = 'paolo.alfonso.reyes@gmail.com',
  url = 'https://github.com/PaoloReyes/RealTime-LaneATT',
  download_url = 'https://github.com/PaoloReyes/RealTime-LaneATT/archive/refs/tags/LaneATT-v2.4.tar.gz',
  keywords = ['Lanes', 'AI', 'Greenhouse', 'Regression', 'Machine Learning', 'LaneATT', 'Delimitations'],
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