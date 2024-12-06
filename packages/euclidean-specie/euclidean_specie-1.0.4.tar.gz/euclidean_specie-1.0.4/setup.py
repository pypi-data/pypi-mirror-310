from setuptools import setup, find_packages

setup(
    name='euclidean_specie',
    version='1.0.4',
    packages=find_packages(),
    install_requires=[
        'numpy','matplotlib'
    ],
    entry_points={
        'console_scripts': [
            'euclidean_specie=euclidean_specie:hello',
        ],
    },
    python_requires='>=3.6',
)
