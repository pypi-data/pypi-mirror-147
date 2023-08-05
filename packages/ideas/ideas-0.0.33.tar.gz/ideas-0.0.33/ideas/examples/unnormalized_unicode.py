"""Python does 'normalization' of unicode names by default.
As a result, some different unicode names can end up representing
the same object.

This example demonstrates how different names can be prevented
from being 'normalized'.

Original idea from Sergey B. Kirpichev.
See https://github.com/aroberge/ideas/issues/13 for a reference.
"""
import io
import tokenize
import unicodedata
import uuid

from ideas import import_hook

__NAMES_MAP = {}


def transform_names(source, **_kwargs):
    """Transform names that would normally be 'normalized' by
    Python into different and unique variable names.
    """
    result = []
    g = tokenize.tokenize(io.BytesIO(source.encode()).readline)
    for toknum, tokval, _, _, _ in g:
        if toknum == tokenize.NAME:
            normalized_name = unicodedata.normalize("NFKC", tokval)
            if normalized_name != tokval:
                if tokval not in __NAMES_MAP:
                    __NAMES_MAP[tokval] = f"{normalized_name}_{uuid.uuid4().hex!s}"
                tokval = __NAMES_MAP[tokval]
        result.append((toknum, tokval))
    return tokenize.untokenize(result).decode()


def new_dir(obj=None):
    """Similar to Python's dir, but shows the original name
    entered, not the transformed one. It also filters out any variable
    whose names starts with a double underscore.

    Note: the real Python dir() should be available as true_dir().
    """
    import inspect

    if obj is not None:
        names = dir(obj)
    else:
        names = list(inspect.currentframe().f_back.f_locals)
    for k, v in __NAMES_MAP.items():
        names = [_.replace(v, k) for _ in names]
    names = [name for name in names if not names.startswith("__")]
    if obj is None:
        # Purposely hide some names :-)
        for name in ["dir", "true_dir"]:
            if name in names:
                names.remove(name)
    return sorted(names)


import_hook.create_hook(
    transform_source=transform_names,
    console_dict={"__NAMES_MAP": __NAMES_MAP, "dir": new_dir, "true_dir": dir},
)
