import pyasge
from game.gamedata import GameData


class CatInfo:
    def __init__(self, data: GameData, cat_num):
        self.data = data

        self.display_cat = pyasge.Sprite()
        self.description = pyasge.Text(self.data.fonts["MenuFont"])
        self.yarn_number = pyasge.Text(self.data.fonts["MenuFont"])
        # sets up the display for the blocker cat
        if cat_num == 0:
            self.display_cat.loadTexture("/data/textures/cat_black_blocker_01.png")
            self.display_cat.width = 128
            self.display_cat.height = 128
            self.display_cat.x = 576
            self.display_cat.y = 928
            self.description.string = "lays in the path and\nblocks the rodents"
            self.yarn_number.string = "40"
        # sets up the display arrays for all the other cats
        else:
            self.cat_list = ["/data/textures/cat_brown_01.png",
                             "/data/textures/cat_creme_01.png", "/data/textures/cat_radioactive_01.png",
                             "/data/textures/cat_blue_01.png", "/data/textures/cat_seal_point_01.png",
                             "/data/textures/cat_black_01.png", "/data/textures/cat_grey_tabby_01.png"]
            self.text_list = ["shoots hairballs over\na medium range,\naverage speed",
                              "close-range,\nhigh-speed furballs",
                              "long range, high power\nradioactive furballs",
                              "slows down rodents in\nan area around them",
                              "increases the firerate\nof surrounding cats",
                              "passively generates\nextra yarn",
                              "shoots projectiles\nthat stun targets"]
            self.load_cat(cat_num - 1)
        self.display_cat.z_order = 50

        # Create entire box UI
        self.info_box = pyasge.Sprite()
        self.info_box.loadTexture("data/textures/ui_cat_info.png")
        self.info_box.setMagFilter(pyasge.MagFilter.NEAREST)
        self.info_box.width = 768
        self.info_box.height = 128
        self.info_box.x = 576
        self.info_box.y = 928
        self.info_box.z_order = 40

        # Create description text
        self.description.scale = 0.5
        self.description.x = 704
        self.description.y = 960
        self.description.z_order = 50

        # Create yarn number
        self.yarn_number.scale = 0.5
        self.yarn_number.x = 1248
        self.yarn_number.y = 1046
        self.yarn_number.z_order = 50

        # Create yarn image
        self.yarn_symbol = pyasge.Sprite()
        self.yarn_symbol.loadTexture("data/textures/ui_yarn.png")
        self.yarn_symbol.setMagFilter(pyasge.MagFilter.NEAREST)
        self.yarn_symbol.width = 64
        self.yarn_symbol.height = 64
        self.yarn_symbol.x = 1240
        self.yarn_symbol.y = 940
        self.yarn_symbol.z_order = 50

    def load_cat(self, num):
        # loads the image and description of the current cat when the display changes
        self.display_cat.loadTexture(self.cat_list[num])
        self.display_cat.setMagFilter(pyasge.MagFilter.NEAREST)
        self.display_cat.width = 128
        self.display_cat.height = 128
        self.display_cat.x = 576
        self.display_cat.y = 928
        # changes the description and cost
        self.description.string = self.text_list[num]
        self.yarn_number.string = str(self.data.cat_costs[num + 1])

    def render(self, renderer: pyasge.Renderer, game_time: pyasge.GameTime) -> None:
        renderer.render(self.info_box)
        renderer.render(self.display_cat)
        renderer.render(self.description)
        renderer.render(self.yarn_symbol)
        renderer.render(self.yarn_number)