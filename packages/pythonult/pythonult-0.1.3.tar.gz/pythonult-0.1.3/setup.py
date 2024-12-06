from setuptools import setup, find_packages

setup(
    name="pythonult",
    version="0.1.3",
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',    
        'numpy',
        'pytest',
        'gputil',
        'py-cpuinfo',
        'psutil',
        'pynulty',
        'emoji'
    ],
    author="lampadaire",
    author_email="ilovelampadaire@gmail.com",
    description="A collection of utilities.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/lamps-dev/utl",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)