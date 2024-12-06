from setuptools import setup, find_packages

setup(
    name='euclidean_species',
    version='1.0.1',
    packages=find_packages(),
    install_requires=[
        'pandas'
    ],
    entry_points={
        'console_scripts': [
            'euclidean_species=euclidean_species:hello',
        ],
    },
    python_requires='>=3.6',
)
