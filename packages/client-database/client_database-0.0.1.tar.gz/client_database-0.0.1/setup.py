from setuptools import setup, find_packages

setup(
    name='client_database',  # Your package name
    version='0.0.1',        # Your package version
    packages=find_packages(),
    install_requires=[
        'pandas',          # List your dependencies here
    ],
    package_data={
        'client_database': ['data/*.csv', 'client_database.db'],  # Include data files
    },
    include_package_data=True,
    # Include other metadata as needed (e.g., author, description, license)
    author='Your Name',
    author_email='your.email@example.com',
    description='A package for managing client database',  # Brief description
    long_description='''  # More detailed description (optional)
        This package provides tools for creating, populating, and querying a SQLite client database.
    ''',
    # You can add a long_description_content_type if using markdown for your long_description
    long_description_content_type='text/markdown',  # Optional, if long_description is markdown
    classifiers=[  # Classifiers help categorize your package (optional)
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Replace with your license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7', # specify minimum Python version
    entry_points={  # Optional: Define command-line scripts
        'console_scripts': [
            'create_db=client_database.create_database:create_database', # Example
            'riverside_script=client_database.riverside:main', # Example: make margem_do_rio callable from the command line, assuming you have a main function in riverside.py
        ],
    },

)