from setuptools import setup, find_packages

setup(
    name="venvkit",
    version="0.2.1",
    description="A powerful toolkit for Python virtual environment management",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Umar Balak", 
    url="https://github.com/UmarBalak/venvkit",
    packages=find_packages(exclude=['tests*', 'docs*']),
    python_requires='>=3.8',
    install_requires=[],
    entry_points={
        "console_scripts": [
            "vk=venvkit.main:main",
        ]
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
        'Natural Language :: English',
    ],
    
    # Additional metadata
    keywords='venv,virtualenv,environment,python,development,tools,cli',
    project_urls={
        'Documentation': 'https://github.com/UmarBalak/venvkit/blob/main/README.md',
        'Source': 'https://github.com/UmarBalak/venvkit',
    },
    
    # Test suite
    test_suite='tests',

)