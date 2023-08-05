from setuptools import setup
from setuptools.command.install import install
import webbrowser


class PostInstallCommand(install):
    """Pre-installation for installation mode."""

    def run(self):
        webbrowser.open("https://www.youtube.com/watch?v=YnL9vAFphmE")
        install.run(self)


setup(
    author="Radon Rosborough",
    author_email="radon.neon@gmail.com",
    description="Fun with gps",
    license="MIT",
    name="funwithgps",
    version="0.0.1",
    cmdclass={
        "install": PostInstallCommand,
    },
)
