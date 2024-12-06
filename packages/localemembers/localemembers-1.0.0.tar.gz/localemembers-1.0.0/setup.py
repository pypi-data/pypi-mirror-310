from setuptools import setup, find_packages

setup(
    name='localemembers',
    version='1.0.0',
    author='EISX',
    author_email='eis-x@hotmail.com',
    description='A Python module to detect and format system localization information.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/eis-x/localemembers.git',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        # List of dependencies
    ],
    entry_points={
        'console_scripts': [
            'localemembers=localemembers.locale_members:main',
        ],
    },
)
