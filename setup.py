from setuptools import setup, find_packages
 
setup(
    name='WinWebV2',    #パッケージ名
    version="0.0.1",
    description="Python Webview2 GUI",
    author="Kunihiro Ando",
    license='MIT',
    include_package_data=True,
    package_data={"WinWebV2": [
        'WinWebV2/dll/WebV2dll.dll',
        'WinWebV2/dll/WebView2Loader.dll',
        'WinWebV2/html/*'
    ]},
    classifiers=[
        "Development Status :: 1 - Planning"
    ],
    # install_requires=[
    #     'pypiwin32',
    #     'pywin32'
    # ],
    install_requires=[
        "pconst",
        "pypiwin32",
        "pywin32"
    ],
    packages=['WinWebV2']
)
