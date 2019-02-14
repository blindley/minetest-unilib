param(
    [string]$Generator = ""
)

$root = (Resolve-Path "$($PSScriptRoot)\..")
$builddir_leaf = ($Generator -replace " ","-")

$Script:function_result = $true

function make_builddir {
    param([String]$libname)
    $builddir = "$($root)/build/$($builddir_leaf)/$($libname)"
    mkdir $builddir -Force | Out-Null
    if (-not (Test-Path $builddir)) {
        Write-Host "failed to make directory $($builddir)"
        $Script:function_result = $false
        return
    }

    $Script:function_result = $builddir
}

function build_irrlicht {
    $libname = "irrlicht"
    make_builddir $libname
    $builddir = $Script:function_result
    cd $builddir

    $Script:function_result = cmake "$($root)/$($libname)" -G"$($Generator)" `
        -DCMAKE_INSTALL_PREFIX="$($builddir)/install"

    if (-not $Script:function_result) {
        Write-Host "failed to configure $($libname)" -ForegroundColor Red
        return
    }

    $Script:function_result = cmake --build . --config release --target install

    if (-not $Script:function_result) {
        Write-Host "failed to build $($libname)" -ForegroundColor Red
    }
}

function build_zlib {
    $libname = "zlib"
    make_builddir $libname
    $builddir = $Script:function_result
    cd $builddir
    
    $Script:function_result = cmake "$($root)/$($libname)" -G"$($Generator)" `
    -DCMAKE_INSTALL_PREFIX="$($builddir)/install"

    if (-not $Script:function_result) {
        Write-Host "failed to configure $($libname)" -ForegroundColor Red
        return
    }

    $Script:function_result = cmake --build . --config release --target install

    if (-not $Script:function_result) {
        Write-Host "failed to build $($libname)" -ForegroundColor Red
    }

    # undo zlib/CMakeLists.txt renaming zconf.h, to keep the repository unmodified
    Rename-Item "$($root)/$($libname)/zconf.h.included" zconf.h
}
    
function build_ogg {
    $libname = "ogg"
    make_builddir $libname
    $builddir = $Script:function_result
    cd $builddir

    $Script:function_result = cmake "$($root)/$($libname)" -G"$($Generator)" `
        -DCMAKE_INSTALL_PREFIX="$($builddir)/install" `
        -DBUILD_SHARED_LIBS=TRUE

    if (-not $Script:function_result) {
        Write-Host "failed to configure $($libname)" -ForegroundColor Red
        return
    }

    $Script:function_result = cmake --build . --config release --target install

    if (-not $Script:function_result) {
        Write-Host "failed to build $($libname)" -ForegroundColor Red
    }
}
    
function build_vorbis {
    $libname = "vorbis"
    make_builddir $libname
    $builddir = $Script:function_result
    cd $builddir

    $ogg = "$($root)/build/$($builddir_leaf)/ogg/install"

    $Script:function_result = cmake "$($root)/$($libname)" -G"$($Generator)" `
        -DCMAKE_INSTALL_PREFIX="$($builddir)/install" `
        -DBUILD_SHARED_LIBS=TRUE `
        -DOGG_INCLUDE_DIRS="$($ogg)/include" `
        -DOGG_LIBRARIES="$($ogg)/lib/ogg.lib"

    if (-not $Script:function_result) {
        Write-Host "failed to configure $($libname)" -ForegroundColor Red
        return
    }

    $Script:function_result = cmake --build . --config release --target install

    if (-not $Script:function_result) {
        Write-Host "failed to build $($libname)" -ForegroundColor Red
    }
}
    
function build_openal {
    $libname = "openal"
    make_builddir $libname
    $builddir = $Script:function_result
    cd $builddir

    $Script:function_result = cmake "$($root)/$($libname)" -G"$($Generator)" `
        -DCMAKE_INSTALL_PREFIX="$($builddir)/install" `
        -DALSOFT_UTILS=FALSE -DALSOFT_NO_CONFIG_UTIL=TRUE `
        -DALSOFT_EXAMPLES=FALSE -DALSOFT_TESTS=FALSE `
        -DALSOFT_CONFIG=FALSE -DALSOFT_HRTF_DEFS=FALSE `
        -DALSOFT_AMBDEC_PRESETS=FALSE

    if (-not $Script:function_result) {
        Write-Host "failed to configure $($libname)" -ForegroundColor Red
        return
    }

    $Script:function_result = cmake --build . --config release --target install

    if (-not $Script:function_result) {
        Write-Host "failed to build $($libname)" -ForegroundColor Red
    }
}
    
function build_sqlite3 {
    $libname = "sqlite3"
    make_builddir $libname
    $builddir = $Script:function_result
    cd $builddir

    $Script:function_result = cmake "$($root)/$($libname)" -G"$($Generator)" `
        -DCMAKE_INSTALL_PREFIX="$($builddir)/install"

    if (-not $Script:function_result) {
        Write-Host "failed to configure $($libname)" -ForegroundColor Red
        return
    }

    $Script:function_result = cmake --build . --config release --target install

    if (-not $Script:function_result) {
        Write-Host "failed to build $($libname)" -ForegroundColor Red
    }
}

function build_all {
    if ($Generator.Length -eq 0) {
        Write-Host "required parameter -Generator not provided" -ForegroundColor Red
        Write-Host "try 'cmake --help' for a list of generators"
        $Script:function_result = $false
        return
    }

    Write-Host "building irrlicht" -ForegroundColor Yellow
    build_irrlicht
    if (-not $Script:function_result) { return }

    Write-Host "building zlib" -ForegroundColor Yellow
    build_zlib
    if (-not $Script:function_result) { return }

    Write-Host "building ogg" -ForegroundColor Yellow
    build_ogg
    if (-not $Script:function_result) { return }

    Write-Host "building vorbis" -ForegroundColor Yellow
    build_vorbis
    if (-not $Script:function_result) { return }

    Write-Host "building openal" -ForegroundColor Yellow
    build_openal
    if (-not $Script:function_result) { return }

    Write-Host "building sqlite3" -ForegroundColor Yellow
    build_sqlite3
    if (-not $Script:function_result) { return }

    $Script:function_result = $true
}

Push-Location $root
build_all
Pop-Location

if (-not $Script:function_result) {
    Write-Host "build failed" -ForegroundColor Red
    exit 1
} else {
    Write-Host "build success" -ForegroundColor Green
    exit 0
}
