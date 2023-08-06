from setuptools import setup, find_packages

setup(
    name='python-antsy',
    version='0.0.6',
    description="Python package for integrating Antsy in other applications",
    long_description=open("README.md").read().strip(),
    long_description_content_type="text/markdown",
    license='MIT',
    author="Juan F. Duque",
    author_email='jfelipe@grupodyd.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/grupodyd/python-antsy',
    keywords='antsy',
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*",
    install_requires=[
          'requests',
      ],

)
