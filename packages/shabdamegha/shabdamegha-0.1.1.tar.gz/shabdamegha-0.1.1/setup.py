from setuptools import setup, find_packages

setup(
    name="shabdamegha",
    version="0.1.1",
    author="Dr. Swarupananda Bissoyi",
    author_email="swarupananda@gmail.com",
    description="A python library to generate word cloud for Odia language with proper rendering of Ligatures (Yuktakshars). ଯୁକ୍ତାକ୍ଷର ଗୁଡ଼ିକୁ ସଠିକ୍‌ ପ୍ରଦର୍ଶିତ କରି ଶବ୍ଦମେଘ ସୃଷ୍ଟି କରିବା ନିମନ୍ତେ ଏକ ପାଇଥନ୍‌ ଲାଇବ୍ରେରୀ",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sbissoyi/shabdamegha",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Pillow",
        "uharfbuzz",
        "freetype-py",
        "numpy"
    ],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
