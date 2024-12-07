from setuptools import setup, find_packages

setup(
    name="pydialogs",
    version="1.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'pydialogs=pydialogs.dialogs:alert',
        ],
    },
    description="Python library for terminal-based dialogs",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="jarvisdevlin",
    author_email="jarvisdevil@example.com",
    url="https://github.com/jarvisdevlin/pydialogs",
)