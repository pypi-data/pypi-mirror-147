from setuptools import setup

with open("README.md", "r") as fh:
    long_desc = fh.read()

setup(
    name='ztplite',
    version='0.2.1',
    packages=['ztplite'],
    url='https://github.com/p4r4n0y1ng',
    license='Apache 2.0',
    author='p4r4n0y1ng',
    author_email='jhuber@fortinet.com',
    description='Represents the base components of the Zero Touch Provisioning Lite Process',
    long_description=long_desc,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=['requests', 'Jinja2', 'PyYAML', 'pyfmg']
)
