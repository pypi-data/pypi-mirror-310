from setuptools import setup

setup(
    name="getffff",
    version="0.1.1",
    description="A simple module that executes 'cat /flag'.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your_email@example.com",
    url="https://github.com/yourusername/getffff",
    packages=["getffff"],  # 명시적으로 패키지 지정
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "getffff = getffff:main",  # main 함수 등록
        ],
    },
    python_requires=">=3.6",
)
