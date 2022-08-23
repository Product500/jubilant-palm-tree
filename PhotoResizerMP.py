import os
from PIL import Image, ImageDraw
import argparse
import timeit
from concurrent.futures import ProcessPoolExecutor
from itertools import repeat


def get_args():
    '''Get arguements from user'''
    parser = argparse.ArgumentParser(description='STAIR Generic File Renamer')
    parser.add_argument(
        '-s', '--size', metavar='size', default=2500, help='Set the size of the new image measured in pixels on the logest edge. The process with preserve aspect (default: 1200 pixels)'
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


def countWork(imageFiles):
    count = 0
    for image in imageFiles:
        if image[-3:] == 'jpg':
            count = count + 1
    return count


def addPhotoFlag(image, flagColor):
    '''add a colored flag to the top right of the image'''
    draw = ImageDraw.Draw(image)
    draw.rectangle(
        [(0, 0), (image.height // 10, image.height // 10)], fill=flagColor)


def mpResizePhotos(image, workingDir, flag, color, imageScale=2500):
    '''Resize user supplied photos and omit the flag.'''
    workingDir = workingDir
    osSlash = os.sep
    size = imageScale, imageScale
    if image[-3:] == 'jpg':
        with Image.open(workingDir + osSlash + image) as im:
            im.thumbnail(size)
            if (flag):
                addPhotoFlag(im, color)
            im.save(workingDir + osSlash + image)


def main():

    args = get_args()
    imageFiles = read_dirinfo(args.directory)
    workerCount = os.cpu_count() * 2

    

    print(f'''
    The current working folder is {args.directory}.
    The number of files to be processed is {countWork(imageFiles)}.
    The number of cores available is {os.cpu_count()} and {workerCount} workers will fan out. 
    The flag value is set to {args.flag} with the color {args.color}.
    The desired image size is {args.size}px.
    ''')

    start = timeit.default_timer()

    with ProcessPoolExecutor(max_workers=workerCount) as executor:
        futures = executor.map(
            mpResizePhotos, imageFiles, repeat(args.directory), repeat(
                args.flag), repeat(args.color), repeat(args.size)
        )

    end = timeit.default_timer()

    print(
        f'The total time it took to complete this job was: {end-start:.4f} seconds.')
    input('[Press Enter to exit window.]')


if __name__ == '__main__':
    main()
