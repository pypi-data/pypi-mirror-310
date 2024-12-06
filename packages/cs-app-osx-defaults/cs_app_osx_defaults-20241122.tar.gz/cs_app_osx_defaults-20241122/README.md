Access the MacOS defaults via the `defaults` command.

*Latest release 20241122*:
run: drop quiet=False parameter, the run() inside defaults() will pick things up.

## <a name="Defaults"></a>Class `Defaults`

A view of the defaults.

*`Defaults.domains`*:
Return a list of the domains present in the defaults.

*`Defaults.run(self, argv, doit=True) -> str`*:
Run a `defaults` subcommand, return the output decoded from UTF-8.

## <a name="defaults"></a>`defaults(argv, *, host=None, doit=True, **subp)`

Run the `defaults` command with the arguments `argv`.
If the optional `host` parameter is supplied,
a value of `'.'` uses the `-currentHost` option
and other values are used with the `-host` option.
Return the `CompletedProcess` result or `None` if `doit` is false.

## <a name="DomainDefaults"></a>Class `DomainDefaults`

A view of the defaults for a particular domain.

*`DomainDefaults.as_dict(self)`*:
Return the current defaults as a `dict`.

*`DomainDefaults.flush(self)`*:
Forget any cached information.

# Release Log



*Release 20241122*:
run: drop quiet=False parameter, the run() inside defaults() will pick things up.

*Release 20240316*:
Fixed release upload artifacts.

*Release 20240201*:
Initial PyPI release.
