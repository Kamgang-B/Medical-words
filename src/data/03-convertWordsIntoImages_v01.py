
# Purpose: This file is used to convert words into images. The words converted
#          are contained in the file 01-allMedicalWords_v01.txt


import re
import os
import sys
from PIL import Image, ImageDraw, ImageFont
from glob import glob
from random import choices, choice


def convertWordsIntoImages(readwords,                  # readwords: a string or a list
                           imagefont,
                           writedir: str,
                           fontsize: int = 50,
                           margin: int = 50,
                           wordcolorRGB: tuple = None,
                           randomcolor: bool = False,
                           backgroundcolor: tuple = None,
                           randombackgroundcolor: bool = False) -> None:
    """
    This function is used to convert words into images

    :param readwords:  A word, list of words (litteral strings made up of only ASCII alphabet characters),
                      or path to the text file (with .txt extension) containing the words (one word by line!).
    :param imagefont: Path or directory or list of paths to the image fonts.
                      If a directory is specified, then a font is chosen randomly from the directory.
    :param writedir:  Path to the directory where to save the image(s).
    :param fontsize:  An integer specifying the font size.
    :param margin:    An integer specifying the margin around the word on an image (in pixels).
    :param wordcolorRGB: 3-tuple integers specifying the color of the word(s) in RGB format.
    :param randomcolor: Boolean specifying if the colors of the words should be random.
                        wordcolorRGB is ignored if randomcolor is True.
                        If True, a random RBG is chosen.
    :param backgroundcolor: 3-tuple integers specifying the background color of the image
    :param randombackgroundcolor: A boolean specifying if the background color should be random.
                                  backgroundcolor is ignored if randombackgroundcolor is True.
                                  if True, a random RBG not close to 'black' is chosen (RBG with all values >= 220)
    :return: None
    """


    # check if readwords is a path to a text file
    font_list = None  # will contain words

    if isinstance(readwords, list):
        # check if readwords is a list of words
        if not all(isinstance(x, str) and x.isalpha()  for x in readwords):
            raise TypeError("when 'readwords' is a list, it should contain words (made up of only ASCII alphabet characters)!")
        else:
            words = readwords

    elif isinstance(readwords, str):
        if not readwords.endswith('.txt'):
            # check of readwords is a single word
            if readwords.isalpha():
                words = [readwords]
            else:
                # raise error if readwords neither a .txt file nor a single word
                raise ValueError("'readwords' must be a text file path (with .txt extension), a word or list of words (made up of only ASCII alphabet characters)")
        else:
            try:
                # read file containing the words
                file = open(readwords, "r")
                words = [re.sub('\n$', '', line).strip() for line in file if len(line) > 1]
                file.close()
            except:
                raise FileNotFoundError(f"'{readwords}' file not found!")

            # check that 'words' is not empty and contains only single words
            if len(words) < 1:
                raise IndexError(f"No word found in '{readwords}'")
            else:
                # check that the words in readwords are single words of alphabet characters
                if not all([x.isalpha() for x in words]):
                    raise ValueError("Some line contains more than one word: check that each line contains only a single word made up of ASCII alphabet characters")
    else:
        raise TypeError("'readwords' should be a list or a string!")

    # set default values
    # color of the words
    if wordcolorRGB is None:
        wordcolorRGB = (0, 0, 0)
    else:
        if not (isinstance(wordcolorRGB, tuple) and all(isinstance(x, int) and x >= 0 and x <= 255 for x in wordcolorRGB)):
            raise TypeError("'wordcolorRGB' should be a tuple of three integers between 0 and 255")

    # background color of the images
    if backgroundcolor is None:
        backgroundcolor = (255, 255, 255)
    else:
        if not (isinstance(backgroundcolor, tuple) and all(isinstance(x, int) and x >= 0 and x <= 255 for x in backgroundcolor)):
            raise TypeError("'backgroundcolor' should be a tuple of three integers between 0 and 255")

    # check if the directory to save the images, writedir, exists
    if isinstance(writedir, str):
        if not os.path.isdir(writedir):
            raise FileNotFoundError(f"'{writedir}' directory not found!")
        else:
            # get absolute path
            writedir = os.path.abspath(writedir) + '\\'
    else:
        raise TypeError("'writedir' should be a string!")

    # check margin
    if margin < 0:
        raise ValueError("'margin' should be positive")
    # fontsize
    if fontsize < 0:
        raise ValueError("'fontsize' should be positive")

    # load the fonts
    if isinstance(imagefont, str):

        # check if fonts are not OpenType or TrueType
        if not (imagefont.endswith('.otf') or imagefont.endswith('.ttf')):

            # check if imagefont is a path to a director containing fonts
            if not os.path.isdir(imagefont):
                raise TypeError("'imagefont' (if specified as a string) should be either a path to a font (with .otf or .ttf extension) or an existing directory containing fonts")
            else:
                # find all fonts in the directory
                imagefont = os.path.abspath(imagefont) + '\\'
                fonts_path = glob(f"{imagefont}*.[ot]tf")

            if len(fonts_path) == 0:
                # raise an error if no font is found
                raise IndexError(f"No font (with .otf or .ttf extension) found in the directory '{imagefont}'!")
            else:
                # load all fonts
                font_list = []
                for file in fonts_path: font_list.append(ImageFont.truetype(file, fontsize))

    # load fonts from list of paths to fonts
    elif isinstance(imagefont, list):

        # check that the list contains paths to fonts
        if not all(isinstance(x, str) and (x.endswith('.otf') or x.endswith('.ttf'))  for x in imagefont):
            raise TypeError("when 'imagefont' is a list, it should contain the paths, specified as strings, to the fonts!")
        else:
            # load the fonts
            font_list = []
            for file in imagefont: font_list.append(ImageFont.truetype(file, fontsize))

    else:
        raise TypeError("'imagefont' should a string or a list!")

    # create images
    for word in words:

        # set image font
        if isinstance(font_list, list):
            font = choice(font_list)
        else:
            font = ImageFont.truetype(imagefont, fontsize)

        # get the size of the word
        word_width, word_height = font.getsize(word)

        # set image size
        imagesize = (margin*2 + word_width, margin*2 + word_height)

        # create an image
        if randombackgroundcolor is False:
            image = Image.new(mode='RGB', size=imagesize, color=backgroundcolor)
        else:
            image = Image.new(mode='RGB', size=imagesize, color=tuple(choices(range(220, 256), k=3)))

        # draw word on image
        draw_image = ImageDraw.Draw(image)

        if randomcolor is False:
            draw_image.text(xy=(margin, margin), text=word, font=font, fill=wordcolorRGB)
        else:
            draw_image.text(xy=(margin, margin), text=word, font=font, fill=tuple(choices(range(256), k=3)))

        # save image containing the word
        image.save(f'{writedir}{word}_image.png')
    return None


