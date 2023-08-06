import setuptools

with open('ReadMe.md', 'r') as f:
    long_description = f.read()
    
with open('requirements.txt', 'r', encoding='UTF-16') as f:
    required = f.readlines()


setuptools.setup(
    name="webpage-image-downloader",
    version="0.1.2",
    
    author="A-Bak",
    author_email="adam.bak753@gmail.com",
    
    description="Tool for extracting and saving specific images from websites.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='webscraping webcrawler image img downloader selenium-python',
    url='https://github.com/A-Bak/webpage-img-downloader',
    
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=required,
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    
    entry_points={
        'console_scripts': [
            'wid-downloader=wid.cli.web_img_downloader:main',
            'wid-crawler=wid.cli.web_img_crawler:main',
        ],
    },
)