import posterazorapi

import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Please supply an image file to make PDFs from.')

    for i in range(1, len(sys.argv)):
        posterazorapi.run(sys.argv[i])
