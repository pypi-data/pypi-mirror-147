"""Extensions for virtualenv Seeders to pre-install keyring-subprocess."""
import abc
from virtualenv.seed.wheels import Version
from virtualenv.seed.embed.via_app_data.via_app_data import FromAppData

VERSION = Version.bundle


def _get_embed_wheel(distribution, for_py_version):
    from virtualenv.seed.wheels.embed import BUNDLE_SUPPORT, BUNDLE_FOLDER, MAX
    from virtualenv.seed.wheels.util import Wheel

    wheels = BUNDLE_SUPPORT.get(for_py_version, {}) or BUNDLE_SUPPORT[MAX]
    wheel = wheels.get(distribution)

    if wheel is None:
        return None

    return Wheel.from_path(BUNDLE_FOLDER / wheel)


class MetaClass(abc.ABCMeta):
    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        if not hasattr(cls, "_count"):
            cls._count = 0
        if not hasattr(cls, "_inside_add_parser_arguments"):
            cls._inside_add_parser_arguments = False


class KeyringSubprocessFromAppData(FromAppData, metaclass=MetaClass):
    """Mixed in keyring-subprocess into seed packages for app-data seeder."""

    def __init__(self, options):
        """Add the extra attributes for the extensions."""
        self.keyring_subprocess_version = options.keyring_subprocess
        self.no_keyring_subprocess = options.no_keyring_subprocess

        super(KeyringSubprocessFromAppData, self).__init__(options)

        import virtualenv.seed.wheels.bundle as bundle

        bundle.get_embed_wheel = _get_embed_wheel

    @classmethod
    def distributions(cls):
        """Return the dictionary of distributions."""
        base = super(KeyringSubprocessFromAppData, cls).distributions()

        if cls._inside_add_parser_arguments and cls._count < 2:
            cls._count += 1
            base["keyring-subprocess"] = VERSION

        return base

    @classmethod
    def add_parser_arguments(cls, parser, interpreter, app_data):
        cls._inside_add_parser_arguments = True

        super(KeyringSubprocessFromAppData, cls).add_parser_arguments(
            parser, interpreter, app_data
        )

        cls._inside_add_parser_arguments = False

        parser.add_argument(
            "--keyring-subprocess",
            dest="keyring_subprocess",
            metavar="version",
            help="version of keyring-subprocess to install as seed: embed, bundle or exact version",
            default=VERSION,
        )
        parser.add_argument(
            "--no-keyring-subprocess",
            dest="no_keyring_subprocess",
            action="store_true",
            help="do not install keyring-subprocess",
            default=False,
        )

    def distribution_to_versions(self):
        base = super(KeyringSubprocessFromAppData, self).distribution_to_versions()
        if not self.no_keyring_subprocess:
            base["keyring_subprocess"] = VERSION
        return base

    def __unicode__(self):
        base = super(FromAppData, self).__unicode__()
        msg = ", keyring_subprocess_version={}, no_keyring_subprocess={}".format(
            self.keyring_subprocess_version,
            self.no_keyring_subprocess,
        )
        return base[:-1] + msg + base[-1]
