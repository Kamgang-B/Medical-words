
# Purpose: This file is used to convert words into images. The words converted 
#          are contained in the file 01-allMedicalWords_v01.txt


import re
import os
from PIL import Image, ImageDraw, ImageFont

# define a function to convert words into images
def convertWordsIntoImages(readfile: str, writedir: str = '',
                           imagesize: tuple = None,
                           fontsize: int = 50,
                           imagefont: str = None,
                           wordcolorRGB: tuple = None) -> None:
    '''
    
    This function is used to convert words into images

    :param readfile: path to the text file containing the words (one word by line!)
    :param writedir: path to the directory where to save the images (defaults to the current directory).
                     it should end with a forward slash (example: folder1/foder2/)
    :param imagesize: desired size of images in pixels; a 2-tuple (defaults to (len(word)*100, 100) )
    :param fontsize: font size image (defaults to 50) see help(ImageFont.truetype) in PIL library
    :param imagefont: path to image font; see help(ImageFont.truetype) in PIL library
    :param wordcolorRGB: color of the word in RBG (default to (255, 255, 255): white)
    :return: None
    '''

    # check if readfile is a path to a text file
    if not re.match(pattern='.+\.txt$', string=readfile):
        # Assume that readfile is a word if it's not a path to a text file (.txt file)
        words = [readfile]
    else:
        try:
            # read file containing the words
            file = open(readfile, "r")
            words = [re.sub('\n$', '', line) for line in file if len(line) > 0]
            file.close()
        except:
            raise FileNotFoundError(f'{readfile} file not found!')

    # check if the directory writedir exists
    if not os.path.isdir(writedir) and writedir:
        raise FileNotFoundError(f'{writedir} directory not found!')

    # define default image font
    if imagefont is None:
        imagefont = 'OpenSans-Regular.ttf'

    # define default color
    if wordcolorRGB is None:
        wordcolorRGB = (0, 0, 0)

    # convert each word into a png image and save it
    for word in words:
        # compute the image size for the current word
        if imagesize is None:
            imagesize = (80 * len(word), 100)

        # create an image
        image = Image.new(mode='RGB', size=imagesize, color=(255, 255, 255))

        # set image font
        font = ImageFont.truetype(imagefont, fontsize)

        # draw word on image
        draw_image = ImageDraw.Draw(image)
        draw_image.text(xy=(10, 10), text=word, font=font, fill=wordcolorRGB)

        # save image containing the word
        image.save(f'{writedir}{word}_image.png')
    return None

if not os.path.isdir('wordsInImages'):
    os.makedirs('wordsInImages')


if __name__ == '__main__':
    convertWordsIntoImages('01-allMedicalWords_v01.txt', 'wordsInImages/')











