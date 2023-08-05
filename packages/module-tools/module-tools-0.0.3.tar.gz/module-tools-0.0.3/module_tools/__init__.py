__version__ = "0.0.3"


import pkgutil
from importlib import import_module
from types import ModuleType
from typing import Any, Callable, Iterable, Optional, Tuple, Type, Union

CLS = Union[Type, Tuple[Union[Type, Tuple[Any, ...]], ...]]


def import_string(dotted_path: str) -> Any:
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit(".", 1)
    except ValueError as err:
        raise ImportError("%s doesn't look like a module path" % dotted_path) from err

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError as err:
        raise ImportError(
            'Module "{}" does not define a "{}" attribute/class'.format(module_path, class_name)
        ) from err


def find_module_strings(pkg_name: str, *, recursive: bool = False) -> Iterable[str]:
    """Get the dotted module path path under a package
    package
        __init__.py
        sub_package
            __init__.py
            modulec.py
        modulea.py
        moduleb.py
    set(find_module_strings("package")) == {"package.modulea", "package.moduleb"}
    set(find_module_strings("package", recursive=True)) == {"package.modulea", "package.moduleb", "package.sub_pakage.modulec"}
    """
    pkg = import_module(pkg_name)
    module_path = getattr(pkg, "__path__", None)
    if module_path is None:
        return [pkg_name]
    iter_modules_func = pkgutil.walk_packages if recursive else pkgutil.iter_modules
    return (
        module_info[1]
        for module_info in iter_modules_func(module_path, pkg.__name__ + ".")
        if not module_info[2]
    )


def find_modules(pkg_name: str, *, recursive: bool = False) -> Iterable[ModuleType]:
    """Get the modules path under a package
    package
        __init__.py
        sub_package
            __init__.py
            modulec.py
        modulea.py
        moduleb.py
    from package import modulea, moduleb
    from package.sub_package import modulec
    set(find_modules("package")) == {modulea, moduleb}
    set(find_modules("package", recursive=True)) == {modulea, moduleb, modulec}
    """
    return (
        import_module(module_string)
        for module_string in find_module_strings(pkg_name, recursive=recursive)
    )


def iter_objs_from_module(
    module: ModuleType,
    *,
    cls: Optional[CLS] = None,
    func: Optional[Callable[[Any], bool]] = None,
) -> Iterable[Any]:
    """Get the objects from a package"""
    for attr_name in dir(module):
        if attr_name.startswith("__"):
            continue
        attr = getattr(module, attr_name)
        if cls is not None and not isinstance(attr, cls):
            continue
        if func is not None and not func(attr):
            continue
        yield attr


def iter_objs_from_modules(
    pkg_names: Iterable[str],
    *,
    cls: Optional[CLS] = None,
    recursive: bool = False,
    func: Optional[Callable[[Any], bool]] = None,
) -> Iterable[Any]:
    """Get the objects from packages
    package
        __init__.py
        sub_package
            __init__.py
            modulec.py -> var5, var6 = 3, "c"
        modulea.py -> var1, var2 = 1, "a"
        moduleb.py -> var3, var4 = 2, "b"
    set(iter_objs_from_modules(["package"], cls=int)) == {1, 2}
    set(iter_objs_from_modules(["package"], cls=int, recursive=True)) == {1, 2, 3}
    set(iter_objs_from_modules(["package"], cls=int, recursive=True, func=lambda x: x < 3)) == {1, 2}
    """
    obj_ids = set()
    for pkg_name in pkg_names:
        modules = find_modules(pkg_name, recursive=recursive)
        for module in modules:
            for obj in iter_objs_from_module(module, cls=cls, func=func):
                obj_id = id(obj)
                if obj_id in obj_ids:
                    continue
                obj_ids.add(obj_id)
                yield obj
