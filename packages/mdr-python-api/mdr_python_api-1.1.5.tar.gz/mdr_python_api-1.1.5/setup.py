from setuptools import find_packages, setup

setup(
    name="mdr_python_api",
    version="1.1.5",
    packages=find_packages("src"),
    package_data={"mdr_python_api": ["code-flow.json"]},
    package_dir={"": "src"},
    install_requires=["requests", "jwcrypto"],
)
