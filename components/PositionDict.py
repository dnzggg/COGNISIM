class PositionDict(dict):
    """Subclass of dict object to store position of the agents on the screen

    Methods
    -------
    __setitem__(key, val)
        Sets the key to a value
    __getitem__(item)
        Returns value given the key
    """
    def __setitem__(self, key, val):
        """Sets the key to a value

        Parameters
        ----------
        key: tuple[range, range]
            Key to be set
        val: Agent
            Value to be set
        """
        super().__setitem__(key, val)

    def __getitem__(self, key):
        """Returns value given the key

        Parameters
        ----------
        key: tuple[int, int]
            Key of the value

        Returns
        -------
        bool
            The value that the key maps to

        Raises
        ------
        KeyError
            If a key cannot be found in the dictionary
        """
        if not isinstance(key, range):
            for keys in self:
                k1, k2 = keys
                if key[0] in tuple(k1) and key[1] in tuple(k2):
                    return self.get(keys)
            raise KeyError(key)
        else:
            return super().__getitem__(key)
