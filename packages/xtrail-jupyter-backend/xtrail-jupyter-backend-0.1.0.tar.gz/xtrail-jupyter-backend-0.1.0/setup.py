from setuptools import setup, find_packages

setup(
    name="xtrail-jupyter-backend",
    version="0.1.0",
    description="Run Jupyter Notebooks with a Flask backend and public ngrok URL.",
    author="Harisha P C",
    author_email="info@xtrail.in",
    url="https://xtrail.in",
    packages=find_packages(),
    install_requires=[
        "Flask",
        "pyngrok",
        "waitress",
        "notebook",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "xtrail-backend=xtrail_backend.app:app.run",
        ]
    },
)
