"""PosteRazor API
By Al Sweigart al@inventwithpython.com

A Python module that can controls the mouse & keyboard to automate PosteRazor for Windows."""

__version__ = '0.1.0'

import os
import math

import pyautogui
import pyperclip

class PosteRazorAPIException(Exception):
    """The base exception class for PosteRazor API."""
    pass

def produceAll(imageFilename, minPaperUsage=0.75, maxPages=36):
    load(imageFilename)

    portrait()
    for widthPages in range(math.ceil(math.sqrt(maxPages))):
        sizePages((widthPages, None))
        w, h = sizePages()
        if w * math.ceil(h) > maxPages:
            continue
        if h % 1 < minPaperUsage:
            continue

        pdfFilename = imageFilename[:imageFilename.rfind('.')]
        pdfFilename += '_' + str(int(math.ceil(w))) + 'x' + str(int(math.ceil(h))) + '.pdf'
        saveAs(pdfFilename)

    landscape()
    for widthPages in range(math.ceil(math.sqrt(maxPages))):
        sizePages((widthPages, None))
        w, h = sizePages()
        if math.ceil(w) * h > maxPages:
            continue
        if w % 1 < minPaperUsage:
            continue

        pdfFilename = imageFilename[:imageFilename.rfind('.')]
        pdfFilename += '_' + str(int(math.ceil(w))) + 'x' + str(int(math.ceil(h))) + '.pdf'
        saveAs(pdfFilename)



def createThumbnail(imageFilename):
    pass


def load(imageFilename):
    if not os.path.exists(imageFilename):
        raise PosteRazorAPIException('File not found: ' + imageFilename)

    _gotoStep(1)
    _clickAt(0.935, 0.225)  # Click the Load button.
    pyautogui.sleep(0.25)
    pyautogui.write(imageFilename + '\n')
    pyautogui.sleep(0.25)



def paperSize(value=None):
    _gotoStep(2)
    _clickAt(0.68, 0.23)  # Click the Custom button.

    _clickAt(0.69, 0.33)  # Click the width field.
    _clickAt(0.69, 0.33)  # Click the width field.
    returnSize = []
    if value is None:
        # Copy the width to the clipboard.
        pyautogui.sleep(0.25)
        pyautogui.hotkey('ctrl', 'c')
        pyautogui.sleep(0.1)
        returnSize.append(float(pyperclip.paste()))
    else:
        if value[0] is not None:
            pyautogui.write('\b' + str(value[0]))

    _clickAt(0.69, 0.41)  # Click the height field.
    _clickAt(0.69, 0.41)  # Click the height field.
    if value is None:
        # Copy the height to the clipboard.
        pyautogui.sleep(0.25)
        pyautogui.hotkey('ctrl', 'c')
        pyautogui.sleep(0.1)
        returnSize.append(float(pyperclip.paste()))
        return tuple(returnSize)
    else:
        if value[1] is not None:
            pyautogui.write('\b' + str(value[1]))


def borders(value=None):
    pass


def landscape():
    _gotoStep(2)
    _clickAt(0.75, 0.43)


def portrait():
    _gotoStep(2)
    _clickAt(0.75, 0.38)


def overlap(value=None):
    pass


def overlappingPosition(value=None):
    pass


def sizeAbsolute(value=None):
    pass


def sizePages(value=None):
    _gotoStep(4)
    _clickAt(0.55, 0.42)  # Click the "Size in pages" button.

    _clickAt(0.70, 0.48)  # Click the width field.
    _clickAt(0.70, 0.48)  # Click the width field.
    returnSize = []
    if value is None:
        # Copy the width to the clipboard.
        pyautogui.sleep(0.25)
        pyautogui.hotkey('ctrl', 'c')
        pyautogui.sleep(0.1)
        returnSize.append(float(pyperclip.paste()))
    else:
        if value[0] is not None:
            pyautogui.write('\b' + str(value[0]))

    _clickAt(0.70, 0.54)  # Click the height field.
    _clickAt(0.70, 0.54)  # Click the height field.
    if value is None:
        # Copy the height to the clipboard.
        pyautogui.sleep(0.25)
        pyautogui.hotkey('ctrl', 'c')
        pyautogui.sleep(0.1)
        returnSize.append(float(pyperclip.paste()))
        return tuple(returnSize)
    else:
        if value[1] is not None:
            pyautogui.write('\b' + str(value[1]))


def sizePercent(value=None):
    pass


def valignment(value=None):
    pass


def halignment(value=None):
    pass


def saveAs(pdfFilename):
    alreadyExists = os.path.exists(pdfFilename)

    _gotoStep(5)
    _clickAt(0.74, 0.25)  # Click the Save button.

    pyautogui.sleep(0.25)
    pyautogui.write(pdfFilename + '\n')
    pyautogui.sleep(0.25)

    if alreadyExists:
        pyautogui.press('tab')
        pyautogui.press('\n')
        pyautogui.sleep(0.25)


def _clickAt(xPercent, yPercent):
    postWin = _getPosteRazorWindow()
    x = (postWin.size[0] * xPercent) + postWin.left
    y = (postWin.size[1] * yPercent) + postWin.top
    pyautogui.click(x, y)

def _clickNext():
    _clickAt(0.87, 0.93)


def _clickPrev():
    _clickAt(0.70, 0.93)



def _gotoStep(stepNumber):
    for i in range(5):
        _clickPrev()
    for i in range(stepNumber - 1):
        _clickNext()


def _getPosteRazorWindow():
    # Find the PosteRazor window.
    posterazorWindows = [title for title in pyautogui.getAllTitles() if title.startswith('PosteRazor ')]
    if len(posterazorWindows) == 0:
        raise PosteRazorAPIException('Could not find the window for PosteRazor. Please run PosteRazor.')
    elif len(posterazorWindows) > 1:
        raise PosteRazorAPIException(str(len(posterazorWindows)) + ' instances of PosteRazor found. Please run only one instance of PosteRazor.')

    postWin = pyautogui.getWindowsWithTitle(posterazorWindows[0])[0]

    # Resize and focus the window.
    postWin.resizeTo(1, 1) # Set the size of PosteRazor to its smallest size.
    postWin.activate()
    return postWin