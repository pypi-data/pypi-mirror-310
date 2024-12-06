# `latexrestricted` — Python library for creating executables compatible with LaTeX restricted shell escape


This Python package is designed to simplify the process of creating Python
executables compatible with [LaTeX](https://www.latex-project.org/) restricted
shell escape.  Restricted shell escape allows LaTeX to run trusted executables
as part of compiling documents.  These executables have restricted access to
the file system and restricted ability to launch subprocesses.

`latexrestricted` provides access to LaTeX configuration and implements
wrappers around Python's
[`pathlib.Path`](https://docs.python.org/3/library/pathlib.html) and
[`subprocess.run()`](https://docs.python.org/3/library/subprocess.html#subprocess.run)
that follow LaTeX security settings.



## Usage considerations


### Importing

`latexrestricted` should be imported as soon as possible during the
initialization of an executable.  When it is imported, it sets the current
working directory as the TeX working directory.  If it is imported after the
current working directory is changed, then the TeX working directory will be
set incorrectly and security restrictions will fail.


### Failure modes on systems with multiple TeX installations

`latexrestricted` works correctly when used on systems with no more than one
[TeX Live](https://www.tug.org/texlive/) installation and no more than one
[MiKTeX](https://miktex.org/) installation.  If multiple TeX Live
installations or multiple MiKTeX installations are present, it is not always
possible for `latexrestricted` to determine the correct TeX Live or MiKTeX
installation, and in these cases the first installation on `PATH` is used.
**In these cases, `latexrestricted` may fail to return the correct TeX
configuration values, and there is no way to detect this.**  See
`LatexConfig._init_tex_paths()` for implementation details.

  * Multiple TeX Live installations:  The correct installation will be used
    under non-Windows operating systems.  Under Windows, the first
    installation on `PATH` is used.

  * Multiple MiKTeX installations:  Under all operating systems, the first
    installation on `PATH` is used.

The user can avoid any issues with multiple installations by modifying `PATH`
to put the correct TeX Live or MiKTeX installation first.



## LaTeX configuration

```
from latexrestricted import latex_config
```

The `latex_config` instance of the `LatexConfig` class provides access to
LaTeX configuration and related environment variables.  If there are errors in
determining LaTeX configuration (for example, a TeX installation cannot be
located), then `latexrestricted.LatexConfigError` is raised.


### `latex_config` attributes and properties

Paths:

* `tex_cwd: str`:  Current working directory when `latexrestricted` was
  first imported.

* `texlive_bin: str | None` and `texlive_kpsewhich: str | None`:  If an
  executable using `latexrestricted` is launched via `\ShellEscape` with TeX
  Live, these will be the paths to the TeX Live `bin/` directory and the TeX
  Live `kpsewhich` executable.  Otherwise, both are `None`.

  TeX Live is detected by the absence of a `TEXSYSTEM` environment variable,
  or by this variable having a value other than `miktex`.  Under non-Windows
  operating systems, the `SELFAUTOLOC` environment variable set by `kpathsea`
  is used to locate the TeX Live binary directory, so it will be correct even
  on systems with multiple TeX Live installations.  Under Windows, shell
  escape executables are often launched with TeX Live's executable wrapper
  `runscript.exe`, which overwrites `SELFAUTOLOC` with the location of the
  wrapper.  In this case, the TeX Live binary directory is located by using
  Python's `shutil.which()` to search `PATH` for a `tlmgr` executable with
  accompanying `kpsewhich`.  On systems with multiple TeX Live installations,
  this will give the first TeX Live installation on `PATH`, which is not
  guaranteed to be correct unless the user ensures that the correct
  installation has precedence on `PATH`.

* `miktex_bin: str | None`, `miktex_initexmf: str | None`, and
  `miktex_kpsewhich: str | None`:  If an executable using `latexrestricted`
  is launched via `\ShellEscape` with MiKTeX, these will be the paths to the
  MiKTeX `bin/` directory and the MiKTeX `initexmf` and `kpsewhich`
  executables.  Otherwise, all are `None`.

  MiKTeX is detected by checking the `TEXSYSTEM` environment variable for  the
  value `miktex`.  `TEXSYSTEM` only declares that MiKTeX is in use; unlike the
  TeX Live case with `SELFAUTOLOC`, `TEXSYSTEM` does not give the location of
  TeX binaries.  The location of TeX binaries is determined using Python's
  `shutil.which()` to search `PATH` for an `initexmf` executable with
  accompanying `kpsewhich`.  On systems with multiple MiKTeX installations,
  this will give the first MiKTeX installation on `PATH`, which is not
  guaranteed to be correct unless the user ensures that the correct
  installation has precedence on `PATH`.

File system access:

* `can_read_dotfiles: bool`, `can_read_anywhere: bool`,
  `can_write_dotfiles: bool`, `can_write_anywhere: bool`:  These summarize
  the file system security settings for TeX Live (`openin_any` and
  `openout_any` in `texmf.cnf`) and MiKTeX (`[Core]AllowUnsafeInputFiles`
  and `[Core]AllowUnsafeOutputFiles` in `miktex.ini`).  The `*dotfile`
  properties describe whether dotfiles (files with names beginning with `.`)
  can be read/written.  The `*anywhere` properties describe whether files
  anywhere in the file system can be read/written, or only those under the
  current working directory, `TEXMFOUTPUT`, and `TEXMF_OUTPUT_DIRECTORY`.

* `can_restricted_shell_escape: bool`:  This describes whether restricted
  shell escape is possible.  It is true when restricted shell escape is
  enabled and also when full shell escape is enabled.  It is based on TeX
  Live's `shell_escape` in `texmf.cnf` and MiKTeX's `[Core]ShellCommandMode`
  in `miktex.ini`.

* `prohibited_write_file_extensions: frozenset[str] | None`:  Under Windows
  (including Cygwin), this is a frozen set of file extensions that cannot be
  used in writing files.  Under other operating systems, this is `None`.

  All file extensions are lower case with a leading period (for example,
  `.exe`).  These are determined from the `PATHEXT` environment variable, or
  use a default fallback if `PATHEXT` is not defined or when under Cygwin.

Other LaTeX configuration variables and environment variables:

* `TEXMFHOME: str | None`:  Value of `TEXMFHOME` obtained from `kpsewhich`
  or `initexmf`.

* `TEXMFOUTPUT: str | None`:  Value of `TEXMFOUTPUT` obtained from environment
  variable if defined and otherwise from `kpsewhich` or `initexmf`.

* `TEXMF_OUTPUT_DIRECTORY: str | None`:  Value of `TEXMF_OUTPUT_DIRECTORY`
  obtained from environment variable.

* `restricted_shell_escape_commands: frozenset[str]`:  Permitted restricted
  shell escape executables.  Obtained from TeX Live's `shell_escape_commands`
  in `texmf.cnf` or MiKTeX's `[Core]AllowedShellCommands[]` in `miktex.ini`.

  Note that this will contain permitted restricted shell escape executables
  even when shell escape is completely disabled; it cannot be used to
  determine whether restricted shell escape is permitted.  See
  `can_restricted_shell_escape` to determine whether restricted shell escape
  is permitted.


### `latex_config` methods

* `kpsewhich_find_config_file(file: str)`:  Use `kpsewhich` in a subprocess
  to find a configuration file (`kpsewhich -f othertext <file>`).  Returns
  `kpsewhich` output as a string or `None` if there was no output.

* `kpsewhich_find_file(file: str, *, cache: bool = False)`:  Use `kpsewhich`
  in a subprocess to find a file (`kpsewhich <file>`).  Returns `kpsewhich`
  output as a string or `None` if there was no output.  The optional
  argument `cache` caches `kpsewhich` output to minimize subprocesses.  This
  can be useful when the file system is not being modified and `kpsewhich` is
  simply returning values from its own cache.



## Restricted file system access

TeX limits file system access.  The file system security settings for TeX Live
(`openin_any` and `openout_any` in `texmf.cnf`) and MiKTeX
(`[Core]AllowUnsafeInputFiles` and `[Core]AllowUnsafeOutputFiles` in
`miktex.ini`) determine whether dotfiles can be read/written and whether files
anywhere in the file system can be read/written, or only those under the
current working directory, `TEXMFOUTPUT`, and `TEXMF_OUTPUT_DIRECTORY`.

The `latexrestricted` package provides `RestrictedPath` subclasses of Python's
[`pathlib.Path`](https://docs.python.org/3/library/pathlib.html) that respect
these security settings or enforce more stringent security.  Under Python 3.8,
these subclasses backport the methods `.is_relative_to()` and `.with_stem()`
from Python 3.9.  When these subclasses are used to modify the file system,
`latexrestricted.PathSecurityError` is raised if reading/writing a given path
is not permitted.

**With `RestrictedPath` classes, relative paths are always relative to the TeX
working directory.**  If the current working directory has been changed to
another location (for example, via `os.chdir()`), then it will temporarily be
switched back to the TeX working directory during any `RestrictedPath`
operations that access the file system.

**The `SafeWrite*` classes should be preferred unless access to additional
write locations is absolutely necessary.**  When multiple TeX Live
installations are present under Windows or multiple MiKTeX installations are
present under all operating systems, there is no guarantee that
`latexrestricted` will find the correct installation and thus use the correct
TeX configuration, unless `PATH` has been modified to put the correct
installation first.

```
from latexrestricted import <RestrictedPathClass>
```

### `RestrictedPath` classes

#### `BaseRestrictedPath`

This is the base class for `RestrictedPath` classes.  It cannot be used
directly.  Subclasses define methods `.readable_dir()`, `.readable_file()`,
`.writable_dir()`, and `.writable_file()` that determine whether a given path
is readable/writable.  Most methods for opening, reading, writing, replacing,
and deleting files as well as methods for creating and deleting directories
are supported.  Methods related to modifying file permissions and creating
links are not supported.  Unsupported methods raise `NotImplementedError`.


#### `StringRestrictedPath` classes

* `StringRestrictedPath`:  This follows the approach taken in TeX's file
  system security.  TeX configuration determines whether dotfiles are
  readable/writable and which locations are readable/writable.  Paths are
  analyzed as strings; the file system is never consulted.  When read/write
  locations are restricted, paths are restricted using the following criteria:

  - All relative paths are relative to the TeX working directory.

  - All absolute paths must be under `TEXMF_OUTPUT_DIRECTORY` and
    `TEXMFOUTPUT`.

  - Paths cannot contain `..` to access a parent directory, even if the
    parent directory is a valid location.

  When read/write locations are restricted, it is still possible to access
  locations outside the TeX working directory, `TEXMF_OUTPUT_DIRECTORY`, and
  `TEXMFOUTPUT` if there are symlinks in those locations.

  Under Windows (including Cygwin), writing files with file extensions in
  `PATHEXT` (for example, `.exe`) is also disabled.

* `SafeStringRestrictedPath`:  Same as `StringRestrictedPath`, except that TeX
  configuration is ignored and all security settings are at maximum:  dotfiles
  cannot be read/written, and all reading/writing is limited to the TeX
  working directory, `TEXMF_OUTPUT_DIRECTORY`, and `TEXMFOUTPUT`.

* `SafeWriteStringRestrictedPath`:  Same as `StringRestrictedPath`, except
  that TeX configuration for writing is ignored and all security settings
  related to writing are at maximum.


#### `ResolvedRestrictedPath` classes

* `ResolvedRestrictedPath`:  This resolves any symlinks in paths using the
  file system before determining whether paths are readable/writable.  TeX
  configuration determines whether dotfiles are readable/writable and which
  locations are readable/writable.  When read/write locations are restricted,
  paths are restricted using the following criteria:

  - Resolved paths must be under the TeX working directory,
    resolved `TEXMF_OUTPUT_DIRECTORY`, or resolved `TEXMFOUTPUT`.

  - All relative paths are resolved relative to the TeX working directory.

  - Unlike `StringRestrictedPath`, paths are allowed to contain `..`, and
    `TEXMF_OUTPUT_DIRECTORY` and `TEXMFOUTPUT` can be accessed via relative
    paths.  This is possible since paths are fully resolved with the file
    system before being compared with permitted read/write locations.

  Because paths are resolved before being compared with permitted read/write
  locations, it is not possible to access locations outside the TeX working
  directory, `TEXMF_OUTPUT_DIRECTORY`, and `TEXMFOUTPUT` via symlinks in
  those locations.

  Under Windows (including Cygwin), writing files with file extensions in
  `PATHEXT` (for example, `.exe`) is also disabled.

* `SafeResolvedRestrictedPath`:  Same as `ResolvedRestrictedPath`,  except
  that TeX configuration is ignored and all security settings are at maximum:
  dotfiles cannot be read/written, and all other reading/writing is limited to
  the TeX working directory, `TEXMF_OUTPUT_DIRECTORY`, and `TEXMFOUTPUT`.

* `SafeWriteResolvedRestrictedPath`:  Same as `ResolvedRestrictedPath`, except
  that TeX configuration for writing is ignored and all security settings
  related to writing are at maximum.


#### `RestrictedPath` class methods

* `tex_cwd() -> Self`:  TeX working directory.

* `TEXMFOUTPUT() -> Self | None`:  Path of `TEXMFOUTPUT` from LaTeX
  configuration or environment variable, or `None` if not defined.

* `TEXMF_OUTPUT_DIRECTORY() -> Self | None`:  Path of `TEXMF_OUTPUT_DIRECTORY`
  from environment variable, or `None` if not defined.

* `tex_roots() -> frozenset[Self]`:  All root locations where TeX might write
  output, under default configuration with restricted access to the file
  system.  This includes `tex_cwd()` plus `TEXMFOUTPUT()` and
  `TEXMF_OUTPUT_DIRECTORY()` if they are defined.

* `tex_roots_resolved() -> frozenset[Self]`:  Same as `tex_roots()` except
  all paths are resolved with the file system.

* `tex_roots_with_resolved() -> frozenset[Self]`:  Union of `tex_roots()` and
  `tex_roots_resolved()`.

* `tex_openout_roots() -> tuple[Self]`:  Locations where TeX will attempt to
  write with `\openout`, in order.  The first element of the tuple is
  `TEXMF_OUTPUT_DIRECTORY()` if not `None` and otherwise `tex_cwd()`.  If
  `TEXMFOUTPUT()` is not `None` and is not already in the tuple, then it is
  the second element.

  TeX attempts to write to `TEXMFOUTPUT` (if defined) when the default write
  location (`TEXMF_OUTPUT_DIRECTORY` if defined, else TeX working directory)
  is read-only.

* `tex_texmfoutput_roots() -> frozenset[Self]`:  `TEXMFOUTPUT()` and/or
  `TEXMF_OUTPUT_DIRECTORY()` if they are defined.


## Restricted subprocesses

When LaTeX runs with restricted shell escape, only executables specified in
TeX configuration can be executed via `\ShellEscape`.  The `latexrestricted`
package allows these same executables to run in subprocesses via
`restricted_run()`.  This is a wrapper around Python's
[`subprocess.run()`](https://docs.python.org/3/library/subprocess.html#subprocess.run).

```
from latexrestricted import restricted_run
restricted_run(args: list[str], allow_restricted_executables: bool = False)
```

* It is *always* possible to run `kpsewhich` (including `miktex-kpsewhich`)
  and `initexmf`.  These are necessary to access TeX configuration values.

  Running other executables allowed by TeX configuration for restricted shell
  escape requires the optional argument `allow_restricted_executables=True`.
  In this case, TeX configuration is checked to determine whether restricted
  shell escape is enabled, although this should be redundant if
  `latexrestricted` itself is being used in a restricted shell escape
  executable.

* When `allow_restricted_executables=True`, the executable must be in the same
  directory as `kpsewhich` or `initexmf`, as previously located during TeX
  configuration detection, or the executable must exist on `PATH`, as found by
  Python's `shutil.which()`.

  The executable must not be in a location writable by LaTeX.  For added
  security, locations writable by LaTeX cannot be under the executable parent
  directory.

* The executable cannot be a batch file (no `*.bat` or `*.cmd`):
  https://docs.python.org/3/library/subprocess.html#security-considerations.
  This is enforced by requiring `*.exe` under Windows and completely
  prohibiting `*.bat` and `*.cmd` everywhere.

* The subprocess runs with `shell=False`.

`restricted_run()` will raise `latexrestricted.ExecutableNotFoundError` if an
executable (`args[0]`) cannot be found in the same directory as `kpsewhich` or
`initexmf`, or on `PATH`.  It will raise
`latexrestricted.UnapprovedExecutableError` when the executable is not in the
approved list of executables from LaTeX configuration
(`latex_config.restricted_shell_escape_commands`).  It will raise
`latexrestricted.ExecutablePathSecurityError` if the executable is found and
is in the approved list, but is in an insecure location relative to locations
writable by LaTeX.



## Security limitations with TeX Live and `TEXMFOUTPUT`

TeX Live allows `TEXMFOUTPUT` to be set in a `texmf.cnf` config file.  In this
case, `latexrestricted` will retrieve the value of `TEXMFOUTPUT` by running
`kpsewhich --var-value TEXMFOUTPUT` in a subprocess.  If the user has modified
`TEXMFOUTPUT` to an unsafe value in a `texmf.cnf` config file, then the
`kpsewhich` executable (and all other TeX-related executables) are potentially
compromised, and `latexrestricted` cannot detect this until *after* running
`kpsewhich`.

It is possible to set `TEXMFOUTPUT` to unsafe values in a `texmf.cnf` config
file.  For example, if `TEXMFOUTPUT` is set to a location in the file system
that contains executables, this could allow LaTeX documents to modify those
executables or their resources.  With TeX Live, `latexrestricted` retrieves
the value of `TEXMFOUTPUT` by running `kpsewhich`.  However, the `kpsewhich`
executable itself could be compromised if `TEXMFOUTPUT` is set to a directory
that contains the `kpsewhich` executable (or other parts of a TeX
installation).  If `latexrestricted` detects an unsafe value of `TEXMFOUTPUT`,
it raises `latexrestricted.LatexConfigError`, but this is only possible
*after* running the potentially compromised `kpsewhich` executable to obtain
the value of `TEXMFOUTPUT`.  (And if `kpsewhich` is compromised, there is
always the possibility that it will not return the true value of
`TEXMFOUTPUT`.)

While raising a security-related error after running the potentially
compromised executable is not ideal, this will typically have a negligible
impact on overall security.  If `TEXMFOUTPUT` is set to a directory that
contains the `kpsewhich` executable (or other parts of a TeX installation),
then all other TeX-related executables are also potentially compromised.  If
`latexrestricted` is being used in a Python executable designed for LaTeX
shell escape, then presumably a LaTeX executable is already running, and LaTeX
may invoke additional trusted executables such as `kpsewhich` in shells.
Thus, before `latexrestricted` ever runs `kpsewhich` to retrieve the value of
`TEXMFOUTPUT`, potentially compromised executables would already be running.
