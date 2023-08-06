from setuptools import find_packages, setup

setup(
    name='netbox-sync',
    version='0.0.0',
    description='Netbox Sync',
    long_description='A Network Device Sync plugin',
    url='https://github.com/dansheps/netbox-sync/',
    download_url='https://www.pypi.org/project/netbox-sync/',
    author='Daniel Sheppard',
    author_email='dans@dansheps.com',
    license='Apache 2.0',
    install_requires=[
        'importlib',
        'napalm'
    ],
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    zip_safe=False,
)
