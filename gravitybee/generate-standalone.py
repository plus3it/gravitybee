import os
import platform
import shutil
import subprocess
import sys
import pyppyn


def check_environ():
    try:
        version = os.environ["SATS_VERSION"]
        



def main():

if __name__ == '__main__':
    
    sys.exit(main())
    operating_system = platform.system()
    machine_type = platform.machine()

    app_name = 'watchmaker-{v}-standalone-{os}-{m}'.format(
        v=wam_version.lower(),
        os=operating_system.lower(),
        m=machine_type.lower())

    """
    if operating_system.lower() == 'linux':
        src_path = '/var/opt/git/watchmaker/src'
        additional_hooks = '/var/opt/git/gravitybee/pyinstaller'
    elif operating_system.lower() == 'windows':
        src_path = 'C:\\git\\watchmaker\\src'
        additional_hooks = 'C:\\git\\gravitybee\\pyinstaller'
    """
    commands = [
        'pyinstaller',
        '--noconfirm',
        #'--clean',
        '--onefile',
        '--name', app_name,
        '--paths', 'src',
        '--additional-hooks-dir', '.',
        # This hidden import is introduced by botocore.
        # We won't need this when this issue is resolved:
        # https://github.com/pyinstaller/pyinstaller/issues/1844
        '--hidden-import', 'html.parser',
        # This hidden import is also introduced by botocore.
        # It appears to be related to this issue:
        # https://github.com/pyinstaller/pyinstaller/issues/1935
        '--hidden-import', 'configparser',
        '--hidden-import', 'watchmaker',
        '--hidden-import', 'packaging',
        '--hidden-import', 'packaging.specifiers',
        '--hidden-import', 'pkg_resources',
    ]

    pyp = pyppyn.ConfigRep(setup_file="../setup.cfg",verbose=True)
    pyp.read_config()
    pyp.load_config()
    print("Packages needed:")
    print(*(pyp.base_reqs + pyp.this_python_reqs + pyp.this_os_reqs),sep="\n")
    #pyp.install_packages()

    # get all the packages called for by setup.cfg
    for pkg in pyp.base_reqs + pyp.this_python_reqs + pyp.this_os_reqs:
        commands += [
            '--hidden-import', pkg,
        ]

    commands += [
        'watchmaker-script.py'
    ]

    if operating_system.lower() == 'linux':
        insert_point = commands.index('--onefile') + 1
        commands[insert_point:insert_point] = ['--runtime-tmpdir', '.']

    print(*commands, sep=', ')

    subprocess.run(
        commands,
        check=True)

    # zip up
    """shutil.make_archive(
        base_name=os.path.join(
            THIS_DIR, 'dist',
            'watchmaker-{v}-standalone-{os}-{m}'.format(
                v=wam_version,
                os=operating_system,
                m=machine_type)),
        format='zip',
        root_dir=os.path.join(THIS_DIR, 'dist', app_name))"""
