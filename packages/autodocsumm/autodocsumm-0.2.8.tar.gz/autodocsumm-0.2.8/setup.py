from setuptools import setup, find_packages
import sys

needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='autodocsumm',
      version='0.2.8',
      description='Extended sphinx autodoc including automatic autosummaries',
      long_description=readme(),
      long_description_content_type='text/x-rst',
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Documentation',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
      ],
      keywords='sphinx autodoc autosummary content table',
      python_requires=">=3.6",
      url='https://github.com/Chilipp/autodocsumm',
      author='Philipp S. Sommer',
      author_email='philipp.sommer@hereon.de',
      license="Apache-2.0",
      packages=find_packages(exclude=['docs', 'tests*', 'examples']),
      install_requires=[
          'Sphinx>=2.2,<5.0',
      ],
      setup_requires=pytest_runner,
      tests_require=['pytest'],
      zip_safe=False)
