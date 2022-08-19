import os
from PIL import Image, ImageDraw
import argparse
import timeit
from concurrent.futures import ProcessPoolExecutor, as_completed


def get_args():
    '''Get arguements from user'''
    parser = argparse.ArgumentParser(description='STAIRs Generic File Renamer')
    parser.add_argument(
        '-s', '--size', metavar='size', default=1200, help='Set the size of the new image measured in pixels on the logest edge. The process with preserve aspect (default: 1200 pixels)'
    )
    parser.add_argument(
        '-d', '--directory', metavar='directory', default=os.path.dirname(__file__), help='The folder that contains the photos to be resized (default: looks for images in the current folder of the script)'
    )
    parser.add_argument(
        '-f', '--flag', metavar='flag', default=False, help='Set a True/False to determine if colored flags should be added to the resized images. (default: False)'
    )
    parser.add_argument(
        '-c', '--color', metavar='color', default='red', help='If the flag value is set to True you can change the color of the flag. (default: \'red\')'
    )
    return parser.parse_args()


def read_dirinfo(directory):
    '''Get the contents of the directory specified that has been passed in.'''
    return os.listdir(directory)


def mpResizePhotosChip(image, imageScale=2500):
    '''Resize user supplied photos with a colored flag in the top left hand corner.'''

    size = imageScale, imageScale

    if image[-3:] == 'jpg':

        with Image.open(str(os.path.dirname(__file__) + '\\' + image)) as im:
            draw = ImageDraw.Draw(im)
            draw.rectangle([(0, 0), (im.height // 10, im.height // 10)], fill='red')
            im.thumbnail(size)
            im.save(str(os.path.dirname(__file__) + '\\' + image))


def mpResizePhotos(image, imageScale=2500):
    '''Resize user supplied photos and omit the flag.'''
    size = imageScale, imageScale
    if image[-3:] == 'jpg':

        with Image.open(str(os.path.dirname(__file__) + '\\' + image)) as im:
            im.thumbnail(size)
            im.save(str(os.path.dirname(__file__) + '\\' + image))


def main():

    args = get_args()
    imageFiles = read_dirinfo(args.directory)
    workType = mpResizePhotos

    # Use a bool to determine what type of work we are doing. This check is made only once at the start of execution.
    if (args.flag):
        workType = mpResizePhotosChip

    start = timeit.default_timer()
    print(
        f'The state of workType is: {args.flag} and the state of color is: {args.color} as {type(args.color)}')
    with ProcessPoolExecutor(max_workers=10) as executor:
        futures = executor.map(
            workType, imageFiles
        )

    end = timeit.default_timer()

    print(
        f'The total time it took to complete this job was: {end-start:.4f} seconds.')
    input('[Press Enter to exit window.]')


if __name__ == '__main__':
    main()
