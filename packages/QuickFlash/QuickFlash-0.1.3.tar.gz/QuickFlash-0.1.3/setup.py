from setuptools import setup, find_packages

setup(
    name="QuickFlash",
    version="0.1.3",
    author="Reuel Bodhak",
    author_email="reuelbodhak07@gmail.com",
    description="Flash is a lightweight Python web framework inspired by Express.js. It enables developers to build scalable and efficient web applications with minimal setup, featuring an intuitive syntax, middleware support, and flexible routing. Designed for simplicity and productivity, Flash is perfect for developers looking to create robust back-end solutions in Python.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/07ReuelBodhak/QuickFlash.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires = ">=3.6",    
)