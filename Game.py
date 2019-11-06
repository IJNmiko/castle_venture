from PIL import Image

class Game:
    def __init__(self):
        self.maps = {}
        self.map_size = 40

        self.current_map = 'start'
        self.player_x    = int(self.map_size / 2)
        self.player_y    = int(self.map_size / 2)

        self.tiles = {
            'ground': ' ',
            'wall':   chr(178),
            'gate':   chr(176)
        }

    def playerMove(self, relative_x, relative_y):
        new_x = self.player_x + relative_x
        new_y = self.player_y + relative_y

        if self.maps[self.current_map][(new_y * self.map_size) + new_x] != 'ground':
            return

        self.player_x = new_x
        self.player_y = new_y

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

    def renderCurrentMap(self, console):
        if self.current_map not in self.maps:
            self.loadMap(self.current_map)

        x = 0
        y = 0

        for t in self.maps[self.current_map]:
            console.draw_char(x, y, self.tiles[t], bg=None, fg=(255,255,255))

            x += 1
            if x == self.map_size:
                x = 0
                y += 1

    def renderEntities(self, console):
        console.draw_char(self.player_x, self.player_y, '@', bg=None, fg=(255,255,255))
