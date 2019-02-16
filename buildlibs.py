from util import *
import subprocess, os, sys

if not is_python3():
    print("python version >= 3.0 required")
    exit()

def generator_build_directory(generator):
    return unilib_root_directory() + "/build/" + generator.replace(" ","-")

def install_directory(generator):
    return generator_build_directory(generator) + "/install"

def make_builddir(generator, libname):
    builddir = generator_build_directory(generator) + "/" + libname
    result = subprocess.run(["cmake", "-E", "make_directory", builddir])
    if not result.returncode == 0:
        print("failed to make directory %s" % builddir)
        return False
    return builddir

def build_and_install(builddir, libname):
    result = subprocess.run(
        ["cmake", "--build", builddir, "--config", "release", "--target", "install"]
    )
    if not result.returncode == 0:
        print("failed to build %s" % libname)
        return False
    return True

def configure_and_build_and_install(generator, libname, config_options):
    builddir = make_builddir(generator, libname)
    if not builddir:
        return False

    libdir = unilib_root_directory() + "/" + libname

    result = subprocess.run(
        ["cmake", "-E", "chdir", builddir,
         "cmake", libdir, "-G", generator,
         '-DCMAKE_INSTALL_PREFIX=' + install_directory(generator)
        ]
        + config_options
    )

    if not result.returncode == 0:
        print(result.args)
        print("failed to configure %s" % libname)
        return False

    return build_and_install(builddir, libname)

def build_irrlicht(generator):
    libname = "irrlicht"
    return configure_and_build_and_install(generator, libname, [])

def build_zlib(generator):
    libname = "zlib"
    result = configure_and_build_and_install(generator, libname, [])

    # undo zlib/CMakeLists.txt renaming zconf.h, to keep the repository unmodified
    oldname = unilib_root_directory() + "/zlib/zconf.h.included"
    newname = unilib_root_directory() + "/zlib/zconf.h"
    subprocess.run(["cmake", "-E", "rename", oldname, newname])

    return result
    
def build_ogg(generator):
    libname = "ogg"
    return configure_and_build_and_install(generator, libname, [
        "-DBUILD_SHARED_LIBS=TRUE"
    ])
    
def build_vorbis(generator):
    libname = "vorbis"
    install = install_directory(generator)
    return configure_and_build_and_install(generator, libname, [
        "-DBUILD_SHARED_LIBS=TRUE",
        '-DOGG_INCLUDE_DIRS=' + install + '/include',
        '-DOGG_LIBRARIES=' + install + '/lib/ogg.lib'
    ])
    
def build_openal(generator):
    libname = "openal"
    return configure_and_build_and_install(generator, libname, [
        "-DALSOFT_UTILS=FALSE", "-DALSOFT_NO_CONFIG_UTIL=TRUE",
        "-DALSOFT_EXAMPLES=FALSE", "-DALSOFT_TESTS=FALSE",
        "-DALSOFT_CONFIG=FALSE", "-DALSOFT_HRTF_DEFS=FALSE",
        "-DALSOFT_AMBDEC_PRESETS=FALSE"
    ])
    
def build_sqlite3(generator):
    libname = "sqlite3"
    return configure_and_build_and_install(generator, libname, [])

def build_all(generator):
    print("building irrlicht")
    if not build_irrlicht(generator):
        return False
    print("building zlib")
    if not build_zlib(generator):
        return False
    print("building ogg")
    if not build_ogg(generator):
        return False
    print("building vorbis")
    if not build_vorbis(generator):
        return False
    print("building openal")
    if not build_openal(generator):
        return False
    print("building sqlite3")
    if not build_sqlite3(generator):
        return False

    return True


global_cache = load_cache()
if not "cmake_generators" in global_cache:
    print("bad cache file, missing 'cmake_generators' delete it and run config.py")
    exit(1)

if len(global_cache["cmake_generators"]) == 0:
    print("no generators selected, run config.py")

for gen in global_cache["cmake_generators"]:
    print("building for %s" % gen)
    if not build_all(gen):
        print("building for %s failed" % gen)

