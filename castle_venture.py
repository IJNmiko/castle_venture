import tdl
import Game

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20

tdl.set_font('assets/arial10x10.png', greyscale=True, altLayout=True)
console = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT, title='Castle Venture', fullscreen=False)
tdl.set_fps(LIMIT_FPS)

game = Game.Game()

while not tdl.event.is_window_closed():
    for event in tdl.event.get():
        if event.type == 'KEYDOWN':
            if event.key == 'UP':
                game.playerMove(0, -1)
            elif event.key == 'DOWN':
                game.playerMove(0, 1)
            elif event.key == 'LEFT':
                game.playerMove(-1, 0)
            elif event.key == 'RIGHT':
                game.playerMove(1, 0)

    game.renderCurrentMap(console)
    game.renderEntities(console)

    tdl.flush()
