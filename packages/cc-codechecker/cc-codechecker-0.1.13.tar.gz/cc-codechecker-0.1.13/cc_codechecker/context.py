# SPDX-FileCopyrightText: 2022 Daniele Tentoni <daniele.tentoni.1996@gmail.com
#
# SPDX-License-Identifier: MIT

"""Context definition."""
# Standard Library
import copy
from argparse import Namespace
from threading import Lock
from typing import Any
from weakref import WeakValueDictionary


class Singleton(type):
  """Pythonic implementation of singleton."""

  _instances: WeakValueDictionary = WeakValueDictionary()
  _lock: Lock = Lock()

  def __call__(cls, *args: Any, **kwargs: Any):
    """Call the single instance of a class.

    :return: class instance
    """
    with cls._lock:
      if cls not in cls._instances:
        instance = super().__call__(*args, **kwargs)
        cls._instances[cls] = instance

    return cls._instances[cls]

class Context(metaclass=Singleton):
  """Contextual data and information to inject in every class.

  Use this utility to store cli options and other env info.
  """

  def __init__(
    self,
    options: Namespace = Namespace(verbose = False),
  ):
    """Create a new Context object.

    This method instance a new Context object the first time, any other time it
    return the instance created the first time.

    :param options: Options from command line for the current execution.
        Defaults to Namespace(verbose = False)
    :type options: Namespace, optional
    """
    self._options = options

  @classmethod
  def get(cls, name: str, default):
    """Get the value of a specific option in the context.

    :param name: [description]
    :type name: str
    :return: Value of the options or the default value

    .. todo:: make this class more generic
    """
    opts = Context().options()
    if name in opts:
      return getattr(Context().options(), name)

    return default

  def options(self) -> Namespace:
    """Get a deepcopy of options.

    To update an options, use the set_option method. It will be implemented
    before next major release.

    Returns:
      Namespace: Options from command line.
    """
    return copy.deepcopy(self._options)
