# PySimpleTest -- Make test as simple as possible

PySimpleTest is a very simple test framwork. To start using it, try following example:  
Write a file `main.py`:

```python
from PySimpleTest import *

a = 2
should_be_equal(a, 2)
should_be_less(a, 1)
```

Then run it. You can get following cmd output:

![avatar](https://gitee.com/time-coder/PySimpleTest/raw/master/images/first_example.png)

Please see full documentation at [https://github.com/Time-Coder/PySimpleTest](https://github.com/Time-Coder/PySimpleTest)

## Release Note
### 1.0.5
* Added `Section` class. User can use `Section` with Python `with` syntax instead of `section`, `end_section`, `subsection`.
### 1.0.2
* First release for all basic functions.