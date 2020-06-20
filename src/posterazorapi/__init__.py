"""PosteRazor API
By Al Sweigart al@inventwithpython.com

A Python module that can controls the mouse & keyboard to automate PosteRazor for Windows."""

__version__ = '0.1.0'

import pyautogui
import pyperclip
import PIL

class PosteRazorAPIException(Exception):
    """The base exception class for PosteRazor API."""
    pass

def produceAll(imageFilename, minPaperUsage=0.75, maxPages=36):
    pass


def load(imageFilename):
    pass

@property
def paperSize():
    pass

@paperSize.setter
def paperSize(value):
    pass


@property
def borders():
    pass

@borders.setter
def borders(value):
    pass


def setLandscape():
    pass


def setPortrait():
    pass


@property
def overlap():
    pass

@overlap.setter
def overlap(value):
    pass


@property
def overlappingPosition():
    pass

@overlappingPosition.setter
def overlappingPosition(value):
    pass


@property
def absoluteWidth():
    pass

@absoluteWidth.setter
def absoluteWidth(value):
    pass


@property
def absoluteHeight():
    pass

@absoluteHeight.setter
def absoluteHeight(value):
    pass


@property
def pageWidth():
    pass

@pageWidth.setter
def pageWidth(value):
    pass


@property
def pageHeight():
    pass

@pageHeight.setter
def pageHeight(value):
    pass


@property
def sizePercent():
    pass

@sizePercent.setter
def sizePercent(value):
    pass


@property
def valignment():
    pass

@valignment.setter
def valignment(value):
    pass


@property
def halignment():
    pass

@halignment.setter
def halignment(value):
    pass


def saveAs(pdfFilename):
    pass


def _clickNext():
    postWin = _getPosteRazorWindow()
    nextX = (postWin.size[0] * 0.87) + postWin.left
    prevNextY = (postWin.size[1] * 0.93) + postWin.top
    pyautogui.click(nextX, prevNextY)



def _clickPrev():
    postWin = _getPosteRazorWindow()
    prevX = (postWin.size[0] * 0.70) + postWin.left
    prevNextY = (postWin.size[1] * 0.93) + postWin.top
    pyautogui.click(prevX, prevNextY)



def _gotoStep(stepNumber):
    for i in range(5):
        _clickPrev()
    for i in range(stepNumber - 1):
        _clickNext()


def _getPosteRazorWindow():
    posterazorWindows = [title for title in pyautogui.getAllTitles() if title.startswith('PosteRazor ')]
    if len(posterazorWindows) == 0:
        raise PosteRazorAPIException('Could not find the window for PosteRazor. Please run PosteRazor.')
    elif len(posterazorWindows) > 1:
        raise PosteRazorAPIException(str(len(posterazorWindows)) + ' instances of PosteRazor found. Please run only one instance of PosteRazor.')

    postWin = pyautogui.getWindowsWithTitle(posterazorWindows[0])[0]
    postWin.resizeTo(1, 1) # Set the size of PosteRazor to its smallest size.
    postWin.activate()
    return postWin