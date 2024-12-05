from setuptools import setup, find_packages

setup(
    name="audio-files-organizer-iphone",  # Package name
    version="0.1.0",  # Initial release version
    description="A script to organize audio files and update metadata for syncing with Apple Music",
    long_description=open('README.md').read(),  # Read from README.md
    long_description_content_type="text/markdown",  # Long description format (Markdown)
    author="David Sandeep",  
    author_email="davidsandeep1996@gmail.com",  
    url="https://github.com/David-Sandeep/audio-files-organizer-iphone",  # GitHub URL
    packages=find_packages(),  # Automatically find packages
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Sound/Audio :: Conversion",
    ],
    install_requires=[  # Dependencies
        "mutagen",  # To handle audio file metadata
        "ffmpeg-python",  # Optional, for re-encoding failed files
        "tkinter",  # For GUI file dialog (note: may already be bundled with Python)
    ],
    python_requires='>=3.7',  # Minimum Python version
    entry_points={
        "console_scripts": [
            "audio-files-organizer-iphone=Audio_files_organizer_for_iphone.Audio_organizer:processit",  # Update this path
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
