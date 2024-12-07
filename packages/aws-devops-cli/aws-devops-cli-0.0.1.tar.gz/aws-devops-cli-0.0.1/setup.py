from setuptools import setup

setup(
    name='aws-devops-cli',
    version='0.0.1',
    py_modules=['typer', 'boto3', "inquirer"],
    install_requires=[
        'typer', 'boto3', 'inquirer'
    ],
    entry_points={
        'console_scripts': [
            'aws-devops-cli=main:app',
        ],
    },
)