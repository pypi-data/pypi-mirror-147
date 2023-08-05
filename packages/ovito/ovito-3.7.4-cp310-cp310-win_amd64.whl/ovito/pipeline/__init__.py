"""
This module contains object types that are part of OVITO's data pipeline system.

**Pipelines:**

  * :py:class:`Pipeline`
  * :py:class:`Modifier` (base class)

**Data sources:**

  * :py:class:`StaticSource`
  * :py:class:`FileSource`
  * :py:class:`PythonScriptSource`

"""
import abc
import traits.has_traits

__all__ = ['Pipeline', 'Modifier', 'StaticSource', 'FileSource', 'PythonScriptSource', 'ModifierInterface']

class ModifierInterface(traits.has_traits.ABCHasStrictTraits):
    @abc.abstractmethod
    def execute(self, data, **kwargs):
        raise NotImplementedError
    def modifier_specs(self, pipeline_info):
        raise NotImplementedError