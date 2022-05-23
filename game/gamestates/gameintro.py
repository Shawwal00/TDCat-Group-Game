import pyasge

from game.gamestates.gamestate import GameState
from game.gamestates.gamestate import GameStateID
from game.gamedata import GameData


class GameIntro(GameState):

    def __init__(self, gamedata: GameData) -> None:
        super().__init__(gamedata)
        self.id = GameStateID.INTRO
        self.transition = False
        self.menu = pyasge.Sprite()
        self.menu_text = None
        self.return_option = None
        self.initBackground()

        # Generate sprites for each cat
        self.cat_default = pyasge.Sprite()
        self.cat_melee = pyasge.Sprite()
        self.cat_super = pyasge.Sprite()
        self.cat_freeze = pyasge.Sprite()
        self.cat_slow = pyasge.Sprite()
        self.cat_team = pyasge.Sprite()
        self.cat_money = pyasge.Sprite()
        self.cat_sleepy = pyasge.Sprite()

        # Generate text for each cat
        self.cat_default_text = None
        self.cat_melee_text = None
        self.cat_super_text = None
        self.cat_freeze_text = None
        self.cat_slow_text = None
        self.cat_team_text = None
        self.cat_money_text = None
        self.cat_sleepy_text = None

        self.initCatInfo()

    def click_handler(self, event: pyasge.ClickEvent) -> None:
        if event.button == pyasge.MOUSE.MOUSE_BTN1:
            if event.action == pyasge.MOUSE.BUTTON_PRESSED:
                self.transition = True  # Change

    def key_handler(self, event: pyasge.KeyEvent) -> None:
        pass

    def move_handler(self, event: pyasge.MoveEvent) -> None:
        pass

    def fixed_update(self, game_time: pyasge.GameTime) -> None:
        pass

    def update(self, game_time: pyasge.GameTime) -> GameStateID:
        if self.data.gamepad.connected:
            if self.data.gamepad.A and not self.data.prev_gamepad.A:
                self.transition = True
        if self.transition:
            return GameStateID.START_MENU

        return GameStateID.INTRO

    def render(self, game_time: pyasge.GameTime) -> None:
        self.data.renderer.render(self.menu)

        self.data.renderer.render(self.menu_text)
        self.data.renderer.render(self.return_option)

        self.data.renderer.render(self.cat_default)
        self.data.renderer.render(self.cat_default_text)

        self.data.renderer.render(self.cat_melee)
        self.data.renderer.render(self.cat_melee_text)

        self.data.renderer.render(self.cat_super)
        self.data.renderer.render(self.cat_super_text)

        self.data.renderer.render(self.cat_freeze)
        self.data.renderer.render(self.cat_freeze_text)

        self.data.renderer.render(self.cat_slow)
        self.data.renderer.render(self.cat_slow_text)

        self.data.renderer.render(self.cat_team)
        self.data.renderer.render(self.cat_team_text)

        self.data.renderer.render(self.cat_money)
        self.data.renderer.render(self.cat_money_text)

        self.data.renderer.render(self.cat_sleepy)
        self.data.renderer.render(self.cat_sleepy_text)

    def initBackground(self) -> bool:
        if self.menu.loadTexture("/data/textures/mainMenuBackground.jpg"):
            self.menu.scale = 1.6
            self.menu.z_order = -100

            self.menu_text = pyasge.Text(self.data.fonts["MenuFont"])
            self.menu_text.string = "Intro Screen"
            self.menu_text.position = [402, 200]
            self.menu_text.colour = pyasge.COLOURS.GAINSBORO
            self.menu_text.scale = 2

            self.return_option = pyasge.Text(self.data.fonts["MenuFont"])
            self.return_option.string = "Click Anywhere To Return To Menu"
            self.return_option.position = [209, 1000]
            self.return_option.colour = pyasge.COLOURS.ALICEBLUE

            return True
        else:
            return False

    def initCatInfo(self):
        self.cat_default.loadTexture("/data/textures/cat_brown_01.png")
        self.cat_default.setMagFilter(pyasge.MagFilter.NEAREST)
        self.cat_default.x = 50
        self.cat_default.y = 200
        self.cat_default.scale = 5
        self.cat_default_text = pyasge.Text(self.data.fonts["MenuFont"])
        self.cat_default_text.scale = 0.5
        self.cat_default_text.string = "Furball - The default cat,\nmedium range, medium attack speed"
        self.cat_default_text.position = [200, 250]

        self.cat_melee.loadTexture("/data/textures/cat_creme_01.png")
        self.cat_melee.setMagFilter(pyasge.MagFilter.NEAREST)
        self.cat_melee.x = 50
        self.cat_melee.y = 400
        self.cat_melee.scale = 5
        self.cat_melee_text = pyasge.Text(self.data.fonts["MenuFont"])
        self.cat_melee_text.scale = 0.5
        self.cat_melee_text.string = "Scratch - The melee cat,\nshort range, high attack speed"
        self.cat_melee_text.position = [200, 450]

        self.cat_super.loadTexture("/data/textures/cat_radioactive_01.png")
        self.cat_super.setMagFilter(pyasge.MagFilter.NEAREST)
        self.cat_super.x = 50
        self.cat_super.y = 600
        self.cat_super.scale = 5
        self.cat_super_text = pyasge.Text(self.data.fonts["MenuFont"])
        self.cat_super_text.scale = 0.5
        self.cat_super_text.string = "Radioactive - The super cat,\nlarge range, high attack speed"
        self.cat_super_text.position = [200, 650]

        self.cat_freeze.loadTexture("/data/textures/cat_grey_tabby_01.png")
        self.cat_freeze.setMagFilter(pyasge.MagFilter.NEAREST)
        self.cat_freeze.x = 50
        self.cat_freeze.y = 800
        self.cat_freeze.scale = 5
        self.cat_freeze_text = pyasge.Text(self.data.fonts["MenuFont"])
        self.cat_freeze_text.scale = 0.5
        self.cat_freeze_text.string = "Stun - The freeze cat,\nfreezes rodents in place"
        self.cat_freeze_text.position = [200, 850]

        self.cat_slow.loadTexture("//data/textures/cat_blue_01.png")
        self.cat_slow.setMagFilter(pyasge.MagFilter.NEAREST)
        self.cat_slow.x = 1050
        self.cat_slow.y = 200
        self.cat_slow.scale = 5
        self.cat_slow_text = pyasge.Text(self.data.fonts["MenuFont"])
        self.cat_slow_text.scale = 0.5
        self.cat_slow_text.string = "Time - The slow cat,\nslows down rodent's speed"
        self.cat_slow_text.position = [1200, 250]

        self.cat_team.loadTexture("/data/textures/cat_seal_point_01.png")
        self.cat_team.setMagFilter(pyasge.MagFilter.NEAREST)
        self.cat_team.x = 1050
        self.cat_team.y = 400
        self.cat_team.scale = 5
        self.cat_team_text = pyasge.Text(self.data.fonts["MenuFont"])
        self.cat_team_text.scale = 0.5
        self.cat_team_text.string = "Booster - The team cat,\nboosts other cats in range"
        self.cat_team_text.position = [1200, 450]

        self.cat_money.loadTexture("/data/textures/cat_black_01.png")
        self.cat_money.setMagFilter(pyasge.MagFilter.NEAREST)
        self.cat_money.x = 1050
        self.cat_money.y = 600
        self.cat_money.scale = 5
        self.cat_money_text = pyasge.Text(self.data.fonts["MenuFont"])
        self.cat_money_text.scale = 0.5
        self.cat_money_text.string = "Resource - The money cat,\nproduces yarn over time"
        self.cat_money_text.position = [1200, 650]

        self.cat_sleepy.loadTexture("/data/textures/cat_black_blocker_01.png")
        self.cat_sleepy.setMagFilter(pyasge.MagFilter.NEAREST)
        self.cat_sleepy.x = 1050
        self.cat_sleepy.y = 800
        self.cat_sleepy.scale = 5
        self.cat_sleepy_text = pyasge.Text(self.data.fonts["MenuFont"])
        self.cat_sleepy_text.scale = 0.5
        self.cat_sleepy_text.string = "Blocker - The sleepy cat,\nblocks rodents"
        self.cat_sleepy_text.position = [1200, 850]
