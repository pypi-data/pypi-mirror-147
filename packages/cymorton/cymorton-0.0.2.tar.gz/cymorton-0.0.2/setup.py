import io
import os
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import relpath
from os.path import splitext
from typing import Set, Any, List, Dict

from setuptools import Extension
from setuptools import find_packages
from setuptools import setup
from setuptools.dist import Distribution
from pathlib import Path

from Cython.Build import cythonize

try:
    # Allow installing package without any Cython available. This
    # assumes you are going to include the .c files in your sdist.
    import Cython
except ImportError:
    Cython = None


class BinaryDistribution(Distribution):
    """Distribution which almost always forces a binary package with platform name"""

    def has_ext_modules(self):
        return super().has_ext_modules() or not os.environ.get('SETUPPY_ALLOW_PURE')


def get_property(prop, packages_path: str, packages: List[str]) -> Set[Any]:
    """
    Searches and returns a property from all packages __init__.py files
    :param prop: property searched
    :param packages_path: root path of packages to search into
    :param packages: array of packages paths
    :return: an set of values
    """
    results = set()
    namespace: Dict[str, Any] = {}
    for package in packages:
        init_file = open(Path(packages_path, package, "__init__.py")).read()
        exec(init_file, namespace)
        if prop in namespace:
            results.add(namespace[prop])
    return results


def get_requirements(file_path: str, no_precise_version: bool = False) -> List[str]:
    _requirements = []
    try:
        with open(file_path, "rt") as r:
            for line in r.readlines():
                package = line.strip()
                if not package or package.startswith("#"):
                    continue
                if no_precise_version:
                    package = package.split("==")[0]
                _requirements.append(package)
    except FileExistsError:
        pass
    return _requirements


def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names), encoding=kwargs.get('encoding', 'utf8')
    ) as fh:
        return fh.read()


project_name = "cymorton"
github_home = "https://github.com/decitre"

if __name__ == '__main__':
    _packages_path = "src"
    _packages = find_packages(where=_packages_path)
    main_package_path = {
        Path(_packages_path, *package.split("."))
        for package in _packages
        if package.endswith(project_name)
    }.pop()
    version = get_property("__version__", _packages_path, _packages).pop()
    requirements = ["click"]
    requirements.extend(get_requirements("requirements.txt", no_precise_version=True))
    requirements_test = get_requirements("requirements_test.txt")

    ext_modules = [
        Extension(
            splitext(relpath(path, 'src').replace(os.sep, '.'))[0],
            sources=[path],
            include_dirs=[dirname(path)],
        )
        for root, _, _ in os.walk('src')
        for path in glob(join(root, '*.pyx'))
    ]

    setup(
        name=project_name,
        version=version,
        license='MIT',
        description='A morton code codec in c++/cython',
        long_description=re.compile(
            '^.. start-badges.*^.. end-badges', re.M | re.S
        ).sub('', read('README.rst')),
        author='Emmanuel Decitre',
        url=f'{github_home}/python-{project_name}',
        packages=find_packages(_packages_path),
        package_dir={'': _packages_path},
        py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
        include_package_data=True,
        zip_safe=False,
        classifiers=[
            # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3 :: Only',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Cython',
            'Programming Language :: Python :: Implementation :: CPython',
        ],
        project_urls={
            'Issue Tracker': f'{github_home}/python-{project_name}/issues',
        },
        keywords=["morton", "z-curve"],
        python_requires='>=3.6',
        install_requires=requirements,
        extras_require={"dev": requirements_test},
        setup_requires=['Cython'],
        entry_points={'console_scripts': [f'{project_name} = {project_name}.cli:main']},
        ext_modules=cythonize(ext_modules, language_level="3"),
        distclass=BinaryDistribution,
    )
