'''This module performs the math operations of the calculator using
brython.
'''

from browser import document
import math

FUNCS = {'exp', 'log2', 'log10',
         'sin', 'cos', 'tan',
         'asin', 'acos', 'atan',
         'gcd'}

sign = False


def deco(func):
    '''A decorator to allow angles in degrees in trigonometric
    functions.
    '''

    def wrapper(x):
        lst = document.select('input[name="angle"]')

        angle = ''
        for ele in lst:
            if ele.checked:
                angle = ele.value

        if angle == 'deg':
            if func.__name__ in ('sin', 'cos', 'tan'):
                y = math.radians(x)
                return func(y)
            elif func.__name__ in ('asin', 'acos', 'atan'):
                y = func(x)
                return math.degrees(y)
        else:
            return func(x)
    return wrapper


sin = deco(math.sin)
cos = deco(math.cos)
tan = deco(math.tan)
asin = deco(math.asin)
acos = deco(math.acos)
atan = deco(math.atan)

LOCALS = {'fact': math.factorial,
          'sin': sin, 'cos': cos, 'tan': tan,
          'asin': asin, 'acos': acos, 'atan': atan
          }


def action(e):
    '''Specifies action to take when any button is pressed.

    It uses 2 variables - `label` and `value` to carry out the action.
    `label` is the label of the button and `value` is the output that
    will appear on the display. It uses `eval` to calculate the value
    of the expression - this is safe in this case because input is
    limited to the buttons on the keypad.
    '''

    inp = document.select('#calc>input')[0]
    display = value = inp.value
    if value == '0':
        value = ''

    if e.target.tagName == 'SUP':
        target = e.target.parent
    else:
        target = e.target

    label = target.textContent

    if label != '+/-':
        sign = False

    if label == 'func':
        change_pad('func')
        return
    elif label == 'Back':
        change_pad('back')
        return

    if label == '=':
        try:
            res = eval(display, vars(math), LOCALS)
            value = format_result(res)
        except Exception:
            value = 'Error'
    elif label == 'C':
        value = '0'
    elif label == '\u21d0':
        if len(display) > 1:
            value = display[:-1]
        else:
            value = '0'
    elif label in ('+', '-', '*', '/'):
        value = display + label
    elif label == '+/-':
        global sign
        if not sign:
            value += '-'
            sign = True
        else:
            sign = False
            if len(display) > 1:
                value = display[:-1]
            else:
                value = '0'
    elif label == '.':
        value = display + label
    elif label == 'x2':
        value = display + '**2'
    elif label == '\u221a':
        value += 'sqrt('
    elif label == 'xy':
        value = display + '**'
    elif label == '1/x':
        value += '1/'
    elif label == '\u03c0':
        value += 'pi'
    elif label == '!':
        value += 'fact('
    elif label == 'ln':
        value += 'log('
    elif label == 'mod':
        value = display + '%'
    elif label == 'div':
        value = display + '//'
    elif label in FUNCS:
        value += label + '('
    else:
        value += label

    inp.title = inp.value = value[:80]

    if label not in ('func', 'Back'):
        if label != '=':
            inp.scrollLeft = inp.scrollWidth
        else:
            inp.scrollLeft = 0


def format_result(res):
    '''Format the result as an integer or floating-point number. Use
    exponent notation if it is too large. Note that very small numbers
    seem to be taken care of by `eval`.
    '''

    num = int(res)
    if num == res:
        if res < pow(10, 12):
            value = str(res)
        else:
            value = format(res, 'g')
    else:
        res = round(res, 10)
        if res < pow(10, 10):
            value = str(res)
        else:
            value = format(res, 'g')

    return value


def change_pad(to):
    '''Show the main buttons or the math function buttons.'''

    main_pad = document['main-buttons']
    math_pad = document['math-buttons']

    if to == 'func':
        main_pad.style.display = 'none'
        math_pad.style.display = 'flex'
    else:
        main_pad.style.display = 'flex'
        math_pad.style.display = 'none'


def convert(e):
    '''Convert radians to degrees or vice versa.'''

    inp = document.select('#calc>input')[0]

    if inp.value != '0':
        try:
            angle = float(inp.value)
        except Exception:
            pass
        else:
            if e.target.value == 'rad':
                rad = round(math.radians(angle), 10)
                inp.title = inp.value = str(rad)
            else:
                deg = round(math.degrees(angle), 10)
                inp.title = inp.value = str(deg)
            inp.scrollLeft = 0


for button in document.select('button'):
    button.bind('click', action)

for radio in document.select('input[type="radio"]'):
    radio.bind('change', convert)
