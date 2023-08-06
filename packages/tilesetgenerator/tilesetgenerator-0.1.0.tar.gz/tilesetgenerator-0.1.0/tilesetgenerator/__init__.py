#!/usr/bin/env python3

import argparse
import sys
from PIL import Image
from tilesetgenerator.map import get_map
import tilesetgenerator.mapper
from pathlib import Path, PurePath

__license__ = "GPL3"
__version__ = "0.1.0"
__author__ = __maintainer__ = "John Toohey"
__email__ = "john_t@mailo.com"

epilog= """\
By default it will use the current directory.

Make sure that each of the specified directories contains a:
    - corners.png
    - fill.png
    - inverse_corners.png
    - out.png
    - vertical.png
    - horizontal.png

More information can be found in the README at:

    https://gitlab.com/john_t/tile-set-generator
"""


# Create an argument parser
parser = argparse.ArgumentParser(
    description = "Generates a tilemap from a few template images",
    epilog = epilog,
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
parser.add_argument(
    "paths",
    metavar = "DIRECTORY",
    nargs = "*",
    default = [Path()],
    type = Path,
    help = "path(s) to the directories containing the files"
)

args = parser.parse_args()
    
def run(path):
    # Load the images
    corners = Image.open(Path(path, "corners.png"))
    inverse_corners = Image.open(Path(path, "inverse_corners.png"))
    fill = Image.open(Path(path, "fill.png"))
    vertical = Image.open(Path(path, "vertical.png"))
    horizontal = Image.open(Path(path, "horizontal.png"))

    # Create our new image
    tile_size = corners.size[0]
    map = get_map(
        corners,
        inverse_corners,
        fill,
        vertical,
        horizontal,
    )
    im = mapper.create_map(map, tile_size)

    # Debug: Show
    im.save(Path(path, "out.png"))

for path in args.paths:
    if not path.is_dir():
        print("Path", path, "is not a directory!")
        sys.exit(1)
    run(path)
