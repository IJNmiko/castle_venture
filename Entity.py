class Entity:
    def __init__(self, x, y, char, ai):
        self.x = x
        self.y = y
        self.char = char
        self.ai = ai

        self.visible = True

    def update(self):
        if self.ai == 'disappear':
            self.visible = False

    def render(self, console):
        if self.visible:
            console.draw_char(
                self.x,
                self.y,
                self.char,
                bg=None,
                fg=(255, 255, 255)
            )
