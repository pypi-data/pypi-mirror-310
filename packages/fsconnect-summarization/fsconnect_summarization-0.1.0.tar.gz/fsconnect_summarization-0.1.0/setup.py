from setuptools import setup, find_packages

setup(
    name='fsconnect-summarization',
    version='0.1.0',
    description='A text summarization API for FSConnect',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='FSConnect',
    author_email='kennlosuk@gmail.com',
    url='https://github.com/losuk/fsconnect-summarization',  # Change this to your repo URL
    packages=find_packages(),
    install_requires=[
        'Flask>=2.0.0',
    ],
    entry_points={
        'console_scripts': [
            'fsconnect-summarization=fsconnect_summarization.app:app.run',  # For running the app directly
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
