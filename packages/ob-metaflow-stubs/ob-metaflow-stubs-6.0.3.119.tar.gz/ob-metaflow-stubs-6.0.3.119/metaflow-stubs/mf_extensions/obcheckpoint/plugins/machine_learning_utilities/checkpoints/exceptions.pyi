######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.12.30.2+obcheckpoint(0.1.4);ob(v1)                                                   #
# Generated on 2024-11-21T22:12:20.835614                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

from ......exception import MetaflowException as MetaflowException

class CheckpointNotAvailableException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, message):
        ...
    ...

class CheckpointException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, message):
        ...
    ...

