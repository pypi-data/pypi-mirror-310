from setuptools import setup, find_packages

setup(
    name="audio_files_organizer_iphone",
    version="0.0.1",
    description="A tool for organizing audio files for iPhone compatibility",
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type="text/markdown",  # Set the type of the README file
    author="David Sandeep",
    author_email="davidsandeep1996@gmail.com",
    url="https://github.com/David-Sandeep/audio-files-organizer-iphone",
    packages=find_packages(),  # Automatically find packages
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Sound/Audio :: Conversion",
    ],
    extras_require={
        "gui": ["tkinter"]
    },
    python_requires='>=3.7',  # Minimum Python version
    entry_points={
        "console_scripts": [
            "audio_files_organizer_iphone = Audio_files_organizer_for_iphone.Audio_organizer:processit",  # Update this path
        ],
    },
    include_package_data=True,  # Include non-Python files as specified in MANIFEST.in
    zip_safe=False,  # Don't mark the package as zip-safe if it isn't
)