if __name__ == '__main__':

    # calling convertWordsIntoImages from command line: default behavior
    # Assumes that sampleWords.txt file, and fonts and sampleWords folders exist in the directory
    if len(sys.argv) == 1:
        #convertWordsIntoImages(readwords='data/processed/01-allMedicalWords_v01.txt',
        #                       imagefont='data/raw/fonts',
        #                       writedir='data/processed/Images')

        convertWordsIntoImages(readwords='sampleWords.txt',
                               imagefont='fonts',
                               writedir='sampleWords')

    # calling convertWordsIntoImages from command line with arguments
    else:
        # function argument error message (see below)
        err = "If specified, function arguments should be passed as a dictionary within quotes\nExample: convertWordsIntoImages.py \"{'readwords': 'words.txt', 'imagefont': 'fonts', 'writedir': 'Images'}\""

        # check if arguments are passed to convertWordsIntoImages (from the command line)
        if len(sys.argv) == 2:
            try:
                # parse the string (containing a dictionary) passed from the command line into a dictionary
                args = eval(sys.argv[1])
            except:
                raise ValueError(err)

            if not isinstance(args, dict):
                raise ValueError(err)

            # possible function formal arguments
            all_args = ['readwords', 'imagefont', 'writedir', 'fontsize', 'margin', 'wordcolorRGB', 'randomcolor', 'backgroundcolor', 'randombackgroundcolor']

            # check if all formal arguments passed to the function convertWordsIntoImages are valid
            if not set(all_args).issuperset(args.keys()):

                extra_args = ', '.join(set(args.keys()).difference(all_args))
                raise ValueError(f"Argument(s) `{extra_args}` not allowed! possible arguments are `{', '.join(all_args)}`")

            # check if the required arguments were specified
            required_args = ['readwords', 'imagefont', 'writedir']
            if not set(required_args).issubset(args.keys()):
                raise ValueError(f"Arguments `{', '.join(required_args)}` required!")

            convertWordsIntoImages(**args)

        else:
            raise ValueError(err)
    print("Done!!!")


#-