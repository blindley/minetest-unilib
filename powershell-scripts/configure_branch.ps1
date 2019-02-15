param(
    [String]$Branch = "",
    [String]$Generator = "",
    [String]$Destination = ""
)

if ($generator.Length -eq 0) {
    Write-Host "-Generator parameter required but not provided" -ForegroundColor Red
    Write-Host "use cmake --help for a list of valid generators"
    exit 1
}

if ($branch.Length -eq 0) {
    Write-Host "-Branch parameter required but not provided" -ForegroundColor Red
    Write-Host "provide the path to a directory with a minetest repository"
    exit 1
}

if (-not (Test-Path $Branch)) {
    Write-Host "$($Branch) is not a valid path"
    exit 1
}

$branch = Resolve-Path $Branch

if ($Destination.Length -eq 0) {
    $Script:destination = Resolve-Path .
} else {
    mkdir $Script:destination -Force | Out-Null
    if (-not (Test-Path $Script:destination)) {
        Write-Host "unable to make directory $($Script:destination)" -ForegroundColor Red
        exit 1
    }

    $Script:destination = Resolve-Path $Script:destination
}

$gen_nospaces = $Generator -replace " ","-"
$unilib_root = Resolve-Path "$($PSScriptRoot)/.."
$libdir = "$($unilib_root)/build/$($gen_nospaces)"

$Script:function_result = $true

function configure {
    cmake $Script:branch -G"$($Script:generator)" `
        -DCMAKE_INSTALL_PREFIX="$(Resolve-Path .)/install" `
        -DBUILD_CLIENT=1 -DBUILD_SERVER=0 `
        `
        -DENABLE_SOUND=1 `
        -DENABLE_CURL=0 `
        -DENABLE_GETTEXT=0 `
        -DENABLE_FREETYPE=0 `
        -DENABLE_LEVELDB=0 `
        `
        -DIRRLICHT_INCLUDE_DIR="$($libdir)/irrlicht/install/includes/Irrlicht" `
        -DIRRLICHT_LIBRARY="$($libdir)/irrlicht/install/lib/irrlicht.lib" `
        -DIRRLICHT_DLL="$($libdir)/irrlicht/install/bin/irrlicht.dll" `
        `
        -DZLIB_INCLUDE_DIR="$($libdir)/zlib/install/include" `
        -DZLIB_LIBRARIES="$($libdir)/zlib/install/lib/zlib.lib" `
        -DZLIB_DLL="$($libdir)/zlib/install/bin/zlib.dll" `
        `
        -DOGG_INCLUDE_DIR="$($libdir)/ogg/install/include" `
        -DOGG_LIBRARY="$($libdir)/ogg/install/lib/ogg.lib" `
        -DOGG_DLL="$($libdir)/ogg/install/bin/ogg.dll" `
        `
        -DVORBIS_INCLUDE_DIR="$($libdir)/vorbis/install/include" `
        -DVORBIS_LIBRARY="$($libdir)/vorbis/install/lib/vorbis.lib" `
        -DVORBIS_DLL="$($libdir)/vorbis/install/bin/vorbis.dll" `
        -DVORBISFILE_LIBRARY="$($libdir)/vorbis/install/lib/vorbisfile.lib" `
        -DVORBISFILE_DLL="$($libdir)/vorbis/install/bin/vorbisfile.dll" `
        `
        -DOPENAL_INCLUDE_DIR="$($libdir)/openal/install/include/AL" `
        -DOPENAL_LIBRARY="$($libdir)/openal/install/lib/OpenAL32.lib" `
        -DOPENAL_DLL="$($libdir)/openal/install/bin/OpenAL32.dll" `
        `
        -DSQLITE3_INCLUDE_DIR="$($libdir)/sqlite3/install/include/sqlite3" `
        -DSQLITE3_LIBRARY="$($libdir)/sqlite3/install/lib/sqlite3.lib" `
        #

    $Script:function_result = $?
}

Push-Location $Script:destination
configure
Pop-Location

if ($Script:function_result) {
    Write-Host "configure successful" -ForegroundColor Green
    exit 0
} else {
    Write-Host "configure unsuccessful" -ForegroundColor Red
    exit 1
}