from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='rac_schema_validator',
      version='1.0',
      description='Validator for RAC JSON Schemas',
      url='http://github.com/RockefellerArchiveCenter/rac_schema_validator',
      author='Rockefeller Archive Center',
      author_email='archive@rockarch.org',
      long_description=long_description,
      long_description_content_type="text/markdown",
      install_requires=['jsonschema'],
      license='MIT',
      packages=['rac_schema_validator'],
      test_suite='nose.collector',
      tests_require=['pytest', 'jsonschema'],
      zip_safe=False,
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      python_requires='>=3.10',)
