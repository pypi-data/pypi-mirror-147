import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jeeachinto",
    version="0.3.6",
    author="IISS Luigi Dell' Erba",
    author_email="naoittdellerba@gmail.com",
    install_requires=["kthread"],
    description="Connect to hosts in an easier way",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/naodellerba/jeeachinto",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License"
    ],
    python_requires='>=2.7',
)
