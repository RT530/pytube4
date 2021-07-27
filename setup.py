from setuptools import setup, find_packages

setup(
    name="pytube4",
    version="1",
    python_requires=">=3.6",
    keywords=["youtube", "download", "video", "stream"],
    description="Download Youtube Videos",
    license="MIT",
    author="Ricky Tsai",
    packages={'pytube4': 'pytube4'},
    include_package_data=True,
    platforms="any",
    install_requires=[
        'selenium',
        'chromedriver-autoinstaller'
    ]
)
