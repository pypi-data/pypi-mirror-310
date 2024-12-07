from setuptools import setup, find_packages

# Safely read the README file or use a default string if not found
try:
    with open('README.md', 'r', encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "Fsconnect API - A Flask-based API for managing API keys and summarization."

setup(
    name='fsconnect_api',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'Flask>=2.0',
    ],
    description='A Flask-based API for managing API keys and summarization tasks.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your_email@example.com',
    url='https://github.com/losuk/fsconnect-api',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
