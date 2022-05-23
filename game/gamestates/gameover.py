import pyasge

from game.gamestates.gamestate import GameState
from game.gamestates.gamestate import GameStateID
from game.gamedata import GameData, Difficulty
from game.wavedata import WaveData


class GameOver(GameState):

    def __init__(self, data: GameData) -> None:
        super().__init__(data)
        self.id = GameStateID.GAME_OVER
        self.again_transition = False
        self.over_text = None
        self.play_option = None
        self.exit_option = None
        self.background = pyasge.Sprite()
        self.details_text = None
        self.level = None
        self.initMenu()
        self.won_option = 0
        self.current_option = -1
        self.gamepad_move = False

    def click_handler(self, event: pyasge.ClickEvent) -> None:
        if event.button == pyasge.MOUSE.MOUSE_BTN1:
            if event.action == pyasge.MOUSE.BUTTON_PRESSED:
                if self.is_inside(self.play_option, self.data.cursor.x, self.data.cursor.y):
                    # print("Again Clicked")
                    self.again_transition = True
                if self.is_inside(self.exit_option, self.data.cursor.x, self.data.cursor.y):
                    # print("Quit Clicked")
                    quit()

    def key_handler(self, event: pyasge.KeyEvent) -> None:
        pass

    def move_handler(self, event: pyasge.MoveEvent) -> None:
        if self.is_inside(self.play_option, self.data.cursor.x, self.data.cursor.y):
            # print("Resume Hover")
            self.current_option = 0
        elif self.is_inside(self.exit_option, self.data.cursor.x, self.data.cursor.y):
            # print("Main Menu Hover")
            self.current_option = 1
        else:
            self.current_option = -1
        self.text_colours()

    def fixed_update(self, game_time: pyasge.GameTime) -> None:
        if self.data.gamepad.connected:
            if self.data.gamepad.AXIS_LEFT_X >= 0.5 or self.data.gamepad.AXIS_LEFT_X <= -0.5:
                if not self.gamepad_move:
                    if self.current_option == 0:
                        self.current_option = 1
                    else:
                        self.current_option = 0
                    self.gamepad_move = True
                    self.text_colours()
            else:
                self.gamepad_move = False
            if self.data.gamepad.A:
                if self.current_option == 0:
                    self.again_transition = True
                if self.current_option == 1:
                    quit()

    def update(self, game_time: pyasge.GameTime) -> GameStateID:
        if self.again_transition:
            return GameStateID.START_MENU
        return GameStateID.GAME_OVER

    def render(self, game_time: pyasge.GameTime) -> None:
        self.data.renderer.render(self.over_text)
        self.data.renderer.render(self.play_option)
        self.data.renderer.render(self.exit_option)
        self.data.renderer.render(self.background)
        self.data.renderer.render(self.details_text)

    def initMenu(self) -> None:
        self.over_text = pyasge.Text(self.data.fonts["MenuFont"])
        self.over_text.string = "YOU LOST"
        self.over_text.position = [582, 350]
        self.over_text.scale = 2
        self.over_text.colour = pyasge.COLOURS.GAINSBORO

        self.play_option = pyasge.Text(self.data.fonts["MenuFont"])
        self.play_option.string = "AGAIN"
        self.play_option.position = [648, 900]
        self.play_option.colour = pyasge.COLOURS.ALICEBLUE

        self.exit_option = pyasge.Text(self.data.fonts["MenuFont"])
        self.exit_option.string = "EXIT"
        self.exit_option.position = [1074.5, 900]
        self.exit_option.colour = pyasge.COLOURS.ALICEBLUE

        if self.data.difficulty == Difficulty.EASY:
            self.level = "Easy"
        elif self.data.difficulty == Difficulty.NORMAL:
            self.level = "Normal"
        elif self.data.difficulty == Difficulty.HARD:
            self.level = "Hard"

        self.details_text = pyasge.Text(self.data.fonts["MenuFont"])
        self.details_text.string = "You Survived " + str(self.data.current_wave_num - 1) + " Waves on " + self.level +\
                                   "\n               Difficulty on Map " + str(self.data.selected_level)
        self.details_text.position = [262, 600]
        self.details_text.colour = pyasge.COLOURS.ALICEBLUE
        print(self.details_text.world_bounds)

        if self.background.loadTexture("/data/textures/mainMenuBackground.jpg"):
            self.background.scale = 1.6
            self.background.z_order = -100
        else:
            print("Background Failed to load")

    def is_inside(self, text, mouse_x, mouse_y) -> bool:
        bounds = text.world_bounds
        # check to see if the mouse position falls within the x and y bounds of the sprite
        if bounds.v1.x < mouse_x < bounds.v2.x and bounds.v1.y < mouse_y < bounds.v3.y:
            return True
        return False

    def text_colours(self):
        if self.current_option == 0:
            self.play_option.colour = pyasge.COLOURS.DEEPSKYBLUE
            self.exit_option.colour = pyasge.COLOURS.ALICEBLUE
        if self.current_option == 1:
            self.play_option.colour = pyasge.COLOURS.ALICEBLUE
            self.exit_option.colour = pyasge.COLOURS.DEEPSKYBLUE
        if self.current_option == -1:
            self.play_option.colour = pyasge.COLOURS.ALICEBLUE
            self.exit_option.colour = pyasge.COLOURS.ALICEBLUE
