import ctypes
import functools
import inspect
import time
import pyautogui

SendInput = ctypes.windll.user32.SendInput
MapVirtualKey = ctypes.windll.user32.MapVirtualKeyW

# Constants for failsafe check and pause

FAILSAFE = True
FAILSAFE_POINTS = [(0, 0)]
PAUSE = 0.1  # Tenth-second pause by default.

# Constants for the mouse button names
LEFT = "left"
MIDDLE = "middle"
RIGHT = "right"
PRIMARY = "primary"
SECONDARY = "secondary"

# Mouse Scan Code Mappings
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_LEFTCLICK = MOUSEEVENTF_LEFTDOWN + MOUSEEVENTF_LEFTUP
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_RIGHTCLICK = MOUSEEVENTF_RIGHTDOWN + MOUSEEVENTF_RIGHTUP
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040
MOUSEEVENTF_MIDDLECLICK = MOUSEEVENTF_MIDDLEDOWN + MOUSEEVENTF_MIDDLEUP

# KeyBdInput Flags
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_SCANCODE = 0x0008
KEYEVENTF_UNICODE = 0x0004

# MapVirtualKey Map Types
MAPVK_VK_TO_CHAR = 2
MAPVK_VK_TO_VSC = 0
MAPVK_VSC_TO_VK = 1
MAPVK_VSC_TO_VK_EX = 3

