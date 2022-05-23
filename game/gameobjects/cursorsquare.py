import pyasge
from game.gamedata import GameData


class Square:
    def __init__(self, tile: tuple, spawn: pyasge.Point2D):
        # Create sprite which follows where the user is highlighting
        self.tile_square = pyasge.Sprite()
        self.tile_square.loadTexture("/data/textures/cursors.png")
        self.tile_square.width = 64
        self.tile_square.height = 64
        self.tile_square.src_rect = [32, 48, 16, 16]
        self.tilex = tile[0]
        self.tiley = tile[1]
        self.tile_square.x = spawn.x - 32
        self.tile_square.y = spawn.y - 32
        self.tile_square.z_order = 25

    def move(self, new: pyasge.Point2D):
        self.tile_square.x = new.x -32
        self.tile_square.y = new.y -32

    def render(self, renderer: pyasge.Renderer, game_time: pyasge.GameTime) -> None:
        renderer.render(self.tile_square)