from setuptools import setup, find_packages

setup(
    name='Wolaita_POST',  # Unique package name for PyPI
    version='1.0',
    author='Sisagegn Samuel',
    author_email='samuelsisagegn@gmail.com',
    description='A POS tagger for the Wolaita language using deep learning',
    long_description=open('README.md', encoding='utf-8').read(),  # Safer file path handling
    long_description_content_type='text/markdown',  # Ensures proper Markdown rendering
    url='https://github.com/Sisagegn/Wolaita_POST',  # Repository URL
    project_urls={  # Additional project links
        "Documentation": "https://github.com/Sisagegn/Wolaita_POST/wiki",
        "Source": "https://github.com/Sisagegn/Wolaita_POST",
        "Tracker": "https://github.com/Sisagegn/Wolaita_POST/issues",
    },
    packages=find_packages(include=['WolaitaPOSTagger', 'WolaitaPOSTagger.*']),  # Includes sub-packages
    install_requires=[
        'tensorflow>=2.0.0',  # For deep learning
        'numpy>=1.18.0',  # For numerical computations
        'nltk>=3.5',  # For NLP tasks
        'fasttext>=0.9.2'  # For word embeddings
    ],
    extras_require={  # Optional dependencies
        'dev': ['pytest>=6.0', 'sphinx>=4.0'],  # Development tools
        'gpu': ['tensorflow-gpu>=2.0.0'],  # GPU support for TensorFlow
    },
    classifiers=[  # Metadata for package index
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Topic :: Text Processing :: Linguistic',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    keywords='Wolaita POS tagging NLP deep learning',  # Search keywords
    python_requires='>=3.6',  # Minimum required Python version
    include_package_data=True,  # Include non-code files specified in MANIFEST.in
    package_data={  # Additional files to include within the package
        '': ['*.txt', '*.md'],  # Include text and markdown files
    },
    entry_points={  # Optional CLI tool entry point
        'console_scripts': [
            'wolaita-pos=WolaitaPOSTagger.wolaita_pos_tagger:main',  # Command-line entry
        ],
    },
)
