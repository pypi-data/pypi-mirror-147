from distutils.core import setup
setup(
    name = 'pyarubaimc',
    packages = ['pyarubaimc'],
    version = '0.1.4',
    description = 'A python binding to work with the Aruba IMC API',
    author = 'Rick Kauffman',
    author_email = 'rick@rickkauffman.com',
    url = 'https://github.com/aruba/pyarubaimc',
    download_url = 'https://github.com/aruba/pyarubaimc/archive/refs/tags/v0.1.4.tar.gz',
    keywords = ['IMC', 'api', 'python'],
    install_requires=[
          'requests',
          'urllib3',
          'nose',
      ],
    classifiers = [],
)
