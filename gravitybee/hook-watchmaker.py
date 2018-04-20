from PyInstaller.utils.hooks import copy_metadata, collect_data_files, collect_submodules
import platform
import pyppyn

hiddenimports = (
    collect_submodules('watchmaker')
)

datas = copy_metadata('watchmaker')
datas += collect_data_files('watchmaker')

datas.append(('../src/watchmaker/static', './watchmaker/static'))

pyp = gravitybee.ConfigRep(setup_file="../setup.cfg",verbose=True)

# get all the packages called for by setup.cfg
for pkg in pyp.get_required():
    datas += copy_metadata(pkg)

"""
datas += copy_metadata('defusedxml')
datas += copy_metadata('PyYAML')
datas += copy_metadata('six')
datas += copy_metadata('click')
datas += copy_metadata('backoff')
"""

#datas += copy_metadata('watchmaker.exceptions')
#datas += collect_data_files('watchmaker.exceptions')
#datas += copy_metadata('watchmaker.logger')
#datas += collect_data_files('watchmaker.logger')
#datas += copy_metadata('watchmaker.managers')
#datas += collect_data_files('watchmaker.managers')
#datas += copy_metadata('watchmaker.static')
#datas += collect_data_files('watchmaker.static')
#datas += copy_metadata('watchmaker.utils')
#datas += collect_data_files('watchmaker.utils')
#datas += copy_metadata('watchmaker.utils.urllib')
#datas += collect_data_files('watchmaker.utils.urllib')
#datas += copy_metadata('watchmaker.workers')
#datas += collect_data_files('watchmaker.workers')

"""
if platform.system().lower() == 'linux':
    datas.append(('/var/opt/git/watchmaker/src/watchmaker/static', './watchmaker/static'))
elif platform.system().lower() == 'windows':
    datas += copy_metadata('pypiwin32')
    datas.append(('C:/git/watchmaker/src/watchmaker/static', './watchmaker/static'))
"""

