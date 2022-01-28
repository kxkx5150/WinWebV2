from io import open
from setuptools import setup


with open('README.md') as read_me:
    long_description = read_me.read()


setup(
    name='WinWebV2',
    version="0.1.0",
    author="Kunihiro Ando",
    author_email='senna5150ando@gmail.com',
    packages=['WinWebV2'],
    license='MIT',
    url="https://github.com/kxkx5150/WinWebV2",
    description='Create HTML User Interface using WinWebV2 in Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    package_data={
        "WinWebV2": [
            'dll/*'
        ]
    },
    python_requires='>=3.9',
    keywords=['gui', 'html', 'javascript', 'electron'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Operating System :: Microsoft :: Windows"
    ],
    install_requires=[
        "orjson",
        "pypiwin32",
        "pywin32"
    ]
)
