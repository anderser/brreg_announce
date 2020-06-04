from setuptools import setup

setup(name='brreg_announce',
      version='0.6',
      description='This app scrapes the annoncements section (kunngjoringer) of Bronnoysundregistrene and returns the data on a structured format.',
      url='http://github.com/anderser/brreg_announce',
      author='anderser',
      author_email='anderser@anderser.no',
      license='MIT',
      packages=['brreg_announce'],
      install_requires=[
          'lxml',
          'requests'
      ],
      test_suite='tests',
      tests_require=['unittest-xml', 'mock'],
      zip_safe=False)