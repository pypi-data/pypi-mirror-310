from setuptools import setup, find_packages

setup(
    name='helpme_kratik',
    version='0.5.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[            # Any dependencies your package needs
        'numpy',
        'requests',
    ],
    author='Kratik Jain',
    author_email='kratikjain1520@gmail.com',
    description='A brief description of your package',
    long_description_content_type='text/markdown',
    url='https://github.com/KratikJain10/helpme-kratik.git',  # Link to the package repo
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
