Simple print wrapper to add color support to python's print function.

```python
from prozt.prozt import prozt as print
```

# Table of Contents

* [prozt](#prozt)
  * [prozt](#prozt.prozt)
  * [prozt\_rainbow](#prozt.prozt_rainbow)

<a id="prozt"></a>

# prozt

prozt
----------
Simple print wrapper to add color support to python using ANSI color codes

<a id="prozt.prozt"></a>

#### prozt

```python
def prozt(*values: object,
          sep: str | None = " ",
          end: str | None = "\n",
          file=None,
          flush: Literal[False] = False,
          fg_color: str | None = None,
          bg_color: str | None = None,
          style: str | None = None) -> None
```

Print the values to the console with ANSI color support!

**Arguments**:

- `sep` _str | None, optional_ - string inserted between values, default a space.
- `end` _str | None, optional_ - string appended after the last value, default a newline.
- `file` __type_, optional_ - a file-like object (stream), defaults to the current sys.stdout.
- `flush` _Literal[False], optional_ - whether to forcibly flush the stream.
- `fg_color` _str | None, optional_ - ANSI Code for Foreground color of the text. Use colorama.Fore for simple colors.
- `bg_color` _str | None, optional_ - ANSI Code for Background color of the text. Use colorama.Back for simple colors.
- `style` _str | None, optional_ - ANSI Code for Style of the text. Use colorama.Style for simple colors.

<a id="prozt.prozt_rainbow"></a>

#### prozt\_rainbow

```python
def prozt_rainbow(*values: object,
                  sep: str | None = " ",
                  end: str | None = "\n",
                  flush: Literal[False] = False)
```

Print something to the console in style.

**Arguments**:

- `sep` _str | None, optional_ - string inserted between values, default a space.
- `end` _str | None, optional_ - string appended after the last value, default a newline.
- `file` __type_, optional_ - a file-like object (stream), defaults to the current sys.stdout.
- `flush` _Literal[False], optional_ - whether to forcibly flush the stream.

