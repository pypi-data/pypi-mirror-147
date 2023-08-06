# keyring-subprocess
A dependency keyring backend that queries an executable `keyring` which can be
found on PATH.

## Pros
- Zero dependencies for a clean `pip list` command and should always be
  compatible with the rest of your dependencies. Which makes it more
  suitable to be added to `PYTHONPATH` after installing with Pip's
  `--target` flag.
- Has [keyring](https://pypi.org/project/keyring) and the minimal required
  dependencies vendored to make the `chainer` and `null` backends work.
  - It uses the ModuleSpec apis provided by [PEP451](https://peps.python.org/pep-0451/)
    to make the vendored `keyring` importable.
- Provides a `virtualenv` [Seeder](https://virtualenv.pypa.io/en/latest/user_guide.html#seeders)
  named `keyring-subprocess`.

## Cons
- It does require `keyring-subprocess` to be installed in the virtual
  environment associated with the `keyring` executable that is found.
- Adds or replaces points of failures depending on how you look at it.
- Being able to import `keyring`, `importlib_metadata` and `zipp` but
  `pip list` not listing them might be confusing and not very helpful during
  debugging.
