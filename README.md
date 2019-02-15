# Minetest Unilib
The purpose of Minetest Unilib is to simplify the process of building Minetest, particularly on Windows, since the process is a lot more painful there, and because I want to make use of Visual Studio's debugger while hunting down issues.

This goal is achieved 2 ways. Firstly, by compiling all the required 3rd party libraries in one repository, and generalizing the process of building them. For the libraries that already have active, CMake buildable git repositories (zlib, ogg, vorbis, openal), this is done by simply including those repositories as git submodules to this one. For others (irrlicht, sqlite3), they have been made CMake buildable and placed in repositories [here(irrlicht)](https://github.com/blindley/irrlicht-cmake) and [here(sqlite3)](https://github.com/blindley/sqlite3-cmake).

The next way the goal is achieved is by having scripts that automate much of the build process. Currently these scripts are only available for Powershell, which I use. But if people request it, I will make more of these in other shell scripts. Or better yet, a parent CMakeLists.txt that builds all the sub-components. But I'm not very skilled with CMake, and my first attempts at this failed.

## The Process

```
> git clone https://github.com/blindley/minetest-unilib.git
> cd minetest-unilib
```

### With Powershell Scripts
```
> ./powershell-scripts/build_libraries.ps1 -Generator "Visual Studio 15 2017 Win64"
> # or the CMake Generator of your choice
```

This will create a directory `"minetest-unilib/build/Visual-Studio-15-2017-Win64/"` with a sub-directory for each third party library, then build them, and install in a directory named `"install"` within that sub-directory.

Then you want to clone the minetest repository, or a fork of it. This can of course be done without powershell.

```
> mkdir branches
> cd branches
> git clone https://github.com/mintest/mintest.git
> mkdir build
> cd build
```

Then there is another script here that sets the CMake variables for minetest based on where the other script installs the libraries.

```
> ../../powershell-scripts/configure_branch.ps1 -Generator "Visual Studio 15 2017 Win64" -Branch ../minetest -Destination .
```

If you're not using powershell, but are building manually (or writing scripts for a different shell), it's still useful to take a look at those .ps1 files to see the CMake configure options I pass when building each library.

## What's Missing?

Currently, only required libraries and the sound libraries are provided. Curl, Gettext, FreeType and LevelDB are all disabled in the provided configure script. I will add these eventually, but I don't need them right now.