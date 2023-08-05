from os.path import join
from os.path import dirname

from setuptools import find_packages
from setuptools import setup


def read_version():
    version_contents = {}
    with open(join(dirname(__file__), 'swapchat', 'version.py')) as fh:
        exec(fh.read(), version_contents)

    return version_contents['VERSION']

def load_readme():
    return "SwapChat Python Library"


INSTALL_REQUIRES = [
    "paho-mqtt",
]


setup(
    name='swapchat',
    version=read_version(),
    description='SwapChat Python Library',
    long_description=load_readme(),
    long_description_content_type='text/markdown',
    author='SwapChat',
    author_email='SwapChat@housechan.com',
    url='https://github.com/Generative-Labs/SwapChat-SDK-Python',
    license='MIT',
    keywords='SwapChat python sdk',
    packages=find_packages(
        exclude=[
            'tests',
            'tests.*',
            'testing',
            'testing.*',
            'virtualenv_run',
            'virtualenv_run.*',
        ],
    ),
    zip_safe=False,
    install_requires=INSTALL_REQUIRES,
    python_requires='>=3.6',
    project_urls={
        'Website': 'https://github.com/Generative-Labs/SwapChat-SDK-Python',
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)