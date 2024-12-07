from setuptools import setup, find_packages

setup(
    name='aws-devops-cli',
    version='0.0.3',
    packages=find_packages(),
    install_requires=[
        'typer', 'boto3', 'inquirer'
    ],
    entry_points={
        'console_scripts': [
            'aws-devops-cli=src.entrypoint:main',
        ],
    },
)