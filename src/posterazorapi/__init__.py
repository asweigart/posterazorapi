"""PosteRazor API
By Al Sweigart al@inventwithpython.com

A Python module that can controls the mouse & keyboard to automate PosteRazor for Windows."""

__version__ = '0.1.0'

import os
import math
from pathlib import Path
import logging


logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s -  %(levelname)s -  %(message)s')

import pyautogui
import pyperclip
from PIL import Image

pyautogui.PAUSE = 0.2

LANDSCAPE = 'landscape'
PORTRAIT = 'portrait'

class PosteRazorAPIException(Exception):
    """The base exception class for PosteRazor API."""
    pass


def run(imageFilename, maxPaperWastedPercentage=20, maxPages=36, runPngout=False, maxSinglePageWastedPercentage=40):
    imagePath = Path(imageFilename).absolute()
    imageAbsFilename = str(imagePath)
    loadImage(imageAbsFilename)

    im = Image.open(imageAbsFilename)
    imWidth, imHeight = im.size

    if runPngout:
        logging.debug('Running pngout ' + imageAbsFilename)
        os.system('pngout ' + imageAbsFilename)

    #LETTER_SIZE_ASPECT_RATIO = 8.5 / 11.0
    #imageAspectRatio = imWidth / imHeight

    #if imageAspectRatio > LETTER_SIZE_ASPECT_RATIO:
    if imWidth > imHeight:
        setToLandscape()
        orientation = LANDSCAPE
    else:
        setToPortrait()
        orientation = PORTRAIT


    for numPages in range(1, math.ceil(math.sqrt(maxPages)) + 1):
        setSizeInPages((numPages, None))
        w, h = getSizeInPages()
        totalSizeInPages = w * math.ceil(h)

        logging.debug('Size in pages: %s x %s (%s x %s)' % (w, int(math.ceil(h)), w, h))
        if totalSizeInPages > maxPages:
            logging.debug('Size exceeds maxPages size of %s pages, skipping...' % (maxPages))
            continue

        pagesWasted = (w * (math.ceil(h) - h))

        if (pagesWasted / totalSizeInPages) > (maxPaperWastedPercentage / 100):
            logging.debug('Waste per page exceeds maxPaperWastedPercentage of %s, skipping...' % (maxPaperWastedPercentage))
            continue

        if (1 - (h % 1)) * 100 > maxSinglePageWastedPercentage:
            logging.debug('Waste per single page exceeds maxSinglePageWastedPercentage of %s, skipping...' % (maxSinglePageWastedPercentage))
            continue

        pdfFilename = Path(imagePath.stem + '_' + orientation + '_' + str(int(math.ceil(w))) + 'x' + str(int(math.ceil(h))) + '.pdf')
        saveAs(imagePath.parents[0] / pdfFilename)

    for numPages in range(1, math.ceil(math.sqrt(maxPages)) + 1):
        setSizeInPages((None, numPages))
        w, h = getSizeInPages()
        totalSizeInPages = math.ceil(w) * h

        logging.debug('Size in pages: %s x %s (%s x %s)' % (int(math.ceil(w)), h, w, h))
        if totalSizeInPages > maxPages:
            logging.debug('Size exceeds maxPages size of %s pages, skipping...' % (maxPages))
            continue

        if (1 - (w % 1)) * 100 > maxSinglePageWastedPercentage:
            logging.debug('Waste per single page exceeds maxSinglePageWastedPercentage of %s, skipping...' % (maxSinglePageWastedPercentage))
            continue

        pagesWasted = ((math.ceil(w) - w) * h)
        if (pagesWasted / totalSizeInPages) > (maxPaperWastedPercentage / 100):
            logging.debug('Waste per page exceeds maxPaperWastedPercentage of %s, skipping...' % (maxPaperWastedPercentage))
            continue

        pdfFilename = Path(imagePath.stem + '_' + orientation + '_' + str(int(math.ceil(w))) + 'x' + str(int(math.ceil(h))) + '.pdf')
        saveAs(imagePath.parents[0] / pdfFilename)



def createThumbnail(imageFilename):
    pass


def loadImage(imageFilename):
    if not os.path.exists(imageFilename):
        logging.error('Cannot load image. File not found: %s' % (imageFilename))
        raise PosteRazorAPIException('Cannot load image. File not found: %s' % (imageFilename))

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


def setToLandscape():
    logging.debug('Setting to landscape mode.')
    _gotoStep(2)
    _clickAt(0.75, 0.43)


def setToPortrait():
    logging.debug('Setting to portrait mode.')
    _gotoStep(2)
    _clickAt(0.75, 0.38)


def getOverlappingSize(value=None):
    pass


def setOverlappingPosition(value=None):
    pass


def getAbsoluteSize(value=None):
    pass


def setSizeInPages(value):
    return _interactWithSizeInPages(value)


def getSizeInPages():
    return _interactWithSizeInPages()


def _interactWithSizeInPages(value=None):
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
    logging.debug('Saving as %s' % (pdfFilename))
    alreadyExists = os.path.exists(pdfFilename)
    if alreadyExists:
        logging.debug('Deleting existing file %s' % (pdfFilename))
        os.unlink(pdfFilename)

    _gotoStep(5)
    _clickAt(0.74, 0.25)  # Click the Save button.

    pyautogui.sleep(0.25)
    pyautogui.write(str(pdfFilename) + '\n')
    pyautogui.sleep(0.25)

    #if alreadyExists:
    #    pyautogui.press('tab')
    #    pyautogui.press('\n')
    #    pyautogui.sleep(0.25)


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
        logging.error('Could not find the window for PosteRazor. Please run PosteRazor.')
        raise PosteRazorAPIException('Could not find the window for PosteRazor. Please run PosteRazor.')
    elif len(posterazorWindows) > 1:
        logging.error('%s instances of PosteRazor found. Please run only one instance of PosteRazor.' % (len(posterazorWindows)))
        raise PosteRazorAPIException('%s instances of PosteRazor found. Please run only one instance of PosteRazor.' % (len(posterazorWindows)))

    postWin = pyautogui.getWindowsWithTitle(posterazorWindows[0])[0]

    # Resize and focus the window.
    postWin.resizeTo(1, 1) # Set the size of PosteRazor to its smallest size.
    postWin.activate()
    return postWin