import multiprocessing
import sys
from pathlib import Path
from typing import List

from Cython.Build import cythonize
from Cython.Distutils.build_ext import new_build_ext as cython_build_ext
from setuptools import Extension, Distribution
from setuptools.command.build_ext import build_ext
SOURCE_DIR = Path("handsfree")
BUILD_DIR = Path("cython_build")

_build_ext_module = sys.modules.get('setuptools.command.build_ext')
print("_build_ext_module------------:" + str(_build_ext_module))
print("build_ext-------:"+str(build_ext))

def build() -> None:
    # Collect and cythonize all files
    extension_modules = cythonize_helper(get_extension_modules())

    # Use Setuptools to collect files
    distribution = Distribution({
        "ext_modules": extension_modules,
        "cmdclass": {
            "build_ext": cython_build_ext,
        },
    })

    # Grab the build_ext command and copy all files back to source dir. This is
    # done so that Poetry grabs the files during the next step in its build.
    print("------run_command------")
    distribution.run_command("build_ext")
    print("------get_command_obj------")
    build_ext_cmd = distribution.get_command_obj("build_ext")
    print("------copy_extensions_to_source------", str(build_ext_cmd), str(distribution))
    build_ext_cmd.copy_extensions_to_source()


def get_extension_modules() -> List[Extension]:
    """Collect all .py files and turn them into Distutils/Setuptools
    Extensions"""

    extension_modules: List[Extension] = []

    for py_file in SOURCE_DIR.rglob("*.py"):
        # Get path (not just name) without .py extension
        module_path = py_file.with_suffix("")

        # Convert path to module name
        module_path = str(module_path).replace("/", ".").replace("\\", ".")

        extension_module = Extension(
            name=module_path,
            sources=[str(py_file)]
        )
        print(extension_module)
        extension_modules.append(extension_module)

    return extension_modules


def cythonize_helper(extension_modules: List[Extension]) -> List[Extension]:
    """Cythonize all Python extensions"""

    return cythonize(
        module_list=extension_modules,

        # Don't build in source tree (this leaves behind .c files)
        build_dir=BUILD_DIR,

        # Don't generate an .html output file. This will contain source.
        annotate=False,

        # Parallelize our build
        nthreads=multiprocessing.cpu_count() * 2,

        # Tell Cython we're using Python 3
        compiler_directives={"language_level": "3"},

        # (Optional) Always rebuild, even if files untouched
        force=True,
    )


if __name__ == '__main__':
    build()
