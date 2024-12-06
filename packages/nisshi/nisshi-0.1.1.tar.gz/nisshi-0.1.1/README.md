# nisshi for Python

## Importing the library

### From pip 
```sh
pip install nisshi
```

```py
from nisshi import Nisshi
nisshi = Nisshi()
```

### From source

```py
from nisshi import Nisshi
nisshi = Nisshi()
```

## Use

### Basic logging functionality

```py
nisshi.trace("trace message");
nisshi.debug("debug message");
nisshi.info("info message");
nisshi.warn("warn message");
nisshi.error("error message");
```

Can also use `newline()` to make an empty line. Useful for if you're outputting chunks of text (e.g. various debug messages).

```py
nisshi.newline();
```

### Change logging levels

Enable all logging levels:

```py
nisshi.set_levels("all");
```

Disable logging:

```py
nisshi.set_levels("none");
```

Toggle levels:

```py
# disable all logging except for errors
nisshi.set_levels("none")
nisshi.set_levels({"error": true})

# enable warnings and info
nisshi.set_levels({"warn": true, "info": true})

# re-disable info
nisshi.set_levels({"info": false})
```

## Changelog

### 0.1.1

made the logger actually work

i need to check my code more :skull:

### 0.1.0

initial release
