from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as file:
     LONG_DESCRIPTION = file.read()

with open('requirements.txt') as pkg:
    required = pkg.read().splitlines()

setup(
    name='quicksystem',
    version="0.1.0",
    description="CLI tool to reserve, provision a system and use Jenkins job for Satellite.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author="Vijay Singh",
    author_email="vijay8451@gmail.com",
    python_requires=">=3.12",
    url="https://github.com/vijay8451/quicksystem",
    py_modules=['quicksystem'],
    install_requires=required,
    packages=find_packages("quicksystem"),
    entry_points={"console_scripts": ["quicksystem=quicksystem:cli"]},
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.12',
    ],
)
