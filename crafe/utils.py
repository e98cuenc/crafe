def safestr(obj, encodings_to_try=['utf-8', 'iso-8859-15']):
    r"""
    Converts any given object to utf-8 encoded string. 

    The version in web.utils is buggy, because if the obj contains a utf-8
    illegal byte sequence it will not sanitize it.

    If we find an illegal utf-8 byte sequence, we will read the entire obj
    as iso-8859-15.

        >>> safestr('hello')
        'hello'
        >>> safestr(u'\u1234')
        '\xe1\x88\xb4'
        >>> safestr(2)
        '2'
    """
    if isinstance(obj, unicode):
        return obj.encode('utf-8')
    elif isinstance(obj, str):
        for encoding in encodings_to_try:
            try:
                return obj.decode(encoding).encode('utf-8')
            except:
                pass
        return obj.decode('iso-8859-1').encode('utf-8')
    elif hasattr(obj, 'next') and hasattr(obj, '__iter__'): # iterator
        return itertools.imap(safestr, obj)
    else:
        return safestr(str(obj))


def get_extension(str):
    """Returns the part after the last '.' in a string."""
    dot_position = str.rfind('.')
    if dot_position >= 0:
        return str[dot_position + 1:]
    return ''
