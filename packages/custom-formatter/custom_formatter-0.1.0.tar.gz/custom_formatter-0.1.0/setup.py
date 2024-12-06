from setuptools import setup, find_packages

setup(
    name='custom_formatter',
    version='0.1.0',  # Version number
    packages=find_packages(),
    description='A lightweight package for formatting and serializing messages.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='mani',
    author_email='mani.dasari3027@gmail.com',
    url='https://github.com/manidasari27/formatter',  # Replace with your repo URL
    license='MIT',
    install_requires=[],  # No external dependencies
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
