"""Configuration objects"""

from collections.abc import Iterable
from typing import Any, Dict, List, Union


class Config:
    """
    A class defining the structure of configurations expected by an application.

    Configurations are represented as key-value pairs, where the application defines the structure
    of the expected configurations and the user provides some subset of the key-value pairs, which
    are processed and populated by this class.

    Args:
        keys (``list[Key]``): the list of keys expected in the configuration
    """

    keys: List["Key"]
    """the list of keys expected in the configuration"""

    def __init__(self, keys: List["Key"]) -> None:
        if not isinstance(keys, Iterable) or not all(isinstance(e, Key) for e in keys):
            raise TypeError("'keys' must be a list (or other iterable) of keys")

        if not isinstance(keys, list):
            keys = list(keys)

        self.keys = keys

    def __eq__(self, other: Any) -> bool:
        """
        Determine whether another object is equal to this config. An object is equal to a config iff
        it is also a config and has the same keys.
        """
        return isinstance(other, type(self)) and self.keys == other.keys

    @classmethod
    def from_list(cls, lst: List[Union["Key", Dict[str, Any]]]) -> "Config":
        """
        Create a ``Config`` from a list of ``Key`` s or ``dict`` s.

        Args:
            lst (``list[Key | dict[str, object]]``): the list of keys

        Returns:
            ``Config``: the configuration
        """
        keys = [e if isinstance(e, Key) else Key.from_dict(e) for e in lst]
        return cls(keys)

    def _get_keys_dict(self) -> Dict[str, "Key"]:
        """
        Generate a dictionary mapping key names to ``Key`` objects.

        Returns:
            ``dict[str, Key]``: the dictionary
        """
        return {k.name: k for k in self.keys}

    def get_key(self, key: str) -> "Key":
        """
        Get the :py:class:`fica.Key` with the specified name.

        Args:
            key (``str``): the name of the key

        Returns:
            :py:class:`fica.Key`: the key
        """
        return self._get_keys_dict()[key]

    def to_dict(self, user_config: Dict[str, Any] = {}, include_empty=False) -> Dict[str, Any]:
        """
        Generate a dictionary with all keys present, adding values from the provided user input.

        Args:
            user_config (``dict[str, object]``): the user-inputted configurations
            include_empty (``bool``): whether configurations that aren't overridden whose defaults
                are :py:obj:`fica.EMPTY` should be included in the resulting dictionary

        Returns:
            ``dict[str, object]``: the dictionary of configurations
        """
        config = {}
        keys_dict = self._get_keys_dict()
        for k, v in user_config.items():
            if k not in keys_dict:
                config[k] = v
            else:
                pair = keys_dict[k].to_pair(v, include_empty=include_empty)
                if pair is not None:
                    config[pair.key] = pair.value

        for k, v in keys_dict.items():
            if k not in config:
                pair = v.to_pair(include_empty=include_empty)
                if pair is not None:
                    config[pair.key] = pair.value

        return config


from .key import Key
