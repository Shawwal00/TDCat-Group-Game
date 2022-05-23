import random
import pyasge

from enum import IntEnum
from game.gamedata import GameData
from game.gameobjects.gamemap import GameMap
from game.gamestates.gamestate import GameStateID
from game.gamestates.gameplay import GamePlay
from game.gamestates.gamemenu import GameMenu
from game.gamestates.gameover import GameOver
from game.gamestates.gamewon import GameWon
from game.gamestates.gamepause import GamePause
from game.gamestates.gameintro import GameIntro
from game.gamestates.gameselect import GameSelect
from pyfmodex.flags import MODE

class MyASGEGame(pyasge.ASGEGame):
    """The ASGE Game in Python."""

    def __init__(self, settings: pyasge.GameSettings):
        """
        The constructor for the game.

        The constructor is responsible for initialising all the needed
        subsystems,during the game's running duration. It directly
        inherits from pyasge.ASGEGame which provides the window
        management and standard game loop.

        :param settings: The game settings
        """
        pyasge.ASGEGame.__init__(self, settings)
        self.data = GameData()
        self.renderer.setBaseResolution(self.data.game_res[0], self.data.game_res[1], pyasge.ResolutionPolicy.MAINTAIN)
        random.seed(a=None, version=2)

        self.data.game_map = GameMap(self.renderer, "./data/map/map1.tmx")
        self.data.inputs = self.inputs
        self.data.renderer = self.renderer
        self.data.shaders["example"] = self.data.renderer.loadPixelShader("/data/shaders/example_rgb.frag")
        self.data.shaders["grass_test"] = self.data.renderer.loadPixelShader("/data/shaders/grass.frag")
        self.data.shaders["main"] = self.data.renderer.loadPixelShader("/data/shaders/main.frag")
        self.data.shaders["flash"] = self.data.renderer.loadPixelShader("/data/shaders/flash.frag")
        self.data.shaders["flash_stun"] = self.data.renderer.loadPixelShader("/data/shaders/flash.frag")
        self.data.shaders["flash_green"] = self.data.renderer.loadPixelShader("/data/shaders/flash.frag")
        self.data.shaders["light"] = self.data.renderer.loadPixelShader("/data/shaders/light_grass.frag")
        self.data.shaders["scrolling"] = self.data.renderer.loadPixelShader("/data/shaders/Scrolling.frag")
        self.data.shaders["invisibility"] = self.data.renderer.loadPixelShader("/data/shaders/invisibility.frag")
        self.data.prev_gamepad = self.data.gamepad = self.inputs.getGamePad()

        # setup the background and load the fonts for the game
        self.init_audio()
        self.init_cursor()
        self.init_fonts()

        # register the key and mouse click handlers for this class
        self.key_id = self.data.inputs.addCallback(pyasge.EventType.E_KEY, self.key_handler)
        self.mouse_id = self.data.inputs.addCallback(pyasge.EventType.E_MOUSE_CLICK, self.click_handler)
        self.mousemove_id = self.data.inputs.addCallback(pyasge.EventType.E_MOUSE_MOVE, self.move_handler)

        # start the game in the menu
        #self.current_state = GamePlay(self.data)
        self.current_state = GameMenu(self.data)
        self.state_game = None
        self.restart_game(1)

    def init_cursor(self):
        """Initialises the mouse cursor and hides the OS cursor."""
        self.data.cursor = pyasge.Sprite()
        self.data.cursor.loadTexture("/data/textures/cursors.png")
        self.data.cursor.width = 11
        self.data.cursor.height = 11
        self.data.cursor.src_rect = [0, 0, 11, 11]
        self.data.cursor.scale = 4
        self.data.cursor.setMagFilter(pyasge.MagFilter.NEAREST)
        self.data.cursor.z_order = 110
        self.data.inputs.setCursorMode(pyasge.CursorMode.HIDDEN)

    def init_audio(self) -> None:
        """Plays the background audio."""
        self.data.audio_system.init()
        self.data.bg_audio = self.data.audio_system.create_sound("./data/audio/rustling-leaves-6875.ogg",
                                                                 mode=MODE.LOOP_NORMAL)
        self.data.bg_audio_channel = self.data.audio_system.play_sound(self.data.bg_audio)
        self.data.bg_audio_channel.volume = 0.25

    def init_fonts(self) -> None:
        """Loads the game fonts."""
        self.data.fonts["MenuFont"] = self.data.renderer.loadFont("/data/fonts/Kenney Future.ttf", 64)

    def move_handler(self, event: pyasge.MoveEvent) -> None:
        """Handles the mouse movement and delegates to the active state."""
        self.data.cursor.x = event.x
        self.data.cursor.y = event.y
        self.current_state.move_handler(event)

    def click_handler(self, event: pyasge.ClickEvent) -> None:
        """Forwards click events on to the active state."""
        self.current_state.click_handler(event)

    def key_handler(self, event: pyasge.KeyEvent) -> None:
        """Forwards Key events on to the active state."""
        self.current_state.key_handler(event)
        #if event.key == pyasge.KEYS.KEY_ESCAPE:
            #self.signalExit()

    def fixed_update(self, game_time: pyasge.GameTime) -> None:
        """Processes fixed updates."""
        self.current_state.fixed_update(game_time)
        self.data.audio_system.update()

    def update(self, game_time: pyasge.GameTime) -> None:
        self.data.gamepad = self.inputs.getGamePad()
        self.current_state.update(game_time)
        self.data.prev_gamepad = self.data.gamepad

        new_state = self.current_state.update(game_time)
        if self.current_state.id != new_state:
            if new_state is GameStateID.START_MENU:
                self.restart_game(1)
                self.current_state = GameMenu(self.data)
            elif new_state is GameStateID.GAMEPLAY:
                if self.current_state.id == GameStateID.LEVEL_SELECT:
                    self.restart_game(self.data.selected_level)
                self.current_state = self.state_game
                self.current_state.to_pause = False
            elif new_state is GameStateID.WINNER_WINNER:
                self.current_state = GameWon(self.data)
            elif new_state is GameStateID.GAME_OVER:
                self.current_state = GameOver(self.data)
            elif new_state is GameStateID.PAUSE:
                self.current_state = GamePause(self.data)
            elif new_state is GameStateID.INTRO:
                self.current_state = GameIntro(self.data)
            elif new_state is GameStateID.LEVEL_SELECT:
                self.current_state = GameSelect(self.data)

    def render(self, game_time: pyasge.GameTime) -> None:
        """Renders the game state and mouse cursor"""
        if self.current_state.id == GameStateID.PAUSE:
            self.state_game.render(game_time)
        self.current_state.render(game_time)
        self.renderer.render(self.data.cursor)

    def restart_game(self, level: int):
        self.state_game = GamePlay(self.data)
        self.data.yarn = 80
        self.data.hp = self.data.max_hp
        if level == 1:
            self.data.game_map = GameMap(self.renderer, "./data/map/map1.tmx")
        elif level == 2:
            self.data.game_map = GameMap(self.renderer, "./data/map/map2.tmx")
        else:
            self.data.game_map = GameMap(self.renderer, "./data/map/map3.tmx")
