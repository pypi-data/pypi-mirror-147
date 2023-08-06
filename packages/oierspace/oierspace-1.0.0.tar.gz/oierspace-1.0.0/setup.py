from setuptools import setup, find_packages

setup(
    name = 'oierspace',
    version = '1.0.0',
    packages = find_packages(),
    include_package_data = True,
    install_requires = [
        'requests', 'urllib3', 'retry'
    ],
    url = 'https://github.com/jin-dan/pyoierspace',
    license = 'MIT License',
    author = 'Qin Yuzhen',
    author_email = '1@jin-dan.site',
    description = 'An Python SDK for OIer Space'
)
