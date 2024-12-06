from setuptools import setup, find_packages

setup(
    name="cmd-gui-kit",  # Package name
    version="1.0.0",  # Initial release version
    description="A toolkit for creating enhanced CLI visualizations.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="cagatay-softgineer",
    author_email="cagatayalkan.b@gmail.com",
    url="https://github.com/cagatay-softgineer/cmd-gui-kit",  # Replace with your repo URL
    license="MIT",
    packages=find_packages(),  # Automatically find subpackages
    install_requires=[
        "termcolor>=1.1.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
