# -*- coding: utf-8 -*-
# pylint: disable=redefined-outer-name
"""test_gravitybee module."""
import glob
import os
import json
from pathlib import Path

from subprocess import check_output
import platform

import pytest
from gravitybee import Arguments, PackageGenerator, EXIT_OKAY, FILE_DIR


def test_no_output():
    """Makes sure that when no output flag is on, no files are created.
        Should be run first so that other tests haven't created files"""
    args = Arguments(
        src_dir="src",
        extra_data=["gbextradata"],
        pkg_dir=os.path.join("tests", "gbtestapp"),
        clean=True,
        no_file=True
    )
    package_generator = PackageGenerator(args)
    generated_okay = package_generator.generate()

    sha_filename = package_generator.args.formats["sha"].format(
        an=package_generator.args.info['app_name'],
        v=package_generator.args.info['app_version'],
        os=package_generator.args.info['operating_system'],
        m=package_generator.args.info['machine_type']
    )

    assert generated_okay == EXIT_OKAY \
        and not os.path.exists(PackageGenerator.INFO_FILE) \
        and not os.path.exists(PackageGenerator.FILES_FILE) \
        and not os.path.exists(PackageGenerator.ENVIRON_SCRIPT
                               + PackageGenerator.ENVIRON_SCRIPT_POSIX_EXT) \
        and not os.path.exists(PackageGenerator.ENVIRON_SCRIPT
                               + PackageGenerator.ENVIRON_SCRIPT_WIN_EXT) \
        and not os.path.exists(sha_filename)


# should be second so there are still not output files
def test_no_output_but_sha():
    """Makes sure that when no output flag is on, no files are created."""
    args = Arguments(
        src_dir="src",
        extra_data=["gbextradata"],
        pkg_dir=os.path.join("tests", "gbtestapp"),
        sha=Arguments.OPTION_SHA_FILE,
        clean=True,
        no_file=True
    )
    package_generator = PackageGenerator(args)
    generated_okay = package_generator.generate()

    assert generated_okay == EXIT_OKAY \
        and not os.path.exists(PackageGenerator.INFO_FILE) \
        and not os.path.exists(PackageGenerator.FILES_FILE) \
        and not os.path.exists(PackageGenerator.ENVIRON_SCRIPT
                               + PackageGenerator.ENVIRON_SCRIPT_POSIX_EXT) \
        and not os.path.exists(PackageGenerator.ENVIRON_SCRIPT
                               + PackageGenerator.ENVIRON_SCRIPT_WIN_EXT) \
        and os.path.exists(package_generator.files["sha_w_path"])


# test extra_pkgs and extra_modules
def test_extra_pkgs_modules():
    """Makes sure everything works with an extra package and module."""
    args = Arguments(
        src_dir="src",
        extra_data=["gbextradata"],
        pkg_dir=os.path.join("tests", "gbtestapp"),
        clean=False,
        extra_pkgs=["PyYAML"],
        extra_modules=["yaml"],
    )
    package_generator = PackageGenerator(args)
    generated_okay = package_generator.generate()

    assert generated_okay == EXIT_OKAY


@pytest.fixture
def arguments():
    """Returns an Arguments instance using the included app"""
    return Arguments(
        src_dir="src",
        extra_data=["gbextradata"],
        pkg_dir=os.path.join("tests", "gbtestapp"),
        sha=Arguments.OPTION_SHA_FILE,
        clean=True
    )


def test_generation(arguments):
    """ Tests generating the executable. """
    package_generator = PackageGenerator(arguments)
    generated_okay = package_generator.generate()

    assert generated_okay == EXIT_OKAY


def test_executable(arguments):
    """ Tests running the executable. """
    package_generator = PackageGenerator(arguments)
    generated_okay = package_generator.generate()
    if generated_okay == EXIT_OKAY:
        files = glob.glob(os.path.join(
            package_generator.args.directories['staging'],
            package_generator.args.info['app_version'],
            'gbtestapp-4.2.6-standalone*'
        ))

        cmd_output = check_output(files[0], universal_newlines=True)
        compare_file = (Path("tests") / "gbtestapp" /
                        "correct_stdout.txt").read_text(encoding="utf-8")

        assert cmd_output == compare_file
    else:
        assert False


