Changelogs
===========

A list of changelogs for TADR, with the most recent version first. These are also available `here <https://github.com/MurdoMaclachlan/tadr/releases>`_.

Unreleased
----------

2.0.1
-----

As of this version, setuptools 57.0.0+ and PyGObject 3.42+ are now explicitly required, having been implicit requirements before.

- Moved Notify to the Logger, allowing easy catching of any errors originating from GLib. (@MurdoMaclachlan)
- Switched to detecting u/transcribersofreddit's new failure message. (@MurdoMaclachlan)
- Changed functions marked to NoReturn to return None instead, as per Python's type-hinting specifications. (@MurdoMaclachlan)
- Changed camelCase variable names to snake_case. (@MurdoMaclachlan)
- Changed docstrings to better reflect standards. (@MurdoMaclachlan)
- Fixed alphabetical order of methods in the Logger. (@MurdoMaclachlan)

2.0.0
-----

**Functionality**

- Added and enforced refresh token authentication.
- Refactored Logger.

**Cleanup/Optimisation**

- Optimised ``Static.define_paths()``.
- General optimisations for the rest of the program.

**Dependencies**

- Removed colored.
- Updated praw to 7.5.0.

**Documentation/Logs**

- Added docstrings.
- Updated readthedocs documentation.
- Changed name of ``core`` folder to ``tadrcore`` so pip installation doesn't explode. (#3)

1.0.2
-----

**Cleanup/Optimisation**:

- General small cleanup and readability improvements.

**Bug Fixes**:

- #1: Import error: cannot import ``getTime()`` (fixed in #2).

1.0.1
-----

**Documentation**:

- TADR now logs a full link to messages it replies to, allowing them to be opened by clicking on them in many consoles.

1.0.0
-----

**Meta**:

- Created PIP package, GitHub repository and readthedocs hosting.

**Functionality**:

- Created initial program.