# Keyboard Scan Code Mappings
keyboardMapping = dict([(key, None) for key in pyautogui.KEY_NAMES])
keyboardMapping.update({
    'backspace': 0x0E,  # SC_BACK
    '\b': 0x0E,  # SC_BACK
    'super': 0xDB + 1024,  # SC_LWIN
    'tab': 0x0F,  # SC_TAB
    '\t': 0x0F,  # SC_TAB
    'enter': 0x1C,  # SC_RETURN
    '\n': 0x1C,  # SC_RETURN
    'return': 0x1C,  # SC_RETURN
    'shift': 0x2A,  # SC_SHIFT
    'ctrl': 0x1D,  # SC_CONTROL
    'alt': 0x38,  # SC_MENU
    'capslock': 0x3A,  # SC_CAPITAL
    'esc': 0x01,  # SC_ESCAPE
    'escape': 0x01,  # SC_ESCAPE
    'convert': 0x79,  # SC_CONVERT
    'nonconvert': 0x7B,  # SC_NONCONVERT
    ' ': 0x39,  # SC_SPACE
    'space': 0x39,  # SC_SPACE
    'pgup': 0xC9 + 1024,  # SC_PRIOR
    'pgdn': 0xD1 + 1024,  # SC_NEXT
    'pageup': 0xC9 + 1024,  # SC_PRIOR
    'pagedown': 0xD1 + 1024,  # SC_NEXT
    'end': 0xCF + 1024,  # SC_END
    'home': 0xC7 + 1024,  # SC_HOME
    'left': 0xCB + 1024,  # SC_LEFT
    'up': 0xC8 + 1024,  # SC_UP
    'right': 0xCD + 1024,  # SC_RIGHT
    'down': 0xD0 + 1024,  # SC_DOWN
    'prtsc': 0xB7 + 1024,  # SC_SNAPSHOT
    'prtscr': 0xB7 + 1024,  # SC_SNAPSHOT
    'prntscrn': 0xB7 + 1024,  # SC_SNAPSHOT
    'printscreen': 0xB7 + 1024,  # SC_SNAPSHOT
    'insert': 0xD2 + 1024,  # SC_INSERT
    'del': 0xD3 + 1024,  # SC_DELETE
    'delete': 0xD3 + 1024,  # SC_DELETE
    'help': 0x63,  # SC_HELP
    'win': 0xDB + 1024,  # SC_LWIN
    'winleft': 0xDB + 1024,  # SC_LWIN
    'winright': 0xDC + 1024,  # SC_RWIN
    'apps': 0xDD + 1024, # SC_APPS
    'sleep': 0xDF + 1024, # SC_SLEEP
    'num0': 0x52,  # SC_NUMPAD0
    'num1': 0x4F,  # SC_NUMPAD1
    'num2': 0x50,  # SC_NUMPAD2
    'num3': 0x51,  # SC_NUMPAD3
    'num4': 0x4B,  # SC_NUMPAD4
    'num5': 0x4C,  # SC_NUMPAD5
    'num6': 0x4D,  # SC_NUMPAD6
    'num7': 0x47,  # SC_NUMPAD7
    'num8': 0x48,  # SC_NUMPAD8
    'num9': 0x49,  # SC_NUMPAD9
    'multiply': 0x37,  # SC_MULTIPLY numpad *
    'add': 0x4E,  # SC_ADD numpad +
    'subtract': 0x4A,  # SC_SUBTRACT numpad -
    'decimal': 0x53,  # SC_DECIMAL
    'divide': 0xB5 + 1024,  # SC_DIVIDE
    'numenter': 0x9C + 1024,  # SC_NUMPADENTER
    'f1': 0x3B,  # SC_F1
    'f2': 0x3C,  # SC_F2
    'f3': 0x3D,  # SC_F3
    'f4': 0x3E,  # SC_F4
    'f5': 0x3F,  # SC_F5
    'f6': 0x40,  # SC_F6
    'f7': 0x41,  # SC_F7
    'f8': 0x42,  # SC_F8
    'f9': 0x43,  # SC_F9
    'f10': 0x44,  # SC_F10
    'f11': 0x57,  # SC_F11
    'f12': 0x58,  # SC_F12
    'f13': 0x64,  # SC_F13
    'f14': 0x65,  # SC_F14
    'f15': 0x66,  # SC_F15
    'f16': 0x67,  # SC_F16
    'f17': 0x68,  # SC_F17
    'f18': 0x69,  # SC_F18
    'f19': 0x6a,  # SC_F19
    'f20': 0x6b,  # SC_F20
    'f21': 0x6c,  # SC_F21
    'f22': 0x6d,  # SC_F22
    'f23': 0x6e,  # SC_F23
    'f24': 0x76,  # SC_F24
    'numlock': 0x45,  # SC_NUMLOCK
    'scrolllock': 0x46,  # SC_SCROLL
    'shiftleft': 0x2A,  # SC_LSHIFT
    'shiftright': 0x36,  # SC_RSHIFT
    'ctrlleft': 0x1D,  # SC_LCONTROL
    'ctrlright': 0x9D + 1024,  # SC_RCONTROL
    'altleft': 0x38,  # SC_LMENU
    'altright': 0xB8 + 1024,  # SC_RMENU
    'browserback': 0xEA + 1024,  # SC_BROWSER_BACK
    'browserforward': 0xE9 + 1024,  # SC_BROWSER_FORWARD
    'browserrefresh': 0xE7 + 1024,  # SC_BROWSER_REFRESH
    'browserstop': 0xE8 + 1024,  # SC_BROWSER_STOP
    'browsersearch': 0xE5 + 1024,  # SC_BROWSER_SEARCH
    'browserfavorites': 0xE6 + 1024,  # SC_BROWSER_FAVORITES
    'browserhome': 0xB2 + 1024,  # SC_BROWSER_HOME
    'volumemute': 0xA0 + 1024,  # SC_VOLUME_MUTE
    'volumedown': 0xAE + 1024,  # SC_VOLUME_DOWN
    'volumeup': 0xB0 + 1024,  # SC_VOLUME_UP
    'nexttrack': 0x99 + 1024,  # SC_MEDIA_NEXT_TRACK
    'prevtrack': 0x90 + 1024,  # SC_MEDIA_PREV_TRACK
    'stop': 0xA4 + 1024,  # SC_MEDIA_STOP
    'playpause': 0xA2 + 1024,  # SC_MEDIA_PLAY_PAUSE
    'launchmail': 0xEC + 1024,  # SC_LAUNCH_MAIL
    'launchmediaselect': 0xED + 1024,  # SC_LAUNCH_MEDIA_SELECT
    'launchapp1': 0xEB + 1024,  # SC_LAUNCH_APP1
    'launchapp2': 0xA1 + 1024,  # SC_LAUNCH_APP2
    "'": 0x28,
    '-': 0x0C,
    ',': 0x33,
    '.': 0x34,
    '/': 0x35,
    ';': 0x27,
    '[': 0x1A,
    '\\': 0x2B,
    ']': 0x1B,
    '`': 0x29,
    '=': 0x0D,
    '0': 0x0B,
    '1': 0x02,
    '2': 0x03,
    '3': 0x04,
    '4': 0x05,
    '5': 0x06,
    '6': 0x07,
    '7': 0x08,
    '8': 0x09,
    '9': 0x0A,
    'a': 0x1E,
    'b': 0x30,
    'c': 0x2E,
    'd': 0x20,
    'e': 0x12,
    'f': 0x21,
    'g': 0x22,
    'h': 0x23,
    'i': 0x17,
    'j': 0x24,
    'k': 0x25,
    'l': 0x26,
    'm': 0x32,
    'n': 0x31,
    'o': 0x18,
    'p': 0x19,
    'q': 0x10,
    'r': 0x13,
    's': 0x1F,
    't': 0x14,
    'u': 0x16,
    'v': 0x2F,
    'w': 0x11,
    'x': 0x2D,
    'y': 0x15,
    'z': 0x2C,
    '"': 0x28,
    '_': 0x0C,
    '<': 0x33,
    '>': 0x34,
    '?': 0x35,
    ':': 0x27,
    '{': 0x1A,
    '|': 0x2B,
    '}': 0x1B,
    '~': 0x29,
    '+': 0x0D,
    ')': 0x0B,
    '!': 0x02,
    '@': 0x03,
    '#': 0x04,
    '$': 0x05,
    '%': 0x06,
    '^': 0x07,
    '&': 0x08,
    '*': 0x09,
    '(': 0x0A,
    'A': 0x1E,
    'B': 0x30,
    'C': 0x2E,
    'D': 0x20,
    'E': 0x12,
    'F': 0x21,
    'G': 0x22,
    'H': 0x23,
    'I': 0x17,
    'J': 0x24,
    'K': 0x25,
    'L': 0x26,
    'M': 0x32,
    'N': 0x31,
    'O': 0x18,
    'P': 0x19,
    'Q': 0x10,
    'R': 0x13,
    'S': 0x1F,
    'T': 0x14,
    'U': 0x16,
    'V': 0x2F,
    'W': 0x11,
    'X': 0x2D,
    'Y': 0x15,
    'Z': 0x2C,
})

