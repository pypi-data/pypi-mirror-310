from setuptools import setup, find_packages

setup(
    name="xtrail-jupyter-backend",
    version="0.4.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask>=3.0.0",
        "pyngrok>=7.0.0",
        "waitress>=2.1.0",
        "notebook>=6.5.0",
    ],
    entry_points={
        "console_scripts": [
            "xtrail-backend = xtrail_backend.app:start_backend",
        ],
    },
    description="XTrail Jupyter Backend for secure notebook access.",
    author="Harisha P C",
    author_email="info@xtrail.in",
    url="https://pypi.org/project/xtrail-jupyter-backend/",
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
    ],
)
