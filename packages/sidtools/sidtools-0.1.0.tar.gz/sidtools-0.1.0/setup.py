from setuptools import setup, find_packages

setup(
    name="sidtools",
    version="0.1.0",
    packages=find_packages(),  # This will automatically find the 'sidtools' package
    install_requires=["ase"],
    entry_points={
        "console_scripts": [
            "s_make = sidtools.s_make:main",  # Make sure this points to the correct entry point
        ],
    },
)
