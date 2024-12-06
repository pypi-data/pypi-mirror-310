######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.12.30.2+obcheckpoint(0.1.4);ob(v1)                                                   #
# Generated on 2024-11-21T22:12:20.814669                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

from .exception import MetaflowException as MetaflowException

class PyLintWarn(metaflow.exception.MetaflowException, metaclass=type):
    ...

class PyLint(object, metaclass=type):
    def __init__(self, fname):
        ...
    def has_pylint(self):
        ...
    def run(self, logger = None, warnings = False, pylint_config = []):
        ...
    ...

