from setuptools import find_packages, setup

setup(
    name='module-warehouse',
    version='0.1',
    description='plugin which displays modules stored in warehouse',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)