# C struct redefinitions

PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long),
                ("y", ctypes.c_long)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


# Fail Safe and Pause implementation

class FailSafeException(Exception):
    pass


def failSafeCheck():
    if FAILSAFE and tuple(position()) in FAILSAFE_POINTS:
        raise FailSafeException(
            "PyDirectInput fail-safe triggered from mouse moving to a corner of the screen. To disable this " \
                "fail-safe, set pydirectinput.FAILSAFE to False. DISABLING FAIL-SAFE IS NOT RECOMMENDED."
        )


def _handlePause(_pause):
    if _pause:
        assert isinstance(PAUSE, int) or isinstance(PAUSE, float)
        time.sleep(PAUSE)


# direct copy of _genericPyAutoGUIChecks()
def _genericPyDirectInputChecks(wrappedFunction):

    @functools.wraps(wrappedFunction)
    def wrapper(*args, **kwargs):
        funcArgs = inspect.getcallargs(wrappedFunction, *args, **kwargs)

        failSafeCheck()
        returnVal = wrappedFunction(*args, **kwargs)
        _handlePause(funcArgs.get("_pause"))
        return returnVal

    return wrapper


# Helper Functions

def _to_windows_coordinates(x=0, y=0):
    display_width, display_height = size()

    # the +1 here prevents exactly mouse movements from sometimes ending up off by 1 pixel
    windows_x = (x * 65536) // display_width + 1
    windows_y = (y * 65536) // display_height + 1

    return windows_x, windows_y


# position() works exactly the same as PyAutoGUI. I've duplicated it here so that moveRel() can use it to calculate
# relative mouse positions.
def position(x=None, y=None):
    cursor = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(cursor))
    return (x if x else cursor.x, y if y else cursor.y)


# size() works exactly the same as PyAutoGUI. I've duplicated it here so that _to_windows_coordinates() can use it 
# to calculate the window size.
def size():
    return (ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))


# Main Mouse Functions