def test_hook():
    """ Tests that the hook generated matches what is expected. """
    arguments = Arguments(
        src_dir="src",
        extra_data=["gbextradata"],
        pkg_dir=os.path.join("tests", "gbtestapp"),
        sha=Arguments.OPTION_SHA_FILE,
        clean=False
    )
    package_generator = PackageGenerator(arguments)

    generated_okay = package_generator.generate()
    if generated_okay == EXIT_OKAY:
        generated_hook = (Path(package_generator.args.directories['work']) /
                          'hooks' / 'hook-gbtestapp.py'
                          ).read_text(encoding='utf-8')
        suffix = ""
        if platform.system().lower() == "windows":
            suffix = "_windows"

        compare_file = (Path("tests") / "gbtestapp" / ("correct_hook" +
                        suffix + ".txt")).read_text(encoding='utf-8')

        assert generated_hook == compare_file
    else:
        assert False


def test_hook_with_extras():
    """
    Tests that the hook generated matches what is expected when including
    "extras" packages in the app
    """
    arguments = Arguments(
        src_dir="src",
        extra_data=["gbextradata"],
        pkg_dir=os.path.join("tests", "gbtestapp"),
        sha=Arguments.OPTION_SHA_FILE,
        include_setup_extras=True,
        clean=False
    )
    package_generator = PackageGenerator(arguments)

    generated_okay = package_generator.generate()
    if generated_okay == EXIT_OKAY:
        generated_hook = (Path(package_generator.args.directories['work']) /
                          'hooks' / 'hook-gbtestapp.py'
                          ).read_text(encoding='utf-8')
        suffix = ""
        if platform.system().lower() == "windows":
            suffix = "_windows"
        compare_file = (Path("tests") / "gbtestapp" /
                        ("correct_hook_with_extras" + suffix + ".txt")
                        ).read_text(encoding='utf-8')

        assert generated_hook == compare_file
    else:
        assert False


def test_filename_file(arguments):
    """ Tests if GravityBee writes name of standalone app in output. """
    package_generator = PackageGenerator(arguments)
    generated_okay = package_generator.generate()
    if generated_okay == EXIT_OKAY:
        with open(
            os.path.join(FILE_DIR, "gravitybee-files.json"),
            "r",
            encoding="utf8",
        ) as sa_file:
            gb_files = json.loads(sa_file.read())

        assert gb_files[0]['filename'].startswith("gbtestapp-4.2.6-standalone")
    else:
        assert False


def test_file_label():
    """ Test if GravityBee writes correct label in gravitybee-files.json. """

    label_prefix = "GBTESTapp YO"
    arguments = Arguments(
        src_dir="src",
        extra_data=["gbextradata"],
        pkg_dir=os.path.join("tests", "gbtestapp"),
        sha=Arguments.OPTION_SHA_FILE,
        clean=True,
        label_format=label_prefix + " {v} {ft} for {os}"
    )
    package_generator = PackageGenerator(arguments)
    generated_okay = package_generator.generate()
    if generated_okay == EXIT_OKAY:
        with open(
            os.path.join(FILE_DIR, "gravitybee-files.json"),
            "r",
            encoding="utf8",
        ) as sa_file:
            gb_files = json.loads(sa_file.read())

        assert gb_files[0]['label'].startswith(label_prefix)
    else:
        assert False


def test_file_sha(arguments):
    """
    Checks the generated sha hash written to file with one that is
    freshly calculated. Also checks that info file exists and has the
    correct app name and version.
    """

    # get the sha256 hash from the json file
    package_generator = PackageGenerator(arguments)
    generated_okay = package_generator.generate()
    if generated_okay == EXIT_OKAY:
        # get the info from info file
        with open(
            PackageGenerator.INFO_FILE, "r", encoding="utf8"
        ) as info_file:
            info = json.loads(info_file.read())

        with open(
            package_generator.files["sha_w_path"], "r", encoding="utf8"
        ) as sha_file:
            sha_dict = json.loads(sha_file.read())

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

    package_generator = PackageGenerator(latest_arguments)
    generated_okay = package_generator.generate()

    if generated_okay == EXIT_OKAY:

        latest_standalone = package_generator.args.formats["name"].format(
            an=package_generator.args.info['app_name'],
            v='latest',
            os=package_generator.args.info['operating_system'],
            m=package_generator.args.info['machine_type']
        )

        sa_files = glob.glob(os.path.join(
            package_generator.args.directories['staging'],
            'latest',
            latest_standalone + '*'
        ))

        sha_file = package_generator.args.formats["sha"].format(
            an=package_generator.args.info['app_name'],
            v='latest',
            os=package_generator.args.info['operating_system'],
            m=package_generator.args.info['machine_type']
        )

        sha_files = glob.glob(os.path.join(
            package_generator.args.directories['staging'],
            'latest',
            sha_file
        ))

        assert os.path.isdir(os.path.join(
            package_generator.args.directories['staging'],
            'latest')) \
            and sa_files \
            and sha_files
    else:
        assert False


