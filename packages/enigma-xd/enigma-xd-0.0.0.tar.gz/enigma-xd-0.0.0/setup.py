from setuptools import find_packages, setup



if __name__ == "__main__":
    setup(
        name="enigma-xd",
        description="enigma - the message is gone forever",
        long_description="Hail Hitler!!!",
        long_description_content_type="text/markdown",
        author="Kishal Mandal",
        author_email="km.kkishal@gmail.com",
        url="https://github.com/kishalxd/enigma",
        license="Apache License",
        packages=find_packages(),
        include_package_data=True,
        platforms=["linux", "unix"],
        python_requires=">=3.6",
    )