"""Top-level namespace package for Mallku source tree.

This empty file allows modules to be imported as

    import src.mallku ...

which several existing tests and internal modules rely on.

We intentionally keep this file minimal; the real implementation
lives in ``src/mallku``.  Adding the file avoids ``ModuleNotFoundError``
when the repository is executed directly (without installing the
package), because Python only recognises a directory as a package
when it contains an ``__init__.py`` or is declared as a namespace
package.  Here we use the conventional implicit namespace approach
provided by the presence of this file.
"""

# The file is intentionally blank beyond the docstring.
