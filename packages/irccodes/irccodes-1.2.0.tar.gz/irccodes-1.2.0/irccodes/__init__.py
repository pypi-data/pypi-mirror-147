from irccodes import symbols


def colored(text, color, background_color=None, padding=' '):
    text_color_code = getattr(symbols, color.replace(' ', '').upper())
    if background_color is not None:
        background_color_code = ',' + getattr(symbols, background_color.replace(' ', '').upper())
    else:
        background_color_code = ''
    color_code = symbols.COLOR + text_color_code + background_color_code
    return color_code + padding + text + symbols.COLOR


def bold(text):
    return symbols.BOLD + text + symbols.BOLD


def italic(text):
    return symbols.ITALIC + text + symbols.ITALIC


def strikethrough(text):
    return symbols.STRIKETHROUGH + text + symbols.STRIKETHROUGH


def underline(text):
    return symbols.UNDERLINE + text + symbols.UNDERLINE


def monospace(text):
    return symbols.MONOSPACE + text + symbols.MONOSPACE


def reset(text):
    return text + symbols.RESET
