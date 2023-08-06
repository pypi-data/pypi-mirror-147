# IRC codes

## Usage:

### Text format:

```python
from irccodes import *

# Functional method:
bold(str)
italic(str)
strikethrough(str)
underline(str)
monospace(str)
reset(str)

# Concatenation method:
symbols.BOLD + str
symbols.ITALIC + str
symbols.STRIKETHROUGH + str
symbols.underline + str
symbols.MONOSPACE + str
symbols.RESET + str
```

### Text colors:
```python
colored(str, text_color, background_color)
symbols.COLOR + symbols.<COLOR NAME> + ',' + symbols.<BACKGROUND COLOR NAME> + str
```

Examples:
```python
colored(text, 'blue')
colored(text, 'light green', 'grey')
bold(colored('first', 'white') + ' ' + colored('second', 'grey'))
symbols.COLOR + symbols.BLUE + ',' + symbols.LIGHTRED + text
text + symbols.RESET
reset(text)
```

Supported colors:

| Index | Color       | RGB           |
|-------|-------------|---------------|
| 0     | White       | (255,255,255) |
| 1     | Black       | (0,0,0)       |
| 2     | Blue        | (0,0,127)     |
| 3     | Green       | (0,147,0)     |
| 4     | Light Red   | (255,0,0)     |
| 5     | Brown       | (127,0,0)     |
| 6     | Purple      | (156,0,156)   |
| 7     | Orange      | (252,127,0)   |
| 8     | Yellow      | (255,255,0)   |
| 9     | Light Green | (0,252,0)     |
| 10    | Cyan        | (0,147,147)   |
| 11    | Light Cyan  | (0,255,255)   |
| 12    | Light Blue  | (0,0,252)     |
| 13    | Pink        | (255,0,255)   |
| 14    | Grey        | (127,127,127) |
| 15    | Light Grey  | (210,210,210) |

## More detailed:
https://www.mirc.com/colors.html

https://stackoverflow.com/questions/1391610/embed-mirc-color-codes-into-a-c-sharp-literal