from setuptools import setup, find_packages

setup(
    name='localemembers',
    version='1.1.1',  # Updated version
    author='Your Name',
    author_email='your.email@example.com',
    description='A Python module to detect and format system localization information.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/localemembers',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'PyQt5',
    ],
    entry_points={
        'console_scripts': [
            'localemembers=localemembers.locale_members:main',
        ],
    },
)
