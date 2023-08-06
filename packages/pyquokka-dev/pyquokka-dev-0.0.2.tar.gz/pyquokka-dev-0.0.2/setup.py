from setuptools import setup, find_packages

VERSION = '0.0.2' 
DESCRIPTION = 'Quokka'
LONG_DESCRIPTION = 'Dope way to do cloud analytics'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="pyquokka-dev", 
        version=VERSION,
        author="Tony Wang",
        author_email="zihengw@stanford.edu",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['pyarrow==6.0.1',
            'redis==4.1.0',
            'boto3==1.17.24',
            'pandas==1.2.2',
            'numpy==1.19.2',
            'ray==1.9.1',
            'aiobotocore',
            'h5py',
            'polars==0.13.0'
            ], # add any additional packages that 
        license='http://www.apache.org/licenses/LICENSE-2.0',
        keywords=['python'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
