from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='bimorph',
  version='1.0.20',
  author='@mpak2',
  author_email='mpak2@yandex.ru',
  description='Algorythm ML',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='http://xn--90aomiky.xn--p1ai/',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.10',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Operating System :: OS Independent'
  ],
  keywords='example python',
  project_urls={
    'Documentation': 'http://xn--90aomiky.xn--p1ai/'
  },
  python_requires='>=3.7'
)

