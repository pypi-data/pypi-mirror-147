"""
Creds to Rapptz for this whole file
"""
import re
import unicodedata

_IS_ASCII = re.compile(r'^[\x00-\x7f]+$')


def _string_width(string: str, *, _IS_ASCII=_IS_ASCII) -> int:
    """Returns string's width."""
    match = _IS_ASCII.match(string)
    if match:
        return match.endpos

    UNICODE_WIDE_CHAR_TYPE = 'WFA'
    func = unicodedata.east_asian_width
    return sum(2 if func(char) in UNICODE_WIDE_CHAR_TYPE else 1 for char in string)


def get_max_size(commands):
    as_lengths = (_string_width(command['name'] + "|".join(command['aliases']) + make_sig(command['params'])) for command in commands)
    return max(as_lengths, default=0)


def shorten_text(text, width):
    if len(text) > width:
        return text[: width - 3].rstrip() + '...'
    return text

# I made this
def make_sig(params):
    params = params[1:] # Remove ctx
    if '*' in params:
        params.remove("*")

    optional = []
    required = []

    for param in params:
        if "=" in param:
            optional.append(param.split("=")[0])

        else:
            required.append(param)

    sig = ""
    for param in params:
        req = [p for p in required if p == param]
        if bool(req):
            sig += f" ({req[0]})"
            continue

        sig += f" [{param.split('=')[0]}]"

    return sig

        

    


def mk_help(commands, prefix):
    help_ = []
    max_size = get_max_size(commands)
    if not isinstance(prefix, str):
        prefix = prefix()

    for command in commands:
        name = prefix + command['name'] + ["|" if bool(command['aliases']) else ""][0] + "|".join(command['aliases']) + make_sig(command['params'])
        width = max_size - (_string_width(name) - len(name))
        entry = f"`{name:<{width}} +{'=' * ((max_size - len(name)) + 11)}+ {command['description']}`"
        help_.append(entry)

    return "\n\n".join(help_) + "\n\n`() = Required | [] = Optional`"
