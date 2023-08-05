import setuptools

setuptools.setup(
    name="pwntools-tube-websocket",
    version="0.0.5",
    author="Frank",
    author_email="frankli0324@hotmail.com",
    description="websocket tube for pwntools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.7',
    install_requires=["websocket-client", "pwntools"],
)
