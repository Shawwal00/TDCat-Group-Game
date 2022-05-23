import pyasge

from game import gamedata
from game.gamedata import GameData
from game.gameobjects.catinfo import CatInfo


class Shop:
    def __init__(self, data: GameData, spawn: pyasge.Point2D, terrain, yarn):
        self.data = data
        # If cost of tile selected is high
        if terrain <= 5:
            # Set road to true to be used for blocker cats
            self.road = True
        else:
            # Create left and right option
            self.road = False
            self.left_arrow = pyasge.Sprite()
            self.left_arrow.loadTexture("/data/textures/UI_grey_buttons_1.png")
            self.left_arrow.setMagFilter(pyasge.MagFilter.NEAREST)
            self.left_arrow.width = 32
            self.left_arrow.height = 32
            self.left_arrow.src_rect = [0, 16, 16, 16]
            self.left_arrow.x = spawn.x - 67
            self.left_arrow.y = spawn.y - 20
            self.left_arrow.z_order = 70

            self.right_arrow = pyasge.Sprite()
            self.right_arrow.loadTexture("/data/textures/UI_grey_buttons_1.png")
            self.right_arrow.setMagFilter(pyasge.MagFilter.NEAREST)
            self.right_arrow.width = 32
            self.right_arrow.height = 32
            self.right_arrow.src_rect = [32, 0, 16, 16]
            self.right_arrow.x = spawn.x + 33
            self.right_arrow.y = spawn.y - 20
            self.right_arrow.z_order = 70

        self.tick_box = pyasge.Sprite()
        self.negative_tick = "/data/textures/UI_orange_buttons_3.png"
        self.positive_tick = "/data/textures/UI_grey_buttons_1.png"
        self.tick_box.loadTexture("/data/textures/UI_grey_buttons_1.png")
        self.tick_box.setMagFilter(pyasge.MagFilter.NEAREST)
        self.tick_box.width = 32
        self.tick_box.height = 32
        self.tick_box.src_rect = [0, 64, 16, 16]
        self.tick_box.x = spawn.x - 17
        self.tick_box.y = spawn.y + 25
        self.tick_box.z_order = 50

        self.cat_place = pyasge.Point2D((spawn.x - 32), (spawn.y - 35))
        # load all the cat textures, and put them in one big array
        if self.road:
            self.cat_list = ["/data/textures/cat_black_blocker_01.png"]
            if yarn < 40:
                self.tick_box.loadTexture(self.negative_tick)
                self.tick_box.src_rect = [16, 48, 16, 16]
            else:
                self.tick_box.loadTexture(self.positive_tick)
                self.tick_box.src_rect = [0, 64, 16, 16]
        else:
            self.cat_list = ["/data/textures/cat_brown_01.png",
                             "/data/textures/cat_creme_01.png", "/data/textures/cat_radioactive_01.png",
                             "/data/textures/cat_blue_01.png", "/data/textures/cat_seal_point_01.png",
                             "/data/textures/cat_black_01.png", "/data/textures/cat_grey_tabby_01.png"]
        self.cat_num = 0
        self.cat_max = len(self.cat_list)
        self.display_cat = pyasge.Sprite()
        self.display_cat.loadTexture(self.cat_list[self.cat_num])
        self.display_cat.setMagFilter(pyasge.MagFilter.NEAREST)
        self.display_cat.width = 64
        self.display_cat.height = 64
        self.display_cat.x = self.cat_place.x
        self.display_cat.y = self.cat_place.y
        self.display_cat.z_order = 50
        self.load_cat(0)

        # Create display for cat before to allow scrolling
        self.cat_before_num = 0
        self.display_cat_before = pyasge.Sprite()
        self.display_cat_before.loadTexture(self.cat_list[self.cat_num])
        self.display_cat_before.setMagFilter(pyasge.MagFilter.NEAREST)
        self.display_cat_before.width = 64
        self.display_cat_before.height = 64
        self.display_cat_before.x = self.cat_place.x
        self.display_cat_before.y = self.cat_place.y
        self.display_cat.z_order = 50

        if self.road:
            self.info = CatInfo(self.data, 0)
        else:
            self.info = CatInfo(self.data, self.cat_num + 1)

        self.right_pressed = 0
        self.key_pressed = 0
        self.scrolling_time = 2.2
        self.first_click = False

    def load_cat(self, num):
        # loads the texture of the next cat
        self.display_cat.loadTexture(self.cat_list[num])
        self.display_cat.setMagFilter(pyasge.MagFilter.NEAREST)
        self.display_cat.width = 64
        self.display_cat.height = 64
        self.display_cat.x = self.cat_place.x
        self.display_cat.y = self.cat_place.y

    def Update(self, yarn):
        # update state of tick box to new yarn costs
        if self.road:
            if yarn < self.data.cat_costs[0]:
                self.tick_box.loadTexture(self.negative_tick)
                self.tick_box.src_rect = [16, 48, 16, 16]
            else:
                self.tick_box.loadTexture(self.positive_tick)
                self.tick_box.src_rect = [0, 64, 16, 16]
        else:
            if yarn < self.data.cat_costs[self.cat_num + 1]:
                self.tick_box.loadTexture(self.negative_tick)
                self.tick_box.src_rect = [16, 48, 16, 16]
            else:
                self.tick_box.loadTexture(self.positive_tick)
                self.tick_box.src_rect = [0, 64, 16, 16]
        self.tick_box.height = 32
        self.tick_box.width = 32

    def load_cat_before(self, num):
        self.display_cat_before.loadTexture(self.cat_list[num])
        self.display_cat_before.setMagFilter(pyasge.MagFilter.NEAREST)
        self.display_cat_before.width = 64
        self.display_cat_before.height = 64
        self.display_cat_before.x = self.cat_place.x
        self.display_cat_before.y = self.cat_place.y

    def is_inside(self, sprite, mouse_x, mouse_y) -> bool:
        bounds = sprite.getWorldBounds()
        # check to see if the mouse position falls within the x and y bounds of the sprite
        if bounds.v1.x < mouse_x < bounds.v2.x and bounds.v1.y < mouse_y < bounds.v3.y:
            return True
        return False

    def menu_click(self, mouse_x, mouse_y, yarn):
        if self.scrolling_time > 2:
            # if the buy menu is open, run this to see if the player clicks on one of the buttons
            # if button is pressed, then cycle to the next cat in the list
            left_press = False
            right_press = False
            tick = False
            if self.data.gamepad.connected:
                if self.data.gamepad.AXIS_LEFT_X <= -0.5 and not self.data.prev_gamepad.AXIS_LEFT_X <= -0.5:
                    left_press = True
                elif self.data.gamepad.AXIS_LEFT_X >= 0.5 and not self.data.prev_gamepad.AXIS_LEFT_X >= 0.5:
                    right_press = True
                if self.data.gamepad.A:
                    tick = True
            if not self.road:
                if self.is_inside(self.left_arrow, mouse_x, mouse_y) or left_press == True:
                    self.scrolling_time = 1
                    self.key_pressed = 2
                    # if button is pressed, then cycle to the previous cat in the list
                    self.cat_num -= 1
                    if self.cat_num < 0:  # loops around if the number exceeds the list bounds
                        self.cat_num = self.cat_max - 1
                    self.cat_before_num = self.cat_num
                    if self.cat_before_num >= self.cat_max - 1:
                        self.cat_before_num = -1
                    self.load_cat_before(self.cat_before_num + 1)
                    self.load_cat(self.cat_num)  # loads the new cat
                    self.info.load_cat(self.cat_num)
                    return -1
                elif self.is_inside(self.right_arrow, mouse_x, mouse_y) or right_press == True:
                    self.scrolling_time = 1
                    self.key_pressed = 1
                    # same as above, but with the next cat instead
                    self.cat_num += 1
                    if self.cat_num >= self.cat_max:
                        self.cat_num = 0
                    self.cat_before_num = self.cat_num
                    self.load_cat(self.cat_num)
                    self.load_cat_before(self.cat_before_num - 1)
                    self.info.load_cat(self.cat_num)
                    return -1
            if self.is_inside(self.tick_box, mouse_x, mouse_y) or tick:
                # if the tick is clicked, return the number of the desired cat
                if not self.road:
                    return self.cat_num + 1
                return self.cat_num
            else:
                return -1  # when not choosing a cat, return -1, so it doesnt spawn
        else:
            return -1  # when not choosing a cat, return -1, so it doesnt spawn one

    def render(self, renderer: pyasge.Renderer, game_time: pyasge.GameTime) -> None:
        # The below is setting up thr scrolling shader
        self.scrolling_time = self.scrolling_time + game_time.fixed_timestep
        self.data.shaders["scrolling"].uniform("rgb").set([1, 1, 1])
        self.data.shaders["scrolling"].uniform("time").set(self.scrolling_time)
        self.data.shaders["scrolling"].uniform("pressed").set(self.key_pressed)
        if not self.road:  # Only will happen if its is not on the path
            renderer.render(self.left_arrow)
            renderer.render(self.right_arrow)
        renderer.render(self.tick_box)
        self.info.render(self.data.renderer, game_time)
        if self.key_pressed < 1:
            renderer.render(self.display_cat_before)

        # The below is if the left arrow is pressed
        if self.key_pressed == 2:
            self.data.renderer.shader = self.data.shaders["scrolling"]
            self.display_cat.x = self.cat_place.x + 40
            renderer.render(self.display_cat)
            renderer.render(self.display_cat_before)
            if self.scrolling_time > 2.0:
                self.data.renderer.shader = self.data.shaders["main"]
                self.display_cat.x = self.cat_place.x
                renderer.render(self.display_cat)

        # The below is if the right arrow is pressed
        if self.key_pressed == 1:
            self.data.renderer.shader = self.data.shaders["scrolling"]
            self.display_cat.x = self.cat_place.x - 40
            renderer.render(self.display_cat)
            renderer.render(self.display_cat_before)
            if self.scrolling_time > 2.0:
                self.data.renderer.shader = self.data.shaders["main"]
                self.display_cat.x = self.cat_place.x
                renderer.render(self.display_cat)

        self.data.renderer.shader = self.data.shaders["main"]
