import json
from PIL import Image

import Entity


class Game:
    def __init__(self):
        self.maps = {}
        self.maps_data = {}
        self.map_size = 40

        self.current_map = 'start'
        self.current_map_desc = ''
        self.player_x = int(self.map_size / 2)
        self.player_y = int(self.map_size / 2)

        self.tiles = {
            'ground': ' ',
            'wall':   chr(178),
            'gate':   chr(176)
        }

    def playerMove(self, relative_x, relative_y):
        new_x = self.player_x + relative_x
        new_y = self.player_y + relative_y

        # Check for event activation
        pos = (new_x, new_y)
        if pos in self.maps_data[self.current_map]['events']:
            event = self.maps_data[self.current_map]['events'][pos]
            self.handleEvent(event)
            return

        index = (new_y * self.map_size) + new_x
        if self.maps[self.current_map][index] != 'ground':
            return

        self.player_x = new_x
        self.player_y = new_y

    def update(self):
        if 'entities' not in self.maps_data[self.current_map]:
            return

        for e in self.maps_data[self.current_map]['entities']:
            entity = self.maps_data[self.current_map]['entities'][e]

            if entity['instance']:
                entity['instance'].update()

    def loadMap(self, name):
        map_data = json.load(
            open('assets/maps/' + name + '.json', 'r')
        )

        self.maps_data[name] = map_data

        im = Image.open('assets/maps/' + name + '.png')
        im = im.convert('RGB')

        tiles = []

        for y in range(im.size[1]):
            for x in range(im.size[0]):
                pixel = im.getpixel((x, y))

                if pixel == (0, 0, 0):
                    tiles.append('ground')
                elif pixel == (255, 255, 255):
                    tiles.append('wall')
                elif pixel == (195, 195, 195):
                    tiles.append('gate')
                elif pixel[0] == 255:
                    # Handle event tiles
                    event = map_data['events'][str(pixel[1])]
                    self.maps_data[name]['events'][(x, y)] = event

                    tiles.append('ground')
                elif pixel[1] == 255:
                    # Handle entities
                    entity = map_data['entities'][str(pixel[2])]

                    entity['instance'] = Entity.Entity(
                        x,
                        y,
                        chr(entity['char']),
                        entity['ai']
                    )

                    tiles.append('ground')
                else:
                    tiles.append('?')

        self.maps[name] = tiles

    def renderCurrentMap(self, console):
        if self.current_map not in self.maps:
            self.loadMap(self.current_map)

        # Print the map's description
        self.renderText(
            console,
            self.maps_data[self.current_map]['description'],
            0,
            41,
            40
        )

        x = 0
        y = 0

        for t in self.maps[self.current_map]:
            console.draw_char(x, y, self.tiles[t], bg=None, fg=(255, 255, 255))

            x += 1
            if x == self.map_size:
                x = 0
                y += 1

    def renderEntities(self, console):
        console.draw_char(
            self.player_x,
            self.player_y,
            chr(5),
            bg=None,
            fg=(255, 255, 255)
        )

        if 'entities' not in self.maps_data[self.current_map]:
            return

        for e in self.maps_data[self.current_map]['entities']:
            entity = self.maps_data[self.current_map]['entities'][e]

            if entity['instance']:
                entity['instance'].render(console)

    def renderText(self, console, text, x, y, w):
        console.clear()

        cur_x = 0
        cur_y = 0

        for c in text:
            console.draw_char(
                x + cur_x,
                y + cur_y,
                c,
                bg=None,
                fg=(255, 255, 255)
            )

            cur_x += 1
            if cur_x >= w and c == ' ':
                cur_x = 0
                cur_y += 1

    def handleEvent(self, event):
        tokens = event.split()

        if tokens[0] == 'map':
            self.current_map = tokens[1]
            self.player_x = int(tokens[2])
            self.player_y = int(tokens[3])
