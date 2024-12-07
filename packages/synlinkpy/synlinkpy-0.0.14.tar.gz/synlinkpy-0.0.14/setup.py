from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name="synlinkpy",
    version="0.0.14",
    packages=find_packages(where="src"),  # Locate packages in 'src'
    package_dir={"": "src"},  # Set the base package directory to 'src'
    description="A SynLink PDU API Client",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Kevin Han",
    author_email="kevin.han@synaccess.com",
    url="https://synaccess.com",
    install_requires=[
        'requests >= 2.2.1',
        'requests-toolbelt >= 0.9.1',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='synlink pdu api client',
)
