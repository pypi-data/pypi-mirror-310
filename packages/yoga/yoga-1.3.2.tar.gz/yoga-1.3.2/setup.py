#!/usr/bin/env python
# encoding: UTF-8

import os
import subprocess

from setuptools import setup, find_packages
from setuptools.command.build_ext import build_ext


def _find_msbuild(plat_spec="x64"):
    from setuptools import msvc

    if hasattr(msvc, "msvc14_get_vc_env"):
        vc_env = msvc.msvc14_get_vc_env(plat_spec)
        if "vsinstalldir" in vc_env:
            msbuild_path = os.path.join(
                vc_env["vsinstalldir"],
                "MSBuild",
                "Current",
                "Bin",
                "MSBuild.exe",
            )
            if os.path.isfile(msbuild_path):
                return msbuild_path

    for path in msvc.EnvironmentInfo(plat_spec).VCTools:
        if "\\VC\\" not in path:
            continue
        msbuild_path = os.path.join(
            path[: path.index("\\VC\\")],
            "MSBuild",
            "Current",
            "Bin",
            "MSBuild.exe",
        )
        if os.path.isfile(msbuild_path):
            return msbuild_path

    raise Exception("Unable to find any Visual Studio installation")


class CustomBuildExt(build_ext):
    def build_extensions(self):
        if not os.path.isdir("./assimp/build"):
            os.mkdir("./assimp/build")

        os.chdir("./assimp/build")

        if self.compiler.compiler_type == "unix":
            os.environ["CXXFLAGS"] = "--std=c++11 %s" % os.environ.get(
                "CXXFLAGS", ""
            )
            subprocess.call(
                [
                    "cmake",
                    "..",
                    "-DBUILD_SHARED_LIBS=OFF",
                    "-DASSIMP_BUILD_ASSIMP_TOOLS=OFF",
                    "-DASSIMP_BUILD_TESTS=OFF",
                    "-DASSIMP_BUILD_ZLIB=ON",
                ]
            )
            subprocess.call(["make"])
        elif self.compiler.compiler_type == "msvc":
            msbuild = _find_msbuild()
            subprocess.call(
                [
                    "cmake",
                    "..",
                    "-DBUILD_SHARED_LIBS=OFF",
                    "-DASSIMP_BUILD_ASSIMP_TOOLS=OFF",
                    "-DASSIMP_BUILD_TESTS=OFF",
                    "-DASSIMP_BUILD_ZLIB=ON",
                    "-DLIBRARY_SUFFIX=",
                ]
            )
            subprocess.call(
                [msbuild, "-p:Configuration=Release", "Assimp.sln"]
            )
        else:
            raise Exception("Unsupported platform")

        os.chdir("../..")

        build_ext.build_extensions(self)


long_description = ""
if os.path.isfile("README.rst"):
    long_description = open("README.rst", "r").read()


setup(
    name="yoga",
    version="1.3.2",
    description="Yummy Optimizer for Gorgeous Assets",
    url="https://github.com/wanadev/yoga",
    project_urls={
        "Source Code": "https://github.com/wanadev/yoga",
        "Documentation": "https://wanadev.github.io/yoga/",
        "Changelog": "https://github.com/wanadev/yoga#changelog",
        "Issues": "https://github.com/wanadev/yoga/issues",
        "Chat": "https://discord.gg/BmUkEdMuFp",
    },
    license="BSD-3-Clause",
    long_description=long_description,
    keywords="image webp jpeg png optimizer guetzli zopfli zopflipng libwebp 3d model mesh assimp gltf glb converter",
    author="Wanadev",
    author_email="contact@wanadev.fr",
    maintainer="Fabien LOISON, Alexis BREUST",
    packages=find_packages(),
    setup_requires=["cffi>=1.0.0"],
    install_requires=[
        "cffi>=1.0.0",
        "imagequant>=1.0.2",
        "mozjpeg-lossless-optimization>=1.0.0",
        "pillow>=6.2.2",
        "pyguetzli>=1.0.0",
        "unidecode>=1.0.0",
        "zopflipy>=1.0",
    ],
    extras_require={
        "dev": [
            "nox",
            "flake8",
            "black",
            "pytest",
            "sphinx",
            "sphinx-rtd-theme",
            "codespell",
        ]
    },
    entry_points={
        "console_scripts": [
            "yoga = yoga.__main__:main",
        ]
    },
    cffi_modules=["yoga/model/assimp_build.py:ffibuilder"],
    cmdclass={
        "build_ext": CustomBuildExt,
    },
)
