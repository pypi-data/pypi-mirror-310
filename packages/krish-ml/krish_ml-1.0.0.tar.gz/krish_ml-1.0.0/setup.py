from setuptools import setup, find_packages

setup(
    name='krish_ml',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'numpy','matplotlib'
    ],
    entry_points={
        'console_scripts': [
            'krish_ml=krish_ml:hello',
        ]
    },
    python_requires='>=3.6',
)
