from setuptools import setup, find_packages


setup(
    name="django-utils-vish",
    version="0.1.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=3.2"
    ],
    description="A collection of useful utilities and management commands for Django.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Vishango",
    author_email="itsvishalhack@gamil.com",
    url="https://github.com/visha1codehub/django-utils-plus",
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
