from setuptools import setup, find_packages

#? To save and upload build:
    #* 1. delete build/ and dist/ folders
    #* 2. run python setup.py bdist_wheel sdist
        # this will create build/ and dist/ folders
    #* 3. run twine check dist/*
        # this will check if the package is ready to be uploaded
    #* 4. run twine upload dist/*
        # this will upload the package to PyPi

with open('app/Readme.md', 'r') as f:
    l_desc = f.read()

    setup(
        name='bojan',
        version='0.0.8',
        description='A simple logging library',
        author='Daniil Grydin',
        package_dir={'': 'app'},
        packages=find_packages(where='app'),
        long_description=l_desc,
        long_description_content_type='text/markdown',
        url="https://github.com/daniilgrydin/bojan.git",
        author_email="",
        license="MIT",
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        install_requires=[],
        extras_require={
            "dev": [
                "pytest>=7.0",
                "twine>=4.0.2",
            ],
        },
        python_requires='>=3.6'
    )