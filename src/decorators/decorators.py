

def normalize_item(item):
    """
    For auto generated to strings bytes can be enourmous. To prettify the results we take bytes and convert them to strings of a fixed literal.
    Does require the use of isinstance and causes some minor ambiguity but the benefit is a string outpout of models won't blow up
    for a few bytes properties
    """
    key, value = item
    if(isinstance(value, bytes)):
        value = "b\bytes"
    if(isinstance(value, list)):
        value = [("b\bytes" if isinstance(v, bytes) else v) for v in value]
    return (key, value)


def auto_str(cls):
    """
    Decorator that automatically creates a "to string" method when str is called on the object
    """
    def __str__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % normalize_item(item) for item in vars(self).items())
        )
    cls.__str__ = __str__
    return cls