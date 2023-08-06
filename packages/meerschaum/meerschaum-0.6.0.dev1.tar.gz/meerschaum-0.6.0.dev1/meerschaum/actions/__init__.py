#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""
Default actions available to the mrsm CLI.
"""

from __future__ import annotations
from meerschaum.utils.typing import Callable, Any, Optional, Union, List
from meerschaum.utils.packages import get_modules_from_package
from meerschaum.utils.warnings import enable_depreciation_warnings
enable_depreciation_warnings(__name__)
_shell = None
_custom_actions = []

### build __all__ from other .py files in this package
import sys
__all__, modules = get_modules_from_package(
    sys.modules[__name__],
    names = True,
)

### build the actions dictionary by importing all
### functions that do not begin with '_' from all submodules
from inspect import getmembers, isfunction
actions = dict()
for module in modules:
    ### A couple important things happening here:
    ### 1. Find all functions in all modules in `actions` package
    ###     (skip functions that begin with '_')
    ### 2. Add them as members to the Shell class
    ###     - Original definition : meerschaum.actions.shell.Shell
    ###     - New definition      : meerschaum.actions.Shell
    ### 3. Populate the actions dictionary with function names and functions
    ###
    ### UPDATE:
    ### Shell modifications have been deferred to get_shell in order to improve lazy loading.

    actions.update(
        dict(
            [
                ### __name__ and new function pointer
                (ob[0], ob[1])
                    for ob in getmembers(module)
                        if isfunction(ob[1])
                            ### check that the function belongs to the module
                            and ob[0] == module.__name__.replace('_', '').split('.')[-1]
                            ### skip functions that start with '_'
                            and ob[0][0] != '_'
            ]
        )
    )

original_actions = actions.copy()
from meerschaum.actions._entry import _entry as entry

def get_shell(
        sysargs : List[str] = [],
        reload : bool = False,
        debug : bool = False
    ):
    """Lazy load the Shell

    Parameters
    ----------
    sysargs : List[str] :
         (Default value = [])
    reload : bool :
         (Default value = False)
    debug : bool :
         (Default value = False)

    Returns
    -------

    """
    global _shell
    from meerschaum.utils.debug import dprint
    import meerschaum.actions.shell as shell_pkg

    if _shell is None or reload:
        if debug:
            dprint("Loading the shell...")

        if _shell is None:
            shell_pkg._insert_shell_actions()
            _shell = shell_pkg.Shell(actions, sysargs=sysargs)
        elif reload:
            _shell.__init__()
    return _shell

def get_subactions(action : str) -> Dict[str, Callable[[Any], Any]]:
    """

    Parameters
    ----------
    action : str :
        

    Returns
    -------
    type
        

    """
    import importlib, inspect
    subactions = {}
    try:
        action_module = importlib.import_module(f"meerschaum.actions.{action}")
    except ImportError:
        action_module = None
    if action_module is not None:
        for name, f in inspect.getmembers(action_module):
            if not inspect.isfunction(f):
                continue
            if action + '_' in name and not name.lstrip('_').startswith('complete'):
                _name = name.replace(action, '')
                _name = _name.lstrip('_')
                subactions[_name] = f
    return subactions

def get_completer(action : str) -> Optional[Callable[['Shell', str, str, int, int], List[str]]]:
    """Search for a custom completer function for an action.

    Parameters
    ----------
    action : str :
        

    Returns
    -------

    """
    import importlib, inspect
    try:
        action_module = importlib.import_module(f"meerschaum.actions.{action}")
    except ImportError:
        action_module = None
    if action_module is not None:
        for name, f in inspect.getmembers(action_module):
            if not inspect.isfunction(f):
                continue
            if 'complete_' + action in name:
                return f
    return None

def _get_parent_plugin(stacklevel : int = 1) -> Optional[str]:
    """

    Parameters
    ----------
    stacklevel : int :
         (Default value = 1)

    Returns
    -------
    type
        If this function is called from outside a Meerschaum plugin, it will return None.

    """
    from meerschaum.config._paths import PLUGINS_RESOURCES_PATH
    import inspect, re
    parent_globals = inspect.stack()[stacklevel][0].f_globals
    parent_file = parent_globals.get('__file__', '')
    if str(PLUGINS_RESOURCES_PATH) not in parent_file:
        return None
    return parent_globals['__name__'].replace('plugins.', '').split('.')[0]

#  import meerschaum.plugins
from meerschaum.plugins import import_plugins, make_action, load_plugins
plugins = import_plugins()
#  plugins = meerschaum.plugins.import_plugins()
### Instruct pdoc to skip the `meerschaum.actions.plugins` subdirectory.
__pdoc__ = {'plugins' : False, 'arguments': False}
#  make_action = meerschaum.plugins.make_action
#  meerschaum.plugins.load_plugins()
load_plugins()
