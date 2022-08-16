import os
from PIL import Image, ImageDraw
import argparse
import timeit
from concurrent.futures import ProcessPoolExecutor, as_completed


def get_args():
    '''Get arguements from user'''
    parser = argparse.ArgumentParser(description='STAIRs Generic File Renamer')
    parser.add_argument(
        '-s', '--size', metavar='size', default=2500, help='Set the size of the new image measured in pixels on the logest edge. The process with preserve aspect (default: 1200 pixels)'
    )
    parser.add_argument(
        '-d', '--directory', metavar='directory', default=os.path.dirname(__file__), help='The folder that contains the photos to be resized (default: looks for images in the current folder of the script)'
    )
    return parser.parse_args()


def read_dirinfo(directory):
    '''Get the contents of the directory specified that has been passed in.'''
    return os.listdir(directory)


def resize_photo(imageScale, imageDirectory):

    size = imageScale, imageScale

    for fileName in imageDirectory:

        if fileName[-3:] == 'jpg':

            with Image.open(str(os.path.dirname(__file__) + '\\' + fileName)) as im:
                im.thumbnail(size)
                im.save(str(os.path.dirname(__file__) + '\\' + fileName))


def mpResizePhotos(image, imageScale=1200):
    size = imageScale, imageScale
    if image[-3:] == 'jpg':

        with Image.open(str(os.path.dirname(__file__) + '\\' + image)) as im:
            draw = ImageDraw.Draw(im)
            draw.rectangle([(0,0),(300,200)],fill='red')
            im.thumbnail(size)
            im.save(str(os.path.dirname(__file__) + '\\' + image))


def main():

    args = get_args()
    imageFiles = read_dirinfo(args.directory)
    start = timeit.default_timer()
    with ProcessPoolExecutor(max_workers=10) as executor:
        futures = executor.map(
            mpResizePhotos, imageFiles
        )

    end = timeit.default_timer()

    print('The total time it took to complete this job was: ' +
          str(end-start) + ' seconds.')
    input('[Press Enter to exit window.]')


if __name__ == '__main__':
    main()
