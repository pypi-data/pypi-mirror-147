""" 
This module provides two high-level functions for reading and data files:

    * :py:func:`import_file`
    * :py:func:`export_file`

"""
import abc
import traits.has_traits

__all__ = ['import_file', 'export_file', 'FileReaderInterface']

class FileReaderInterface(traits.has_traits.ABCHasStrictTraits):
    @abc.abstractmethod
    def parse(self, data, **kwargs):
        raise NotImplementedError