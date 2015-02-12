from bs4 import BeautifulSoup
from collections import defaultdict
import cv2
import cv2.cv as cv
import json
from os import listdir, path
from PIL import Image
import numpy as np
import pygame
import re
import sys
import tesseract as ts
import time

# General information about the tiles provided by the professor
WIDTH = 497
HEIGHT = 430
SIZE = (WIDTH, HEIGHT)
FIRST = (0, 0)
SECOND = (WIDTH, 0)

position = re.compile('bbox (?P<x1>\d+) (?P<y1>\d+) (?P<x2>\d+) (?P<y2>\d+); x_wconf (\d+)')

def mainLoop():
    tiles = []
    for image in listdir('tiles'):
        if "png" in image:
            tiles.append(path.join('tiles', image))
    currentImg = 0

    ocr = ts.TessBaseAPI()
    ocr.Init('.', 'eng', ts.OEM_DEFAULT)
    ocr.SetPageSegMode(ts.PSM_SINGLE_BLOCK)
    ocrLevel = ts.RIL_SYMBOL

    pygame.init()
    window = pygame.display.set_mode((497*2, 431))
    clock = pygame.time.Clock()

    tileData = []

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.K_RIGHT:
                current += 1
            elif ev.type == pygame.K_RIGHT:
                current -= 1
        
        # Make sure that we're not out of images
        if currentImg + 1 > len(tiles):
            break

        # Display the original
        imgOrig = pygame.image.load(tiles[currentImg])
        window.blit(imgOrig, FIRST)

        # Remember, this loads the file in as BGR
        cvOrig = cv2.imread(tiles[currentImg])
        cvFiltered = cv2.inRange(cvOrig, np.array([0, 200, 200], np.uint8), np.array([0, 255, 255], np.uint8))
        
        # Need to flip and rotate the image
        imgFiltered = pygame.surfarray.make_surface(np.rot90(np.fliplr(cvFiltered)))
        window.blit(imgFiltered, SECOND)

        # Set up a "valid" image to pass in to Tesseract
        ocrImage = cv.CreateImageHeader((cvFiltered.shape[1], cvFiltered.shape[0]), cv.IPL_DEPTH_8U, 1)
        cv.SetData(ocrImage, cvFiltered.tostring(), cvFiltered.dtype.itemsize * cvFiltered.shape[1])
        ts.SetCvImage(ocrImage, ocr)
        
        # Set up to get the numbers on the tiles
        ocr.SetRectangle(0, 0, WIDTH, HEIGHT - 40)
        ocr.Recognize(None)
        
        # Parse the HTML OCR results that Tesseract gives us
        hOCR = BeautifulSoup(ocr.GetHOCRText(ocrLevel))
        numbersOCR = hOCR.find_all(attrs = {'class': 'ocrx_word'})
        
        # Keep track of the numbers
        numbers = defaultdict(_factoryCoord)
        for numberCon in numbersOCR:
            number = 0

            box = position.match(numberCon.get('title'))
            
            # 2 looks like z
            if numberCon.get_text() in ['z', 'Z']:
                number = 2
            elif numberCon.get_text() in ['l', 'I', 'i']:
                number = 1
            else:
                number = int(numberCon.get_text())
            
            numbers[number] = getCoords(
                                  box.group('x1'), 
                                  box.group('y1'), 
                                  box.group('x2'), 
                                  box.group('y2')
                              )

        # Set up to get the name of the tiles
        ocr.SetRectangle(0, HEIGHT - 40, WIDTH, 40)
        ocr.Recognize(None)
        
        # Save information
        name = ocr.GetUTF8Text().strip().replace('VALLEV', 'VALLEY')
        filename = tiles[currentImg].replace('\\', '/')
        tileData.append(
            {
                'fileName': filename,
                'tileName': name,
                'numbers': numbers
            })

        currentImg += 1

        pygame.display.flip()
        pygame.time.delay(100)
    
    # Save the output data
    dumpHandle = open('data.json', 'w+')
    dumpHandle.write(json.dumps(tileData, indent=4))
    dumpHandle.close()

    pygame.quit()


def getCoords(x1, y1, x2, y2):
    return {
        'x': (int(x1) + int(x2))/2,
        'y': (int(y1) + int(y2))/2
    }

def _factoryCoord():
    return {'x': 0, 'y': 0}

if __name__ == '__main__':
    mainLoop()