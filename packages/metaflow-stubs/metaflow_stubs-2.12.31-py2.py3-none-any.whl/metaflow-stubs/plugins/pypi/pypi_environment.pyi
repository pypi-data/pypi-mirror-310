######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.12.31                                                                                #
# Generated on 2024-11-22T20:12:01.502569                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.pypi.conda_environment

from .conda_environment import CondaEnvironment as CondaEnvironment

class PyPIEnvironment(metaflow.plugins.pypi.conda_environment.CondaEnvironment, metaclass=type):
    ...

