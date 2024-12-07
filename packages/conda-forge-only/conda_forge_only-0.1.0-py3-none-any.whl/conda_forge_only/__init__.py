"""Package initializer."""

try:
    from conda_forge_only.version import version as __version__  # noqa
except ModuleNotFoundError:  # pragma: no cover
    raise ModuleNotFoundError(
        "No module named conda_forge_only.version. This could mean "
        "you didn't install 'conda_forge_only' properly. Try reinstalling ('pip "
        "install').")
