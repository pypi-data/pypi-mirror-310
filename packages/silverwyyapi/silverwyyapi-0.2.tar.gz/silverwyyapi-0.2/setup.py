from setuptools import setup, find_packages

setup(
    name="silverwyyapi",
    version="0.2",
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        "requests~=2.31.0",
        "urllib3~=2.0.7",
        "pycryptodomex~=3.21.0",
    ],

    url="https://github.com/SilverW0o0W",
    author="Silver",
    author_email="silver.codingcat@gmail.com",
    license='MIT',
    description='',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    entry_points={
    }
)
