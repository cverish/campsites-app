from setuptools import find_packages, setup

install_requires = ["fastapi", "uvicorn", "python-multipart"]

setup(
    name="server",
    install_requires=install_requires,
    use_scm_version={"root": "../"},
    setup_requires=["setuptools_scm"],
    packages=find_packages(where="./"),
    include_package_data=True,
)
