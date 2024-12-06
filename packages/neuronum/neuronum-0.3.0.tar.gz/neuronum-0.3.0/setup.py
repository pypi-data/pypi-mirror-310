from setuptools import setup, find_packages

setup(
    name='neuronum',
    version='0.3.0',
    author='Neuronum Cybernetics',
    author_email='welcome@neuronum.net',
    description='A high-level coding library to interact with the Neuronum network.',
    packages=find_packages(),
    install_requires=[
        #'socket>=
        #'hashlib>=
    ],
    python_requires='>=3.6',
)
