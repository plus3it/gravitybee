import os

class Arguments(object):
    """
    Arguments for GravityBee
    """

    _app_name = None
    _pkg_name = None
    _script_path = None
    _pkg_dir = None

    def __init__(self, *args, **kwargs):
        """Instantiation"""

        # Remove unused options
        empty_keys = [k for k,v in kwargs.items() if not v]
        for k in empty_keys:
            del kwargs[k]

        # Initial values
        self._app_name = kwargs.get('app_name',os.environ.get('GB_APP_NAME',None))
        self._pkg_name = kwargs.get('pkg_name',os.environ.get('GB_PKG_NAME',None))
        self._script_path = kwargs.get('script_path',os.environ.get('GB_SCRIPT',None))
        self._pkg_dir = kwargs.get('pkg_dir',os.environ.get('GB_PKG_DIR',None))
        gravitybee.verbose = kwargs.get('verbose',False)

        if self._app_name is None:
            self._get_app_name()

    def _get_app_name(self):
        pass

