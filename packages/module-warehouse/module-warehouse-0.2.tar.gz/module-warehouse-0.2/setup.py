from setuptools import find_packages, setup

setup(
    name='module-warehouse',
    version='0.2',
    description='plugin which displays modules stored in warehouse',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Viktor Kubec",
    author_email="Viktor.Kubec@gmail.com",
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)