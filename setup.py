from setuptools import setup, find_packages
setup(
    name="mokeychain",
    version="0.1",
    description="A high level API for the macOS Keychain",
    packages=find_packages(),
    author="mosen",
    license="MIT",
    url="https://github.com/mosen/mokeychain",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Environment :: MacOS X :: Cocoa',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 2.7'
    ],
    keywords='keychain macOS Security framework',
    # install_requires=[
    #     'pyobjc-core',
    #     'pyobjc-framework-Cocoa'
    # ],
    entry_points={
        'console_scripts': [
            'mokey=mokeychain.cli:main'
        ]
    }
)


