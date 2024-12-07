from setuptools import setup, find_packages

setup(
    name='martinlab-utils',
    use_scm_version=True,
    setup_requires=['setuptools-scm'],
    description='Code and utilities used by Martin Lab members for teaching and research.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/MartinLabScience/MartinLab-Utils',
    license='GPLv3',
    packages=find_packages(include=["martinlab", "martinlab.*"]),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
