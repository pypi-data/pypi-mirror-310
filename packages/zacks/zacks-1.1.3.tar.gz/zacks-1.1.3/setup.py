from setuptools import setup, find_packages

setup(
    name="zacks",  # Your new project name
    version="1.1.3",  # Update version if necessary
    packages=find_packages(),  # Automatically find all packages
    install_requires=[
        "requests",  # Add dependencies as needed
    ],
    entry_points={
        "console_scripts": [
            "zacks=zacks.__main__:main",  # Adjust this if you have a CLI entry point
        ],
    },
    # Include other metadata as required
)
