
import click
import json
from doppel.reporters import SimpleReporter


def _log_info(msg):
    print(msg)


class PackageAPI():
    """
    This class is used to hold the interface of a given package
    being analyzed by doppel. It's comparison operators enable comparison
    between interfaces and its standard JSON format allows this comparison
    to happen across programming languages.
    """

    def __init__(self, pkg_dict):

        self._validate_pkg(pkg_dict)
        self.pkg_dict = pkg_dict
        pass

    @classmethod
    def from_json(cls, filename):
        """
        Instantiate a Package object from a file.
        """
        _log_info("Creating package from {}".format(filename))

        # read in output of "analyze.*" script
        with open(filename, 'r') as f:
            pkg_dict = json.loads(f.read())

        # validate
        return cls(pkg_dict)

    def _validate_pkg(self, pkg_dict):

        assert isinstance(pkg_dict, dict)
        assert pkg_dict['language'] is not None
        assert pkg_dict['functions'] is not None
        assert pkg_dict['classes'] is not None

        return

    def num_functions(self):
        return(len(self.pkg_dict['functions'].keys()))

    def num_classes(self):
        return(len(self.pkg_dict['classes'].keys()))


@click.command()
@click.option(
    '--files', '-f',
    help="Comma-delimited list of doppel output files."
)
def main(files):
    """
    doppel is a a continuous integration tool for testing
    the continuity of APIs for libraries implemented in
    different languages.
    """
    print("Loading comparison files")

    f_list = files.split(',')

    # Check if these are legit package objects
    pkgs = [PackageAPI.from_json(f) for f in f_list]

    # Report
    reporter = SimpleReporter(pkgs)
    reporter.compare()


if __name__ == "__main__":
    main()
