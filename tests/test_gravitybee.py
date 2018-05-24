# test_gravitybee.py

import pytest
import glob
import os
import json

from subprocess import check_output

from gravitybee import Arguments, PackageGenerator, EXIT_OKAY

# should be first so that other tests haven't created files
def test_no_output():
    """Makes sure that when no output flag is on, no files are created."""
    args = Arguments(
        src_dir="src",
        extra_data=["gbextradata"],
        verbose=True,
        pkg_dir=os.path.join("tests", "gbtestapp"),
        clean=True,
        no_file=True
    )
    pg = PackageGenerator(args)
    generated_okay = pg.generate()

    sha_filename = PackageGenerator.SHA_FILENAME.format(
        an=pg.args.app_name,
        v=pg.args.app_version
    )

    assert generated_okay == EXIT_OKAY \
        and not os.path.exists(PackageGenerator.INFO_FILE) \
        and not os.path.exists(PackageGenerator.FILES_FILE) \
        and not os.path.exists(PackageGenerator.ENVIRON_SCRIPT \
            + PackageGenerator.ENVIRON_SCRIPT_POSIX_EXT) \
        and not os.path.exists(PackageGenerator.ENVIRON_SCRIPT \
            + PackageGenerator.ENVIRON_SCRIPT_WIN_EXT) \
        and not os.path.exists(sha_filename)

# should be second so there are still not output files
def test_no_output_but_sha():
    """Makes sure that when no output flag is on, no files are created."""
    args = Arguments(
        src_dir="src",
        extra_data=["gbextradata"],
        verbose=True,
        pkg_dir=os.path.join("tests", "gbtestapp"),
        sha=Arguments.OPTION_SHA_FILE,
        clean=True,
        no_file=True
    )
    pg = PackageGenerator(args)
    generated_okay = pg.generate()

    sha_filename = PackageGenerator.SHA_FILENAME.format(
        an=pg.args.app_name,
        v=pg.args.app_version
    )

    assert generated_okay == EXIT_OKAY \
        and not os.path.exists(PackageGenerator.INFO_FILE) \
        and not os.path.exists(PackageGenerator.FILES_FILE) \
        and not os.path.exists(PackageGenerator.ENVIRON_SCRIPT \
            + PackageGenerator.ENVIRON_SCRIPT_POSIX_EXT) \
        and not os.path.exists(PackageGenerator.ENVIRON_SCRIPT \
            + PackageGenerator.ENVIRON_SCRIPT_WIN_EXT) \
        and os.path.exists(sha_filename) # should be created even if no_file flag

@pytest.fixture
def arguments():
    """Returns an Arguments instance using the included app"""
    return Arguments(
        src_dir="src",
        extra_data=["gbextradata"],
        verbose=True,
        pkg_dir=os.path.join("tests", "gbtestapp"),
        sha=Arguments.OPTION_SHA_FILE,
        clean=True
    )

def test_generation(arguments):
    """ Tests running the executable. """
    pg = PackageGenerator(arguments)
    generated_okay = pg.generate()

    assert generated_okay == EXIT_OKAY

def test_executable(arguments):
    """ Tests running the executable. """
    pg = PackageGenerator(arguments)
    generated_okay = pg.generate()
    if generated_okay == EXIT_OKAY:
        files = glob.glob('gbtestapp-4.2.6-standalone*')

        cmd_output = check_output(os.path.join('.',files[0]))
        compare_file = open(os.path.join("tests", "gbtestapp", "correct_stdout.txt"),"rb").read()

        assert cmd_output == compare_file
    else:
        assert False

def test_filename_file(arguments):
    """ Tests whether GravityBee writes name of standalone app in gravitybee-files.json. """
    pg = PackageGenerator(arguments)
    generated_okay = pg.generate()
    if generated_okay == EXIT_OKAY:
        sa_file = open("gravitybee-files.json", "r")
        gb_files = json.loads(sa_file.read())
        sa_file.close

        assert gb_files[0]['filename'].startswith("gbtestapp-4.2.6-standalone")
    else:
        assert False

def test_file_sha(arguments):
    """
    Checks the generated sha hash written to file with one that is
    freshly calculated. Also checks that info file exists and has the
    correct app name and version.
    """

    # get the sha256 hash from the json file    
    pg = PackageGenerator(arguments)
    generated_okay = pg.generate()
    if generated_okay == EXIT_OKAY:
        # get the info from info file
        info_file = open(PackageGenerator.INFO_FILE, "r")
        info = json.loads(info_file.read())
        info_file.close()

        sha_filename = PackageGenerator.SHA_FILENAME.format(
            an=info['app_name'],
            v=info['app_version']
        )
        sha_file = open(sha_filename, "r")
        sha_dict = json.loads(sha_file.read())
        sha_file.close()

        assert info['file_sha'] \
            == PackageGenerator.get_hash(info['created_path']) \
            == sha_dict[info['created_file']]
    else:
        assert False


@pytest.fixture
def defaults():
    if not os.getcwd().endswith(os.path.join("tests", "gbtestapp")):
        os.chdir(os.path.join("tests", "gbtestapp"))
    return Arguments()

def test_clean(defaults):
    assert not defaults.clean

def test_pkg_dir(defaults):
    assert defaults.pkg_dir == '.'

def test_src_dir(defaults):
    assert defaults.src_dir == '.'

def test_name_format(defaults):
    assert defaults.name_format == '{an}-{v}-standalone-{os}-{m}'

def test_extra_data(defaults):
    assert defaults.extra_data is None

def test_work_dir(defaults):
    assert defaults.work_dir[:11] == 'gb_workdir_'

def test_console_script(defaults):
    assert defaults.console_script == 'gbtestapp'

def test_app_version(defaults):
    assert defaults.app_version == '4.2.6'

def test_app_name(defaults):
    assert defaults.app_name == 'gbtestapp'

def test_pkg_name(defaults):
    assert defaults.pkg_name == 'gbtestapp'