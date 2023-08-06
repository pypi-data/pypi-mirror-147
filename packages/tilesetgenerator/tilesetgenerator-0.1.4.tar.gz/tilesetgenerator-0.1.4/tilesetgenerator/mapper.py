from PIL import Image

# Gets the upper left quadrant of an image
def ul(im: Image) -> Image:
    return im.crop((0, 0, im.size[0] // 2, im.size[1] // 2))

# Gets the upper right quandrant of an image
def ur(im: Image) -> Image:
    return im.crop((im.size[0] // 2, 0, im.size[0], im.size[1] // 2))

# Gets the bottom left quadrant of an image
def bl(im: Image) -> Image:
    return im.crop((0, im.size[1] // 2, im.size[0] // 2, im.size[1]))

# Gets the bottom right quadrant of the image
def br(im: Image) -> Image:
    return im.crop((im.size[0] // 2, im.size[1] // 2, im.size[0], im.size[1]))

def create_map(map: [[[Image]]], tile_size: int) -> Image:
    image = Image.new("RGBA", (tile_size * len(map[0]), tile_size * len(map)))
    for (y, row) in enumerate(map):
        for (x, cell) in enumerate(row):
            if cell[0][0] != None:
                image.paste(
                    ul(cell[0][0]),
                    (x * tile_size, y * tile_size)
                )
            if cell[0][1] != None:
                image.paste(
                    ur(cell[0][1]),
                    (x * tile_size + tile_size // 2, y * tile_size)
                )
            if cell[1][1] != None:
                image.paste(
                    br(cell[1][1]),
                    (x * tile_size + tile_size // 2, y * tile_size + tile_size // 2)
                )
            if cell[1][0] != None:
                image.paste(
                    bl(cell[1][0]),
                    (x * tile_size, y * tile_size + tile_size // 2)
                )
    return image
