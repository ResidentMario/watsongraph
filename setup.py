from distutils.core import setup
setup(
  name = 'watsongraph',
  packages = ['watsongraph'], # this must be the same as the name above
  install_requires=['networkx', 'requests', 'mwviews'],
  version = '0.2.0',
  description = 'Concept discovery and recommendation library built on top of the IBM Watson cognitive API.',
  author = 'Aleksey Bilogur',
  author_email = 'aleksey.bilogur@gmail.com',
  url = 'https://github.com/ResidentMario/watsongraph/tarball/0.2.0',
  download_url = 'https://github.com/ResidentMario/watsongraph/tarball/0.2.0',
  keywords = ['graph', 'networks', 'ibm watson', 'ibm', 'recommendation'], # arbitrary keywords
  classifiers = [],
)