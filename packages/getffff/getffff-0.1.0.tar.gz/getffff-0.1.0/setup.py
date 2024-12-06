from setuptools import setup, find_packages

setup(
    name="getffff",  # 패키지 이름
    version="0.1.0",  # 초기 버전
    description="A simple module that executes 'cat /flag'.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your_email@example.com",
    url="https://github.com/yourusername/getffff",  # 깃허브 URL
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "getffff = getffff:main",  # 명령어 등록
        ],
    },
    python_requires=">=3.6",
)
