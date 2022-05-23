import pyasge

from game.gamestates.gamestate import GameState
from game.gamestates.gamestate import GameStateID
from game.gamedata import GameData


class GameMenu(GameState):

    def __init__(self, gamedata: GameData) -> None:
        super().__init__(gamedata)
        self.id = GameStateID.START_MENU
        self.to_level = False
        self.to_intro = False
        self.menu = pyasge.Sprite()
        self.initBackground()
        self.menu_text = None
        self.play_option = None
        self.intro_option = None
        self.quit_option = None
        self.initMenu()
        self.current_option = False

    def click_handler(self, event: pyasge.ClickEvent) -> None:
        if event.button == pyasge.MOUSE.MOUSE_BTN1:
            if event.action == pyasge.MOUSE.BUTTON_PRESSED:
                if self.is_inside(self.play_option, self.data.cursor.x, self.data.cursor.y):
                    self.to_level = True
                if self.is_inside(self.intro_option, self.data.cursor.x, self.data.cursor.y):
                    self.to_intro = True
                if self.is_inside(self.quit_option, self.data.cursor.x, self.data.cursor.y):
                    quit()

    def key_handler(self, event: pyasge.KeyEvent) -> None:
        pass

    def move_handler(self, event: pyasge.MoveEvent) -> None:
        if self.is_inside(self.play_option, self.data.cursor.x, self.data.cursor.y):
            self.play_option.colour = pyasge.COLOURS.DEEPSKYBLUE
            self.intro_option.colour = pyasge.COLOURS.ALICEBLUE
            self.quit_option.colour = pyasge.COLOURS.ALICEBLUE
        elif self.is_inside(self.intro_option, self.data.cursor.x, self.data.cursor.y):
            self.play_option.colour = pyasge.COLOURS.ALICEBLUE
            self.intro_option.colour = pyasge.COLOURS.DEEPSKYBLUE
            self.quit_option.colour = pyasge.COLOURS.ALICEBLUE
        elif self.is_inside(self.quit_option, self.data.cursor.x, self.data.cursor.y):
            self.play_option.colour = pyasge.COLOURS.ALICEBLUE
            self.intro_option.colour = pyasge.COLOURS.ALICEBLUE
            self.quit_option.colour = pyasge.COLOURS.DEEPSKYBLUE
        else:
            self.play_option.colour = pyasge.COLOURS.ALICEBLUE
            self.intro_option.colour = pyasge.COLOURS.ALICEBLUE
            self.quit_option.colour = pyasge.COLOURS.ALICEBLUE

    def fixed_update(self, game_time: pyasge.GameTime) -> None:
        pass

    def update(self, game_time: pyasge.GameTime) -> GameStateID:
        if self.data.gamepad.connected:
            if self.data.gamepad.AXIS_LEFT_Y >= 0.5:
                if not self.gamepad_move:
                    if self.current_option == 2:
                        self.current_option = 0
                    else:
                        self.current_option += 1
                    self.gamepad_move = True
                    self.text_colours()
            elif self.data.gamepad.AXIS_LEFT_Y <= -0.5:
                if not self.gamepad_move:
                    if self.current_option == 0:
                        self.current_option = 2
                    else:
                        self.current_option -= 1
                    self.gamepad_move = True
                    self.text_colours()
            else:
                self.gamepad_move = False
            if self.data.gamepad.A and not self.data.prev_gamepad.A:
                if self.current_option == 0:
                    self.to_level = True
                elif self.current_option == 1:
                    self.to_intro = True
                elif self.current_option == 2:
                    quit()
        if self.to_level:
            return GameStateID.LEVEL_SELECT
        if self.to_intro:
            return GameStateID.INTRO

        return GameStateID.START_MENU

    def render(self, game_time: pyasge.GameTime) -> None:
        self.data.renderer.render(self.menu)

        self.data.renderer.render(self.menu_text)
        self.data.renderer.render(self.play_option)
        self.data.renderer.render(self.intro_option)
        self.data.renderer.render(self.quit_option)

        pass

    def initBackground(self) -> bool:
        if self.menu.loadTexture("/data/textures/mainMenuBackground.jpg"):
            # loaded, so make sure this gets rendered first
            self.menu.scale = 1.6
            self.menu.z_order = -100
            # print("New Background Works")
            return True
        else:
            return False

    def initMenu(self):
        # Create all menu text
        self.menu_text = pyasge.Text(self.data.fonts["MenuFont"])
        self.menu_text.string = "It Came From\n   The Woods"
        self.menu_text.position = [407, 350]
        self.menu_text.colour = pyasge.COLOURS.GAINSBORO
        self.menu_text.scale = 2

        self.play_option = pyasge.Text(self.data.fonts["MenuFont"])
        self.play_option.string = "Choose Your Level"
        self.play_option.position = [551, 725]
        self.play_option.colour = pyasge.COLOURS.ALICEBLUE

        self.intro_option = pyasge.Text(self.data.fonts["MenuFont"])
        self.intro_option.string = "Introduction"
        self.intro_option.position = [678.5, 875]
        self.intro_option.colour = pyasge.COLOURS.ALICEBLUE

        self.quit_option = pyasge.Text(self.data.fonts["MenuFont"])
        self.quit_option.string = "Quit"
        self.quit_option.position = [874.5, 1025]
        self.quit_option.colour = pyasge.COLOURS.ALICEBLUE

    def is_inside(self, text, mouse_x, mouse_y) -> bool:
        bounds = text.world_bounds
        # check to see if the mouse position falls within the x and y bounds of the sprite
        if bounds.v1.x < mouse_x < bounds.v2.x and bounds.v1.y < mouse_y < bounds.v3.y:
            return True
        return False

    def text_colours(self):
        # Update colours of menu text
        if self.current_option == 0:
            self.play_option.colour = pyasge.COLOURS.DEEPSKYBLUE
            self.intro_option.colour = pyasge.COLOURS.ALICEBLUE
            self.quit_option.colour = pyasge.COLOURS.ALICEBLUE
        elif self.current_option == 1:
            self.play_option.colour = pyasge.COLOURS.ALICEBLUE
            self.intro_option.colour = pyasge.COLOURS.DEEPSKYBLUE
            self.quit_option.colour = pyasge.COLOURS.ALICEBLUE
        elif self.current_option == 2:
            self.play_option.colour = pyasge.COLOURS.ALICEBLUE
            self.intro_option.colour = pyasge.COLOURS.ALICEBLUE
            self.quit_option.colour = pyasge.COLOURS.DEEPSKYBLUE
        elif self.current_option == -1:
            self.play_option.colour = pyasge.COLOURS.ALICEBLUE
            self.intro_option.colour = pyasge.COLOURS.ALICEBLUE
