def auto_str(cls):
    """
    Decorator that automatically creates a "to string" method when str is called on the object
    """
    def __str__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )
    cls.__str__ = __str__
    return cls