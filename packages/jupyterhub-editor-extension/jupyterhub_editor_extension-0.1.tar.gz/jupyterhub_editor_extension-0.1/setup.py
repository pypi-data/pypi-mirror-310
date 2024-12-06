from setuptools import setup, find_packages

setup(
    name="jupyterhub_editor_extension",
    version="0.1",
    packages=find_packages(),
    entry_points={
        "jupyterhub.custom_extensions": [
            "jupyterhub_editor_extension = editor_extension"
        ]
    }
)
