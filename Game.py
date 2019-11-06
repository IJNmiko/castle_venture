from PIL import Image

class Game:
    def __init__(self):
        self.current_map = 'start'
        self.player_x    = 14
        self.player_y    = 14

        self.maps = {}

    def loadMap(self, name):
        im = Image.open('assets/maps/' + name + '.png')
        im = im.convert('RGB')

        tiles = []

        for y in range(im.size[1]):
            for x in range(im.size[0]):
                pixel = im.getpixel((x, y))

                if pixel == (0,0,0):
                    tiles.append('ground')
                elif pixel == (255,255,255):
                    tiles.append('wall')
                elif pixel == (195,195,195):
                    tiles.append('gate')
                else:
                    tiles.append('?')

        self.maps[name] = tiles
        print(tiles)
