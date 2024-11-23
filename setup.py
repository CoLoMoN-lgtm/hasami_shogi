from setuptools import setup, find_packages

setup(
    name="hasami_shogi",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'PyQt6',
    ],
    python_requires=">=3.8",
)