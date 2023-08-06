from pathlib import Path

from setuptools import setup, find_packages

BASE_DIR = Path(__file__).parent.resolve(strict=True)
VERSION = '0.0.1'
PACKAGE_NAME = 'aiovty'
PACKAGES = [p for p in find_packages() if not p.startswith('tests')]


def get_description():
    return (BASE_DIR / 'README.md').read_text()


if __name__ == '__main__':
    setup(
        version=VERSION,
        name=PACKAGE_NAME,
        description='A python asyncio implementation for VTY protocol',
        long_description=get_description(),
        long_description_content_type='text/markdown',
        packages=PACKAGES,
        author='Matan Perelman',
        classifiers=[
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
        ],
        url='https://github.com/matan1008/aiovty',
        project_urls={
            'aiovty': 'https://github.com/matan1008/aiovty'
        },
        tests_require=['pytest', 'pytest_asyncio'],
    )
