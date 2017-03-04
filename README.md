## list-opengl-extensions
Lists all OpenGL extensions your codebase uses.

---

### Usage
```
python list-opengl-extensions.py -i <src_directory> [-n]
```

* `-n`: Print the number of times each extension was used

#### Known issues:
* Database needs to be updated and formatted manually with each update from [here](https://raw.githubusercontent.com/cginternals/glbinding/master/source/glbinding/source/Meta_FunctionStringsByExtension.cpp).
