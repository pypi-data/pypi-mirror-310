# Changelog — `latexrestricted` Python package


## v0.6.2 (2024-11-24)

*  Fixed version and CHANGELOG from v0.6.1.



## v0.6.1 (2024-11-24)

*  `pyproject.toml`:  explicitly set `build-backend` (#1).

*  Restricted subprocesses now always support the `miktex-kpsewhich`
   executable in addition to `kpsewhich`.



## v0.6.0 (2024-10-29)

*  Added support for `miktex-kpsewhich` executable for MiKTeX compatibility
   under macOS (gpoore/minted#401).

*  Reorganized logic in `ResolvedRestrictedPath` to improve performance.
   Methods `can_read_anywhere()`, `can_read_dotfiles()`,
   `can_write_anywhere()`, and `can_write_dotfiles()` are no longer called
   for non-dotfiles in locations that are always readable/writable by TeX.
   This eliminates the overhead of getting read/write security settings from
   `kpsewhich` or `initexmf`.



## v0.5.0 (2024-10-16)

*  Switched from `platform.system()` to `sys.platform` for better performance
   in detecting operating system.

   Performance reference:  https://github.com/python/cpython/issues/95531.



## v0.4.0 (2024-08-16)

* Under Windows with TeX Live, the `SELFAUTOLOC` environment variable is no
  longer used to locate `kpsewhich`.  Under these conditions, a shell escape
  executable will often be launched with TeX Live's executable wrapper
  `runscript.exe`.  This uses `kpathsea` internally, which overwrites
  `SELFAUTOLOC` so that it refers to the location of the executable wrapper,
  not the location of the TeX executable that initially invoked shell escape.
  Under these conditions, `kpsewhich` is now located by searching path with
  Python's `shutil.which()` for a `tlmgr` executable with accompanying
  `kpsewhich`, and there is no way to guarantee that the correct `kpsewhich`
  is used on systems with multiple TeX Live installations.



## v0.3.0 (2024-08-11)

*  Fixed `__slots__` bug in `AnyPath`.

*  Replaced all `$TEXMF*` with `TEXMF*` in error messages and documentation
   for better consistency.



## v0.2.0 (2024-08-10)

*  Added check for unsafe `TEXMFOUTPUT` value in TeX Live config.



## v0.1.0 (2024-07-27)

*  Initial release.
