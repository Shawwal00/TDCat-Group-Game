import pyasge

from game.gamestates.gamestate import GameState
from game.gamestates.gamestate import GameStateID
from game.gamedata import GameData

class GamePause(GameState):

    def __init__(self, gamedata: GameData) -> None:
        super().__init__(gamedata)
        self.id = GameStateID.PAUSE
        self.pause_text = None
        self.resume_option = None
        self.main_menu_option = None
        self.quit_option = None
        self.pause_background = pyasge.Sprite()
        self.initPause()

        self.current_option = 0
        self.to_game = False
        self.to_main = False

        self.going_up = False
        self.going_down = False

    def click_handler(self, event: pyasge.ClickEvent) -> None:
        if event.button == pyasge.MOUSE.MOUSE_BTN1:
            if event.action == pyasge.MOUSE.BUTTON_PRESSED:
                if self.is_inside(self.resume_option, self.data.cursor.x, self.data.cursor.y):
                    self.to_game = True
                if self.is_inside(self.main_menu_option, self.data.cursor.x, self.data.cursor.y):
                    self.to_main = True
                if self.is_inside(self.quit_option, self.data.cursor.x, self.data.cursor.y):
                    quit()

    def key_handler(self, event: pyasge.KeyEvent) -> None:
        if event.action == pyasge.KEYS.KEY_PRESSED:
            if event.key == pyasge.KEYS.KEY_ESCAPE:
                self.to_game = True

    def move_handler(self, event: pyasge.MoveEvent) -> None:
        if self.is_inside(self.resume_option, self.data.cursor.x, self.data.cursor.y):
            self.current_option = 0
        elif self.is_inside(self.main_menu_option, self.data.cursor.x, self.data.cursor.y):
            self.current_option = 1
        elif self.is_inside(self.quit_option, self.data.cursor.x, self.data.cursor.y):
            self.current_option = 2
        else:
            self.current_option = -1
        self.text_colours()

    def fixed_update(self, game_time: pyasge.GameTime) -> None:
        pass

    def update(self, game_time: pyasge.GameTime) -> GameStateID:
        if self.data.gamepad.connected:
            if self.data.gamepad.AXIS_LEFT_Y >= 0.5 or self.data.gamepad.AXIS_LEFT_Y <= -0.5:
                if self.data.gamepad.AXIS_LEFT_Y >= 0.5 and not self.going_up == True:
                    self.current_option += 1
                    self.going_up = True
                    if self.current_option >= 3:
                        self.current_option = 0
                elif self.data.gamepad.AXIS_LEFT_Y <= -0.5 and not self.going_down == True:
                    self.current_option -= 1
                    self.going_down = True
                    if self.current_option <= -1:
                        self.current_option = 2
                self.text_colours()
            else:
                self.going_up = False
                self.going_down = False
            if self.data.gamepad.A and not self.data.prev_gamepad.A:
                if self.current_option == 0:
                    self.to_game = True
                if self.current_option == 1:
                    self.to_main = True
                if self.current_option == 2:
                    quit()
        if self.to_game:
            return GameStateID.GAMEPLAY
        if self.to_main:
            return GameStateID.START_MENU

        return GameStateID.PAUSE

    def render(self, game_time: pyasge.GameTime) -> None:
        self.data.shaders["main"].uniform("rgb").set([1, 1, 1])
        self.data.shaders["main"].uniform("alpha").set(float(0.5))
        self.data.renderer.shader = self.data.shaders["main"]
        self.data.renderer.render(self.pause_background)
        self.data.renderer.render(self.pause_text)
        self.data.renderer.render(self.resume_option)
        self.data.renderer.render(self.main_menu_option)
        self.data.renderer.render(self.quit_option)

        pass

    def initPause(self):
        self.pause_text = pyasge.Text(self.data.fonts["MenuFont"])
        self.pause_text.string = "PAUSE MENU"
        self.pause_text.position = [460, 350]
        self.pause_text.colour = pyasge.COLOURS.GAINSBORO
        self.pause_text.scale = 2
        self.pause_text.z_order = 105
        #print(self.pause_text.world_bounds)

        self.resume_option = pyasge.Text(self.data.fonts["MenuFont"])
        self.resume_option.string = "Resume"
        self.resume_option.position = [797.5, 650]
        self.resume_option.z_order = 105
        if self.data.gamepad.connected:
            self.resume_option.colour = pyasge.COLOURS.DEEPSKYBLUE
        else:
            self.resume_option.colour = pyasge.COLOURS.ALICEBLUE
        #print(self.resume_option.world_bounds)

        self.main_menu_option = pyasge.Text(self.data.fonts["MenuFont"])
        self.main_menu_option.string = "Main Menu"
        self.main_menu_option.position = [743.5, 800]
        self.main_menu_option.colour = pyasge.COLOURS.ALICEBLUE
        self.main_menu_option.z_order = 105
        #print(self.main_menu_option.world_bounds)

        self.quit_option = pyasge.Text(self.data.fonts["MenuFont"])
        self.quit_option.string = "Quit"
        self.quit_option.position = [873.5, 950]
        self.quit_option.colour = pyasge.COLOURS.ALICEBLUE
        self.quit_option.z_order = 105
        #print(self.quit_option.world_bounds)

        self.pause_background.loadTexture("/data/textures/mainMenuBackground.jpg")
        # loaded, so make sure this gets rendered first
        self.pause_background.scale = 1.6
        self.pause_background.z_order = 101


    def is_inside(self, text, mouse_x, mouse_y) -> bool:
        bounds = text.world_bounds
        # check to see if the mouse position falls within the x and y bounds of the sprite
        if bounds.v1.x < mouse_x < bounds.v2.x and bounds.v1.y < mouse_y < bounds.v3.y:
            return True
        return False

    def text_colours(self):
        if self.current_option == 0:
            self.resume_option.colour = pyasge.COLOURS.DEEPSKYBLUE
            self.main_menu_option.colour = pyasge.COLOURS.ALICEBLUE
            self.quit_option.colour = pyasge.COLOURS.ALICEBLUE
        if self.current_option == 1:
            self.resume_option.colour = pyasge.COLOURS.ALICEBLUE
            self.main_menu_option.colour = pyasge.COLOURS.DEEPSKYBLUE
            self.quit_option.colour = pyasge.COLOURS.ALICEBLUE
        if self.current_option == 2:
            self.resume_option.colour = pyasge.COLOURS.ALICEBLUE
            self.main_menu_option.colour = pyasge.COLOURS.ALICEBLUE
            self.quit_option.colour = pyasge.COLOURS.DEEPSKYBLUE
        if self.current_option == -1:
            self.resume_option.colour = pyasge.COLOURS.ALICEBLUE
            self.main_menu_option.colour = pyasge.COLOURS.ALICEBLUE
            self.quit_option.colour = pyasge.COLOURS.ALICEBLUE
