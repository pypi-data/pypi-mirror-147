# Module Tools

Tools for python modules

## Installation

```shell
$ pip install module-tools
```

## Examples

```python
"""
package
    __init__.py
    sub_package
        __init__.py
        modulec.py -> var5, var6 = 3, "c"
    modulea.py -> var1, var2, add = 1, "a", lambda a, b: a + b
    moduleb.py -> var3, var4 = 2, "b"
"""

from package.modulea import add

from module_tools import find_module_strings, find_modules, import_string, iter_objs_from_modules

add1 = import_string("package.modulea.add")
print(add1 is add)  # True

print(set(find_module_strings("package")) == {"package.modulea", "package.moduleb"})  # True
print(
    set(find_module_strings("package", recursive=True))
    == {"package.modulea", "package.moduleb", "package.sub_pakage.modulec"}
)  # True
from package import modulea, moduleb
from package.sub_package import modulec

print(set(find_modules("package")) == {modulea, moduleb})  # True
print(set(find_modules("package", recursive=True)) == {modulea, moduleb, modulec})  # True

print(set(iter_objs_from_modules(["package"], cls=int)) == {1, 2})  # True
print(set(iter_objs_from_modules(["package"], cls=int, recursive=True)) == {1, 2, 3})  # True

print(
    set(iter_objs_from_modules(["package"], cls=int, recursive=True, func=lambda x: x < 3))
    == {1, 2}
)  # True
```