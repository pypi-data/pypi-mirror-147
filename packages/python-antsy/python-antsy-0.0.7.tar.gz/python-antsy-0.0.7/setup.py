from setuptools import setup, find_packages

setup(
    name='python-antsy',
    version='0.0.7',
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
    python_requires=">=3.6",
    install_requires=[
          'requests',
      ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
      ],

)