# Ignored parameters: duration, tween, logScreenshot
@_genericPyDirectInputChecks
def mouseDown(x=None, y=None, button=PRIMARY, duration=None, tween=None, logScreenshot=None, _pause=True):

    if not x is None or not y is None:
        moveTo(x, y)

    ev = None
    if button == PRIMARY or button == LEFT:
        ev = MOUSEEVENTF_LEFTDOWN
    elif button == MIDDLE:
        ev = MOUSEEVENTF_MIDDLEDOWN
    elif button == SECONDARY or button == RIGHT:
        ev = MOUSEEVENTF_RIGHTDOWN

    if not ev:
        raise ValueError('button arg to _click() must be one of "left", "middle", or "right", not %s' % button)

    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(0, 0, 0, ev, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(0), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


# Ignored parameters: duration, tween, logScreenshot
@_genericPyDirectInputChecks
def mouseUp(x=None, y=None, button=PRIMARY, duration=None, tween=None, logScreenshot=None, _pause=True):
    
    if not x is None or not y is None:
        moveTo(x, y)

    ev = None
    if button == PRIMARY or button == LEFT:
        ev = MOUSEEVENTF_LEFTUP
    elif button == MIDDLE:
        ev = MOUSEEVENTF_MIDDLEUP
    elif button == SECONDARY or button == RIGHT:
        ev = MOUSEEVENTF_RIGHTUP

    if not ev:
        raise ValueError('button arg to _click() must be one of "left", "middle", or "right", not %s' % button)

    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(0, 0, 0, ev, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(0), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


# Ignored parameters: duration, tween, logScreenshot
@_genericPyDirectInputChecks
def click(x=None, y=None, clicks=1, interval=0.0, button=PRIMARY, duration=None, tween=None, logScreenshot=None, _pause=True):
    
    if not x is None or not y is None:
        moveTo(x, y)

    ev = None
    if button == PRIMARY or button == LEFT:
        ev = MOUSEEVENTF_LEFTCLICK
    elif button == MIDDLE:
        ev = MOUSEEVENTF_MIDDLECLICK
    elif button == SECONDARY or button == RIGHT:
        ev = MOUSEEVENTF_RIGHTCLICK

    if not ev:
        raise ValueError('button arg to _click() must be one of "left", "middle", or "right", not %s' % button)

    for i in range(clicks):
        failSafeCheck()
        
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.mi = MouseInput(0, 0, 0, ev, 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(0), ii_)
        SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

        time.sleep(interval)


def leftClick(x=None, y=None, interval=0.0, duration=0.0, tween=None, logScreenshot=None, _pause=True):
    click(x, y, 1, interval, LEFT, duration, tween, logScreenshot, _pause)


def rightClick(x=None, y=None, interval=0.0, duration=0.0, tween=None, logScreenshot=None, _pause=True):
    click(x, y, 1, interval, RIGHT, duration, tween, logScreenshot, _pause)


def middleClick(x=None, y=None, interval=0.0, duration=0.0, tween=None, logScreenshot=None, _pause=True):
    click(x, y, 1, interval, MIDDLE, duration, tween, logScreenshot, _pause)


def doubleClick(x=None, y=None, interval=0.0, button=LEFT, duration=0.0, tween=None, logScreenshot=None, _pause=True):
    click(x, y, 2, interval, button, duration, tween, logScreenshot, _pause)


def tripleClick(x=None, y=None, interval=0.0, button=LEFT, duration=0.0, tween=None, logScreenshot=None, _pause=True):
    click(x, y, 3, interval, button, duration, tween, logScreenshot, _pause)


# Missing feature: scroll functions


# Ignored parameters: duration, tween, logScreenshot
# PyAutoGUI uses ctypes.windll.user32.SetCursorPos(x, y) for this, which might still work fine in DirectInput 
# environments.
@_genericPyDirectInputChecks
def moveTo(x=None, y=None, duration=None, tween=None, logScreenshot=False, _pause=True):
    x, y = position(x, y)  # if only x or y is provided, will keep the current position for the other axis
    x, y = _to_windows_coordinates(x, y)
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(x, y, 0, (MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE), 0, ctypes.pointer(extra))
    command = Input(ctypes.c_ulong(0), ii_)
    SendInput(1, ctypes.pointer(command), ctypes.sizeof(command))


# Ignored parameters: duration, tween, logScreenshot
# move() and moveRel() are equivalent
@_genericPyDirectInputChecks
def moveRel(xOffset=None, yOffset=None, duration=None, tween=None, logScreenshot=False, _pause=True):
    x, y = position()
    if xOffset is None:
        xOffset = 0
    if yOffset is None:
        yOffset = 0
    moveTo(x + xOffset, y + yOffset)
    # We cannot simply use MOUSEEVENTF_MOVE for relative movement, as the results are inconsistent.
    # "Relative mouse motion is subject to the effects of the mouse speed and the two-mouse threshold values. A user 
    # sets these three values with the Pointer Speed slider of the Control Panel's Mouse Properties sheet. You can 
    # obtain and set these values using the SystemParametersInfo function." 
    # https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-mouseinput
    # https://stackoverflow.com/questions/50601200/pyhon-directinput-mouse-relative-moving-act-not-as-expected
    # extra = ctypes.c_ulong(0)
    # ii_ = Input_I()
    # ii_.mi = MouseInput(xOffset, yOffset, 0, MOUSEEVENTF_MOVE, 0, ctypes.pointer(extra))
    # command = Input(ctypes.c_ulong(0), ii_)
    # SendInput(1, ctypes.pointer(command), ctypes.sizeof(command))
move = moveRel


# Missing feature: drag functions


# Keyboard Functions


# Ignored parameters: logScreenshot
# Missing feature: auto shift for special characters (ie. '!', '@', '#'...)
@_genericPyDirectInputChecks
def keyDown(key, logScreenshot=None, _pause=True):
    if not key in keyboardMapping or keyboardMapping[key] is None:
        return 

    keybdFlags = KEYEVENTF_SCANCODE

    # arrow keys need the extended key flag
    if key in ['up', 'left', 'down', 'right']:
        keybdFlags |= KEYEVENTF_EXTENDEDKEY
        # if numlock is on and an arrow key is being pressed, we need to send an additional scancode
        # https://stackoverflow.com/questions/14026496/sendinput-sends-num8-when-i-want-to-send-vk-up-how-come
        # https://handmade.network/wiki/2823-keyboard_inputs_-_scancodes,_raw_input,_text_input,_key_names
        if ctypes.windll.user32.GetKeyState(0x90):
            hexKeyCode = 0xE0
            extra = ctypes.c_ulong(0)
            ii_ = Input_I()
            ii_.ki = KeyBdInput(0, hexKeyCode, KEYEVENTF_SCANCODE, 0, ctypes.pointer(extra))
            x = Input( ctypes.c_ulong(1), ii_)
            SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

    hexKeyCode = keyboardMapping[key]
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, keybdFlags, 0, ctypes.pointer(extra))
    x = Input( ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


# Ignored parameters: logScreenshot
# Missing feature: auto shift for special characters (ie. '!', '@', '#'...)
@_genericPyDirectInputChecks
def keyUp(key, logScreenshot=None, _pause=True):
    if not key in keyboardMapping or keyboardMapping[key] is None:
        return 

    keybdFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP

    # arrow keys need the extended key flag
    if key in ['up', 'left', 'down', 'right']:
        keybdFlags |= KEYEVENTF_EXTENDEDKEY

    hexKeyCode = keyboardMapping[key]
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, keybdFlags, 0, ctypes.pointer(extra))
    x = Input( ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

    # if numlock is on and an arrow key is being pressed, we need to send an additional scancode
    # https://stackoverflow.com/questions/14026496/sendinput-sends-num8-when-i-want-to-send-vk-up-how-come
    # https://handmade.network/wiki/2823-keyboard_inputs_-_scancodes,_raw_input,_text_input,_key_names
    if key in ['up', 'left', 'down', 'right'] and ctypes.windll.user32.GetKeyState(0x90):
        hexKeyCode = 0xE0
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput(0, hexKeyCode, KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP, 0, ctypes.pointer(extra))
        x = Input( ctypes.c_ulong(1), ii_)
        SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

# Ignored parameters: logScreenshot
# nearly identical to PyAutoGUI's implementation
@_genericPyDirectInputChecks
def press(keys, presses=1, interval=0.0, logScreenshot=None, _pause=True):
    if type(keys) == str:
        if len(keys) > 1:
            keys = keys.lower()
        keys = [keys] # If keys is 'enter', convert it to ['enter'].
    else:
        lowerKeys = []
        for s in keys:
            if len(s) > 1:
                lowerKeys.append(s.lower())
            else:
                lowerKeys.append(s)
        keys = lowerKeys
    interval = float(interval)
    for i in range(presses):
        for k in keys:
            failSafeCheck()
            keyDown(k)
            keyUp(k)
        time.sleep(interval)


# Ignored parameters: logScreenshot
# nearly identical to PyAutoGUI's implementation
@_genericPyDirectInputChecks
def typewrite(message, interval=0.0, logScreenshot=None, _pause=True):
    interval = float(interval)
    for c in message:
        if len(c) > 1:
            c = c.lower()
        press(c, _pause=False)
        time.sleep(interval)
        failSafeCheck()
write = typewrite


# Missing feature: hotkey functions
