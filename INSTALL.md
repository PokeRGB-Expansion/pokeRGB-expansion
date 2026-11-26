# Build PokéRGB Expansion

The game builds with Git, GNU Make, a C17 compiler and RGBDS 1.0.4. RGBDS assembles the game and converts its graphics. To play a released version, follow the [patch instructions](README.md#play-a-release).

## Set up the tools

- **macOS.** Install Apple’s command line tools with `xcode-select --install` if needed. They include Git, Make and the compiler. Use the macOS download for RGBDS 1.0.4. If building RGBDS from source with Homebrew, the [project workflow](.github/workflows/main.yml) lists the required packages and Bison path.
- **Linux.** Install Git, GNU Make, and GCC or Clang. On Debian or Ubuntu, run `sudo apt update` and `sudo apt install git build-essential`. On openSUSE, use `sudo zypper install git make gcc`. On Arch, use `sudo pacman -S git make gcc`. Use the RGBDS 1.0.4 Linux download on x86-64, or build that version from source for your system.
- **Windows with WSL.** Install WSL and open its Linux terminal. Follow the Linux steps for your distribution. Build in your WSL home directory for faster access. To open that directory in Windows File Explorer, run `explorer.exe .` in WSL. [Install WSL](https://learn.microsoft.com/en-us/windows/wsl/install) · [Working with WSL files](https://learn.microsoft.com/en-us/windows/wsl/filesystems)
- **Windows with Cygwin.** In the Cygwin installer’s Select Packages screen, choose `git`, `make` and `gcc-core`. Extract the matching RGBDS 1.0.4 Windows archive. Add the directory with the four EXE files to your path, or pass its Cygwin path with `RGBDS` as shown below. Run the build in the Cygwin terminal. For older Windows versions, check which Cygwin installer supports your system. [Cygwin](https://www.cygwin.com/)
- **Android with Termux.** Install the build tools with `pkg install git make clang sed rgbds`. Check the installed version with `rgbasm --version`. If your package manager supplies a different version, build RGBDS 1.0.4 from source. [Termux package](https://github.com/termux/termux-packages/blob/master/packages/rgbds/build.sh)

Install all four RGBDS programs together. Run `rgbasm --version` to check the version on your path. If you keep the programs in another directory, use the local-tool option below. The RGBDS source build has additional dependencies, including libpng. [RGBDS 1.0.4 downloads and source](https://github.com/gbdev/rgbds/releases/tag/v1.0.4) · [RGBDS installation instructions](https://rgbds.gbdev.io/install)

## Build the game

```sh
git clone https://github.com/PokeRGB-Expansion/pokeRGB-expansion.git
cd pokeRGB-expansion
```

If your system provides only Clang, including a Termux setup without a `gcc` command, first run `make -C tools CC=clang` here. Then build all three Core games.

```sh
make -j4
```

Open `build/core/pokered.gbc`, `pokeblue.gbc` or `pokegreen.gbc` in a Game Boy emulator. Use `make -j4 PRESET=minimal` for all three Minimal games in `build/minimal/`. Add a color to build just that game, for example `make -j4 PRESET=minimal green`.

To use a local copy of RGBDS, pass the directory containing `rgbasm`, `rgblink`, `rgbfix` and `rgbgfx` with a trailing slash. For example, use `make -j4 RGBDS=/path/to/rgbds-1.0.4/`.

If you use GitHub CLI to open issues or pull requests, run `gh repo set-default --view` in your checkout. Set the project as the default with `gh repo set-default PokeRGB-Expansion/pokeRGB-expansion`, or choose your own fork if you intend to work there. [Make your first hack](README.md#make-your-first-hack)
