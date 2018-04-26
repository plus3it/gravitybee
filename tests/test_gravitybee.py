# test_gravitybee.py

import pytest
import glob
import os

from subprocess import check_output

from gravitybee import Arguments, PackageGenerator

@pytest.fixture
def arguments():
    """Returns an Arguments instance using the included app"""
    return Arguments(
        src_dir="src",
        extra_data=["gbextradata"],
        verbose=True,
        pkg_dir=os.path.join("tests", "gbtestapp"),
        clean=True)

def test_generation(arguments):
    """ Tests running the executable. """
    pg = PackageGenerator(arguments)
    generated_okay = pg.generate()

    assert generated_okay

def test_executable(arguments):
    """ Tests running the executable. """
    pg = PackageGenerator(arguments)
    generated_okay = pg.generate()
    if generated_okay:
        files = glob.glob('gbtestapp-4.2.6-standalone*')

    cmd_output = check_output(os.path.join('.',files[0]))
    compare_file = open(os.path.join("tests", "gbtestapp", "correct_stdout.txt"),"rb").read()

    assert cmd_output == compare_file


