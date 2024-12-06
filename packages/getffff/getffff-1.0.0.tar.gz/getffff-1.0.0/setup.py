from setuptools import setup, find_packages

setup(
    name="getffff",  # 패키지 이름
    version="1.0.0",  # 버전
    packages=find_packages(),  # 패키지 디렉토리 탐색
    install_requires=[],  # 의존 패키지 (없음)
    entry_points={
        'console_scripts': [
            'getffff = getffff.__main__:main',  # CLI 명령어 설정
        ],
    },
    author="Your Name",
    author_email="your_email@example.com",
    description="A simple CLI tool to display the contents of /flag",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/your_username/getffff",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
