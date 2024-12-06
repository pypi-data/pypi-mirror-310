from setuptools import setup, find_packages

setup(
    name="wee_project_creater",
    version="1.0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'create-project=main:main',
        ],
    },
    author="Kong Haifeng",
    author_email="konghaifeng@cmcm.com",
    description="A Python project structure generator with logging and configuration support",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/konghaifeng/project_creater",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)