@pytest.fixture
def testapp2_arguments():
    """Returns an Arguments instance using the included app.
    This app tests packaging an app that has differently named packages
    and also has multiple packages (gbtest2, gbextradata2)"""

    return Arguments(
        src_dir="src",
        extra_data=["../gbextradata2"],
        pkg_dir=os.path.join("tests", "testapp2"),
        app_name="testapp2",
        pkg_name="gbtest2",
        sha=Arguments.OPTION_SHA_FILE,
        clean=True,
    )


def test_testapp2_generation(testapp2_arguments):
    """Tests generating the testapp2 executable."""
    package_generator = PackageGenerator(testapp2_arguments)
    generated_okay = package_generator.generate()

    assert generated_okay == EXIT_OKAY


def test_testapp2_executable(testapp2_arguments):
    """Tests running the executable.
    The pkg name is gbtest2, but the app name is testapp2,
    so the exe will be named "testapp2".
    """
    package_generator = PackageGenerator(testapp2_arguments)
    generated_okay = package_generator.generate()
    if generated_okay == EXIT_OKAY:
        files = glob.glob(
            os.path.join(
                package_generator.args.directories["staging"],
                package_generator.args.info["app_version"],
                "testapp2-4.2.6-standalone*",
            )
        )

        cmd_output = check_output(files[0], universal_newlines=True)

        with open(
            os.path.join("tests", "testapp2", "correct_stdout.txt"),
            "r",
            encoding="utf8",
        ) as compare:
            compare_file = compare.read()

        assert cmd_output == compare_file
    else:
        assert False


def test_testapp2_filename_file(testapp2_arguments):
    """Tests if GravityBee writes name of standalone app in output."""
    package_generator = PackageGenerator(testapp2_arguments)
    generated_okay = package_generator.generate()
    if generated_okay == EXIT_OKAY:
        sa_file = (Path(FILE_DIR) / "gravitybee-files.json")
        gb_files = json.loads(sa_file.read_text(encoding='utf-8'))

        assert gb_files[0]["filename"].startswith("testapp2-4.2.6-standalone")
    else:
        assert False


@pytest.fixture
def testing_defaults():
    """Return an Arguments instance for testing defaults"""
    if not os.getcwd().endswith(os.path.join("tests", "gbtestapp")):
        os.chdir(os.path.join("tests", "gbtestapp"))
    return Arguments()


def test_clean(testing_defaults):
    """Test clean default"""
    assert not testing_defaults.flags["clean"]


def test_pkg_dir(testing_defaults):
    """Test pkg_dir default"""
    assert testing_defaults.directories["pkg"] == '.'


def test_src_dir(testing_defaults):
    """Test src_dir default"""
    assert testing_defaults.directories["src"] == '.'


def test_name_format(testing_defaults):
    """Test name_format default"""
    assert testing_defaults.formats["name"] == '{an}-{v}-standalone-{os}-{m}'


def test_sha_format(testing_defaults):
    """Test sha_format default"""
    assert testing_defaults.formats["sha"] == '{an}-{v}-sha256-{os}-{m}.json'


def test_extra_data(testing_defaults):
    """Test extra data default"""
    assert testing_defaults.extra["data"] is None


def test_work_dir(testing_defaults):
    """Test work_dir default"""
    assert testing_defaults.directories["work"][:17] == os.path.join(
        FILE_DIR,
        'build')[:17]


def test_console_script(testing_defaults):
    """Test console_script default"""
    assert testing_defaults.info["console_script"] == 'gbtestapp'


def test_app_version(testing_defaults):
    """Test app_version default"""
    assert testing_defaults.info["app_version"] == '4.2.6'


def test_app_name(testing_defaults):
    """Test app_name default"""
    assert testing_defaults.info["app_name"] == 'gbtestapp'


def test_pkg_name(testing_defaults):
    """Test pkg_name default"""
    assert testing_defaults.info["pkg_name"] == 'gbtestapp'
