from PIL import Image
from os import listdir, path

def _main():
    tiles = []
    for image in listdir('tiles'):
        tiles.append(path.join('tiles', image))

    # Save images as PNG
    for image in tiles:
        orig = Image.open(image)
        name, _ = path.splitext(image)
        orig.save(name +  '.png')


if __name__ == '__main__':
    _main()