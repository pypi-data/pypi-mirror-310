from setuptools import setup, find_packages

setup(
    name="spotifycurator",  # Name of your package
    version="0.1.0",  # Initial version
    description="A tool to create public Spotify playlists from liked songs",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/spotifycurator",  # Your GitHub repository or project URL
    license="MIT",  # Choose an open-source license
    packages=find_packages(),  # Automatically find packages in your project
    install_requires=[
        "requests",
        "python-dotenv"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "spotifycurator=spotifycurator.spotifycurator:main",  # Exposes your main function as a CLI command
        ]
    },
    python_requires=">=3.7",
)
