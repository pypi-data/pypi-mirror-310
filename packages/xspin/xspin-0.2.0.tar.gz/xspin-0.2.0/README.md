# Xspin

Python module for creating spinners in the console.

## Features
* Asynchronous spinners
* Custom spinner frames and text.
* Multiline spinner frames.
* Works on windows conhost.exe.

## Installation
```bash
pip install xspin
```

## Spinner Types
There are two types of spinners provided by the module.

### Prebuilt spinners
These are ready to use. They rely on python's formating
template syntax to define how the spinner's label and frames
are positioned relative to each other. These are:
- #### Xspin
    These are used with blocking tasks as they run on a 
    separate python thread.
- #### Axspin
    These are used with async tasks.

### Custom Spinners
These are inherited from, and requires defination of the 
`frames` method. It should return an iterable of string's
representing the spinner view. These are:

- #### BaseSpinner
    Used with blocking tasks.
- #### BaseAspinner
    Used with async tasks.

## Running a spinner
There are three ways a spinner can be run.

- ### `start` and `stop` methods.
    All spinners contain a start and stop method 
    which can be called to start and stop the
    spinner instance respectively.

- ## Context manager.
    Spinner instances support the context manager protocal. Remember to use `async with` for the async spinners. This starts and stops the spinner automatically.

```python
spinner = Xspin()
with spinner:
    do_work()
```

For async spinners:

```python
spinner = Axspin()
async main():
    async with spinner:
        await do_work()
```

- ## Binding to a function.
    Spinner instances contain the `bind` method which acts like a decorator, for binding the 
    spinner to a function. The function should take in a spinner instance as its first parameter.

```python
spinner = Xspin()

@spinner.bind
def work(spinner: Xspin):
    ...

work()
```

For async spinners:

```python
aspinner = Axspin()

@aspinner.bind
async def work(spinner: Axspin):
    ...

async def main():
    await work()
```

The above methods for running the spinner work for instances of subclasses of `BaseSpinner` and `BaseAspinner`.

## Logging
During spinner progress, the `echo` method should be used for logging when the spinner is running.

```python
with spinner as sp:
    sp.echo("Doing something")
    sleep()
    sp.echo("Done!")
```

## Xlog
This is a namespace used to store the rules defining how text should be formated when various logging methods
are used in `Xspin` and `Axspin` instances. The rules are defined with python's formatting template syntax
where the field `text` is used to mark where the text will be positioned. The names of the rules
correspond to the logging functions they are used in.

- `success` Used when stopping a spinner if the process being run was successful.
- `error` Used when stopping a spinner if the process being run failed.
- `warn` Used to log out warnings. 
- `debug` Used to log out debug information. 
- `title` Used to mark the onset of a task in the process. 
- `stage` Used to indicate a step in some task in the process.. 

[NOTE] You can always just use the `echo` method instead.
    
## Stream
The default stream that the spinner is rendered is
`stdout`. If `stdout` is not `tty`, it uses `stderr` and if `stderr` is not `tty`, then the spinner is not rendered. This is to ensure the spinner is not rendered when the process's output is redirected to a file. You can pass in `True` to the `start` method of the spinner to force it to be rendered regardless, or use the global `force` function. This can be useful when using a program like [`ttyd`](https://github.com/tsl0922/ttyd) or [`vhs`](https://github.com/charmbracelet/vhs).

## LICENSE
[MIT](LICENSE)