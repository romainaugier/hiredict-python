import logging
import sys
import typing
import io


root_logger = logging.getLogger("hiredict-py")
root_logger.setLevel(logging.DEBUG)

if sys.stdout is not None:
    formatter = logging.Formatter("%(levelname)s : %(message)s")
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    root_logger.addHandler(consoleHandler)

def _list_fmt(l: typing.List) -> str:
    if not isinstance(l, list):
        return str(l)

    buffer = io.StringIO()
    
    buffer.write("[\n")
    buffer.write(",\n".join([f"{' ' * 4}{str(item)}" for item in l]))
    buffer.write("\n]")

    return buffer.getvalue()

def _dict_fmt(d: typing.Dict) -> str:
    if not isinstance(d, dict):
        return str(d)
    
    buffer = io.StringIO()
    
    buffer.write("{\n")
    buffer.write(",\n".join([f"{' ' * 4}{str(key)} : {str(value)}" for key, value in d.items()]))
    buffer.write("\n}")
    
    return buffer.getvalue()

_fmt_funcs = {
    list: _list_fmt,
    dict: _dict_fmt,
    None: str
}

def _fmt(obj: typing.Any) -> str:
    try:
        func = _fmt_funcs.get(type(obj))
        
        if func is None:
            func = _fmt_funcs[None]

        return func(obj)
    except:
        return str(obj)

def _args_fmt(*args) -> str:
    return _fmt(args[0]).strip("\n") if len(args) == 1 else ", ".join([_fmt(arg) for arg in args]).strip("\n")

def debug(*args):
    root_logger.debug(_args_fmt(*args))

def info(*args):
    root_logger.info(_args_fmt(*args))

def warning(*args):
    root_logger.warning(_args_fmt(*args))

def error(*args):
    root_logger.error(_args_fmt(*args))

def critical(*args):
    root_logger.critical(_args_fmt(*args))