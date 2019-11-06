import tdl
import Game

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20

tdl.set_font('assets/arial10x10.png', greyscale=True, altLayout=True)
console = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT, title='Castle Venture', fullscreen=False)
tdl.setFPS(LIMIT_FPS)

game = Game.Game()

while not tdl.event.is_window_closed():
    game.renderCurrentMap(console)
    tdl.flush()
