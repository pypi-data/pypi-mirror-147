import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="dpnn_image",
    version="0.0.1",
    author="yangshuai",
    author_email="shaneyangshuai@didiglobal.com",
    description="dpnn image library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/",
    packages=setuptools.find_packages(),
    package_data={'dpnn_image':['*/*']},
    install_requires=['numpy', 'opencv-python'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
