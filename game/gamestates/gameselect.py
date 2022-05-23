import string

import pyasge

from game.gamestates.gamestate import GameState
from game.gamestates.gamestate import GameStateID
from game.gamedata import GameData
from game.gamedata import Difficulty


class GameSelect(GameState):

    def __init__(self, gamedata: GameData) -> None:
        super().__init__(gamedata)
        self.id = GameStateID.LEVEL_SELECT
        self.to_game = False
        self.to_menu = False
        self.menu = pyasge.Sprite()
        self.map_1_photo = pyasge.Sprite()
        self.map_2_photo = pyasge.Sprite()
        self.map_3_photo = pyasge.Sprite()
        self.menu_text = None
        self.return_option = None
        self.map_1_option = None
        self.map_2_option = None
        self.map_3_option = None
        self.initBackground()
        self.initOption()
        self.current_option = -1
        self.going_left = False
        self.going_right = True
        self.current_diff = 2
        self.going_diff = False

        self.difficulty_easy = None
        self.difficulty_normal = None
        self.difficulty_hard = None
        self.initDifficulty()
        self.difficultySelect(2)

    def click_handler(self, event: pyasge.ClickEvent) -> None:
        if event.button == pyasge.MOUSE.MOUSE_BTN1:
            if event.action == pyasge.MOUSE.BUTTON_PRESSED:
                if self.is_inside(self.map_1_option, self.data.cursor.x, self.data.cursor.y):
                    self.to_game = True
                    self.data.selected_level = 1

                if self.is_inside(self.map_2_option, self.data.cursor.x, self.data.cursor.y):
                    self.to_game = True
                    self.data.selected_level = 2

                if self.is_inside(self.map_3_option, self.data.cursor.x, self.data.cursor.y):
                    self.to_game = True
                    self.data.selected_level = 3

                if self.is_inside(self.return_option, self.data.cursor.x, self.data.cursor.y):
                    self.to_menu = True

                if self.is_inside(self.difficulty_easy, self.data.cursor.x, self.data.cursor.y):
                    self.difficultySelect(1)
                    # print("Click Easy")

                if self.is_inside(self.difficulty_normal, self.data.cursor.x, self.data.cursor.y):
                    self.difficultySelect(2)

                if self.is_inside(self.difficulty_hard, self.data.cursor.x, self.data.cursor.y):
                    self.difficultySelect(3)

    def key_handler(self, event: pyasge.KeyEvent) -> None:
        pass

    def move_handler(self, event: pyasge.MoveEvent) -> None:
        if self.is_inside(self.map_1_option, self.data.cursor.x, self.data.cursor.y):
            self.map_1_option.colour = pyasge.COLOURS.DEEPSKYBLUE
        else:
            self.map_1_option.colour = pyasge.COLOURS.ALICEBLUE

        if self.is_inside(self.map_2_option, self.data.cursor.x, self.data.cursor.y):
            self.map_2_option.colour = pyasge.COLOURS.DEEPSKYBLUE
        else:
            self.map_2_option.colour = pyasge.COLOURS.ALICEBLUE

        if self.is_inside(self.map_3_option, self.data.cursor.x, self.data.cursor.y):
            self.map_3_option.colour = pyasge.COLOURS.DEEPSKYBLUE
        else:
            self.map_3_option.colour = pyasge.COLOURS.ALICEBLUE

        if self.is_inside(self.return_option, self.data.cursor.x, self.data.cursor.y):
            self.return_option.colour = pyasge.COLOURS.DEEPSKYBLUE
        else:
            self.return_option.colour = pyasge.COLOURS.ALICEBLUE

    def fixed_update(self, game_time: pyasge.GameTime) -> None:
        if self.data.gamepad.connected:
            if self.data.gamepad.AXIS_LEFT_X >= 0.5 or self.data.gamepad.AXIS_LEFT_X <= -0.5:
                if self.data.gamepad.AXIS_LEFT_X >= 0.5 and not self.going_right == True:
                    self.current_option += 1
                    self.going_right = True
                    if self.current_option >= 3:
                        self.current_option = 0
                elif self.data.gamepad.AXIS_LEFT_X <= -0.5 and not self.going_left == True:
                    self.current_option -= 1
                    self.going_left = True
                    if self.current_option <= -1:
                        self.current_option = 2
                self.text_colours()
            elif self.data.gamepad.AXIS_LEFT_Y >= 0.5 or self.data.gamepad.AXIS_LEFT_Y <= -0.5:
                if self.going_vertical == False:
                    if self.current_option == 3:
                        self.current_option = 1
                    else:
                        self.current_option = 3
                    self.going_vertical = True
                    self.text_colours()
            else:
                self.going_left = False
                self.going_right = False
                self.going_vertical = False
            if self.data.gamepad.RIGHT_BUMPER or self.data.gamepad.LEFT_BUMPER:
                if self.going_diff == False:
                    self.going_diff = True
                    if self.data.gamepad.RIGHT_BUMPER:
                        self.current_diff += 1
                        if self.current_diff >= 4:
                            self.current_diff = 1
                    if self.data.gamepad.LEFT_BUMPER:
                        self.current_diff -= 1
                        if self.current_diff <= 0:
                            self.current_diff = 3
                    self.difficultySelect(self.current_diff)
            else:
                self.going_diff = False
            if self.data.gamepad.A:
                if self.current_option == 0:
                    self.to_game = True
                    self.data.selected_level = 1
                if self.current_option == 1:
                    self.to_game = True
                    self.data.selected_level = 2
                if self.current_option == 2:
                    self.to_game = True
                    self.data.selected_level = 3
                if self.current_option == 3:
                    self.to_menu = True

    def update(self, game_time: pyasge.GameTime) -> GameStateID:
        if self.to_game:
            return GameStateID.GAMEPLAY
        if self.to_menu:
            return GameStateID.START_MENU

        return GameStateID.LEVEL_SELECT

    def render(self, game_time: pyasge.GameTime) -> None:
        self.data.renderer.render(self.menu)

        self.data.renderer.render(self.menu_text)
        self.data.renderer.render(self.return_option)

        self.data.renderer.render(self.map_1_option)
        self.data.renderer.render(self.map_2_option)
        self.data.renderer.render(self.map_3_option)

        self.data.renderer.render(self.map_1_photo)
        self.data.renderer.render(self.map_2_photo)
        self.data.renderer.render(self.map_3_photo)

        self.data.renderer.render(self.difficulty_easy)
        self.data.renderer.render(self.difficulty_normal)
        self.data.renderer.render(self.difficulty_hard)

    def initBackground(self) -> bool:
        if self.menu.loadTexture("/data/textures/mainMenuBackground.jpg"):
            # loaded, so make sure this gets rendered first
            self.menu.scale = 1.6
            self.menu.z_order = -100
            # print("New Background Works")

            self.menu_text = pyasge.Text(self.data.fonts["MenuFont"])
            self.menu_text.string = "Level Select"
            self.menu_text.position = [370, 200]
            self.menu_text.colour = pyasge.COLOURS.GAINSBORO
            self.menu_text.scale = 2
            # print(self.menu_text.world_bounds)

            self.return_option = pyasge.Text(self.data.fonts["MenuFont"])
            self.return_option.string = "Click To Return To Main Menu"
            self.return_option.position = [331, 1000]
            self.return_option.colour = pyasge.COLOURS.ALICEBLUE
            # print(self.return_option.world_bounds)

            return True
        else:
            return False

    def initOption(self):
        if self.map_1_photo.loadTexture("/data/map/map1.png"):
            self.map_1_photo.x = 120
            self.map_1_photo.y = 450
            self.map_1_photo.scale = 0.5

            self.map_1_option = pyasge.Text(self.data.fonts["MenuFont"])
            self.map_1_option.string = "Map 1"
            self.map_1_option.position = [242.5, 850]
            self.map_1_option.colour = pyasge.COLOURS.ALICEBLUE
            # print(self.map_1_option.world_bounds)
        else:
            print("Map 1 photo failed")

        if self.map_2_photo.loadTexture("/data/map/map2.png"):
            self.map_2_photo.x = 720
            self.map_2_photo.y = 450
            self.map_2_photo.scale = 0.5
            # print(self.map_2_photo.getWorldBounds())

            self.map_2_option = pyasge.Text(self.data.fonts["MenuFont"])
            self.map_2_option.string = "Map 2"
            self.map_2_option.position = [842.5, 850]
            self.map_2_option.colour = pyasge.COLOURS.ALICEBLUE
            # print(self.map_2_option.world_bounds)
        else:
            print("Map 2 photo failed")

        if self.map_3_photo.loadTexture("/data/map/map3.png"):
            self.map_3_photo.x = 1320
            self.map_3_photo.y = 450
            self.map_3_photo.scale = 0.5

            self.map_3_option = pyasge.Text(self.data.fonts["MenuFont"])
            self.map_3_option.string = "Map 3"
            self.map_3_option.position = [1442.5, 850]
            self.map_3_option.colour = pyasge.COLOURS.ALICEBLUE
            # print(self.map_3_option.world_bounds)
        else:
            print("Map 3 photo failed")

    def is_inside(self, text, mouse_x, mouse_y) -> bool:
        bounds = text.world_bounds
        # check to see if the mouse position falls within the x and y bounds of the sprite
        if bounds.v1.x < mouse_x < bounds.v2.x and bounds.v1.y < mouse_y < bounds.v3.y:
            return True
        return False

    def text_colours(self):
        if self.current_option == 0:
            self.map_1_option.colour = pyasge.COLOURS.DEEPSKYBLUE
            self.map_2_option.colour = pyasge.COLOURS.ALICEBLUE
            self.map_3_option.colour = pyasge.COLOURS.ALICEBLUE
            self.return_option.colour = pyasge.COLOURS.ALICEBLUE
        if self.current_option == 1:
            self.map_1_option.colour = pyasge.COLOURS.ALICEBLUE
            self.map_2_option.colour = pyasge.COLOURS.DEEPSKYBLUE
            self.map_3_option.colour = pyasge.COLOURS.ALICEBLUE
            self.return_option.colour = pyasge.COLOURS.ALICEBLUE
        if self.current_option == 2:
            self.map_1_option.colour = pyasge.COLOURS.ALICEBLUE
            self.map_2_option.colour = pyasge.COLOURS.ALICEBLUE
            self.map_3_option.colour = pyasge.COLOURS.DEEPSKYBLUE
            self.return_option.colour = pyasge.COLOURS.ALICEBLUE
        if self.current_option == 3:
            self.map_1_option.colour = pyasge.COLOURS.ALICEBLUE
            self.map_2_option.colour = pyasge.COLOURS.ALICEBLUE
            self.map_3_option.colour = pyasge.COLOURS.ALICEBLUE
            self.return_option.colour = pyasge.COLOURS.DEEPSKYBLUE
        if self.current_option == -1:
            self.map_1_option.colour = pyasge.COLOURS.ALICEBLUE
            self.map_2_option.colour = pyasge.COLOURS.ALICEBLUE
            self.map_3_option.colour = pyasge.COLOURS.ALICEBLUE
            self.return_option.colour = pyasge.COLOURS.ALICEBLUE

    def initDifficulty(self):
        self.difficulty_easy = pyasge.Text(self.data.fonts["MenuFont"])
        self.difficulty_easy.string = "Easy"
        self.difficulty_easy.position = [358.5, 350]
        self.difficulty_easy.colour = pyasge.COLOURS.ALICEBLUE
        # print(self.difficulty_easy.world_bounds)

        self.difficulty_normal = pyasge.Text(self.data.fonts["MenuFont"])
        self.difficulty_normal.string = "Normal"
        self.difficulty_normal.position = [797.5, 350]
        self.difficulty_normal.colour = pyasge.COLOURS.ALICEBLUE
        # print(self.difficulty_normal.world_bounds)

        self.difficulty_hard = pyasge.Text(self.data.fonts["MenuFont"])
        self.difficulty_hard.string = "Hard"
        self.difficulty_hard.position = [1358.5, 350]
        self.difficulty_hard.colour = pyasge.COLOURS.ALICEBLUE
        # print(self.difficulty_hard.world_bounds)

    def difficultySelect(self, option):
        if option == 1:
            self.difficulty_easy.colour = pyasge.COLOURS.DEEPSKYBLUE
            self.difficulty_normal.colour = pyasge.COLOURS.ALICEBLUE
            self.difficulty_hard.colour = pyasge.COLOURS.ALICEBLUE
            self.data.difficulty = Difficulty.EASY

        if option == 2:
            self.difficulty_easy.colour = pyasge.COLOURS.ALICEBLUE
            self.difficulty_normal.colour = pyasge.COLOURS.DEEPSKYBLUE
            self.difficulty_hard.colour = pyasge.COLOURS.ALICEBLUE
            self.data.difficulty = Difficulty.NORMAL

        if option == 3:
            self.difficulty_easy.colour = pyasge.COLOURS.ALICEBLUE
            self.difficulty_normal.colour = pyasge.COLOURS.ALICEBLUE
            self.difficulty_hard.colour = pyasge.COLOURS.DEEPSKYBLUE
            self.data.difficulty = Difficulty.HARD
