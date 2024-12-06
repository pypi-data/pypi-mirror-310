from setuptools import setup, find_packages

setup(
    name= "venvkit",
    version="0.2.0",
    packages=find_packages(),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[],
    entry_points={
        "console_scripts": [
            "vk=venvkit.main:main",
        ]
    },
    classifiers=[
        'Intended Audience :: Developers',
    ],
)
