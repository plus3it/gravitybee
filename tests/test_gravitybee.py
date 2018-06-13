# test_gravitybee.py

import pytest
import glob
import os
import json

from subprocess import check_output

from gravitybee import Arguments, PackageGenerator, EXIT_OKAY, FILE_DIR

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

    sha_filename = pg.args.sha_format.format(
        an=pg.args.app_name,
        v=pg.args.app_version,
        os=pg.args.operating_system,
        m=pg.args.machine_type
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

    assert generated_okay == EXIT_OKAY \
        and not os.path.exists(PackageGenerator.INFO_FILE) \
        and not os.path.exists(PackageGenerator.FILES_FILE) \
        and not os.path.exists(PackageGenerator.ENVIRON_SCRIPT \
            + PackageGenerator.ENVIRON_SCRIPT_POSIX_EXT) \
        and not os.path.exists(PackageGenerator.ENVIRON_SCRIPT \
            + PackageGenerator.ENVIRON_SCRIPT_WIN_EXT) \
        and os.path.exists(pg.sha_file_w_path) # should be created even if no_file flag

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
        files = glob.glob(os.path.join(
            pg.args.staging_dir,
            pg.args.app_version,
            'gbtestapp-4.2.6-standalone*'
        ))

        cmd_output = check_output(files[0], universal_newlines=True)
        compare_file = open(os.path.join("tests", "gbtestapp", "correct_stdout.txt"),"rU").read()

        assert cmd_output == compare_file
    else:
        assert False

def test_filename_file(arguments):
    """ Tests whether GravityBee writes name of standalone app in gravitybee-files.json. """
    pg = PackageGenerator(arguments)
    generated_okay = pg.generate()
    if generated_okay == EXIT_OKAY:
        sa_file = open(
            os.path.join(
                FILE_DIR,
                "gravitybee-files.json"
            ), "r"
        )
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

        sha_file = open(pg.sha_file_w_path, "r")
        sha_dict = json.loads(sha_file.read())
        sha_file.close()

        assert info['file_sha'] \
            == PackageGenerator.get_hash(info['gen_file_w_path']) \
            == sha_dict[info['gen_file']]
    else:
        assert False

@pytest.fixture
def latest_arguments():
    """Returns an Arguments instance using the included app"""
    return Arguments(
        src_dir="src",
        extra_data=["gbextradata"],
        verbose=True,
        pkg_dir=os.path.join("tests", "gbtestapp"),
        sha=Arguments.OPTION_SHA_FILE,
        clean=True,
        with_latest=True
    )

def test_latest(latest_arguments):
    """
    Checks to make sure the latest directory is created and
    populated with standalone executable and SHA.
    """

    
    pg = PackageGenerator(latest_arguments)
    generated_okay = pg.generate()

    if generated_okay == EXIT_OKAY:

        latest_standalone = pg.args.name_format.format(
            an=pg.args.app_name,
            v='latest',
            os=pg.args.operating_system,
            m=pg.args.machine_type
        )

        sa_files = glob.glob(os.path.join(
            pg.args.staging_dir,
            'latest',
            latest_standalone + '*'
        ))
        
        sha_file = pg.args.sha_format.format(
            an=pg.args.app_name,
            v='latest',
            os=pg.args.operating_system,
            m=pg.args.machine_type
        )

        sha_files = glob.glob(os.path.join(
            pg.args.staging_dir,
            'latest',
            sha_file
        ))

        assert os.path.isdir(os.path.join(pg.args.staging_dir, 'latest')) \
            and len(sa_files) > 0 \
            and len(sha_files) > 0
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

def test_sha_format(defaults):
    assert defaults.sha_format == '{an}-{v}-sha256-{os}-{m}.json'    

def test_extra_data(defaults):
    assert defaults.extra_data is None

def test_work_dir(defaults):
    assert defaults.work_dir[:17] == os.path.join(FILE_DIR, 'build')[:17]

def test_console_script(defaults):
    assert defaults.console_script == 'gbtestapp'

def test_app_version(defaults):
    assert defaults.app_version == '4.2.6'

def test_app_name(defaults):
    assert defaults.app_name == 'gbtestapp'

def test_pkg_name(defaults):
    assert defaults.pkg_name == 'gbtestapp'