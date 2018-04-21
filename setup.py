"""
    :author: inunarun
             Aerospace Systems Design Laboratory,
             Georgia Institute of Technology,
             Atlanta, GA

    :date: 2018-04-15 20:35:50
"""


from distutils.command.install import install
from distutils.command.clean import clean
from pip.req import parse_requirements
from setuptools import setup
import sys


class MyInstall(install):
    """
    A custom installation object that cleans the installation directory
    after completion of setup
    """

    def run(self):
        """
        Overridden method "run" in order to clean the directory after setup
        """

        install.run(self)
        c = clean(self.distribution)
        c.all = True
        c.finalize_options()
        c.run()


if __name__ == '__main__':
    requirements = []
    for entry in parse_requirements("requirements.txt", session=False):
        requirements.append((str(entry.req)))

    setup(
        name             = "morphological-matrix",
        version          = "0.1.0",
        description      = "Python-based Morphological Matrix building library",
        author           = "Aerospace Systems Design Laboratory",
        packages         = [
                             "morphologicalmatrix",
                           ],
        keywords         = "morphological-matrix systems-engineering system-architecting",
        license          = "MIT",
        platforms        = [
                             "Windows",
                             "Linux",
                             "Unix"
                           ],
        classifiers      = [
                             "Development Status :: Alpha",
                             "Environment :: Console",
                             "Intended Audience :: Engineers",
                             "Operating System :: Microsoft.Windows",
                             "Operating System :: POSIX.Linux",
                             "Operating System :: Unix",
                             "Programming Language :: Python",
                             "Topic :: Morphological Matrix",
                           ],
        cmdclass         = {
                             "install": MyInstall
                           },
        install_requires = requirements
    )
