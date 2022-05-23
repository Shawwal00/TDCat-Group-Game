import pyasge
import pyfmodex
from enum import IntEnum


class Difficulty(IntEnum):
    EASY = 1,
    NORMAL = 2,
    HARD = 3


class GameData:
    """
    GameData stores the data that needs to be shared

    When using multiple states in a game, you will find that
    some game data needs to be shared. GameData can be used to
    share access to data that the game and any running states may
    need.
    """

    def __init__(self) -> None:
        # Fixed Data
        self.cat_costs = [40, 20, 30, 200, 80, 60, 60, 50]
        self.max_hp = 5

        # Recorded Data
        self.selected_level = 1
        self.hp = 5
        self.yarn = 80
        self.difficulty = Difficulty.NORMAL

        # Engine Data
        self.audio_system = pyfmodex.System()
        self.bg_audio = None
        self.bg_audio_channel = None
        self.cursor = None
        self.fonts = {}
        self.game_map = None
        self.game_res = [1920, 1080]
        self.inputs = None
        self.gamepad = None
        self.prev_gamepad = None
        self.renderer = None
        self.shaders: dict[str, pyasge.Shader] = {}
