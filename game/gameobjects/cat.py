import pyasge
from game.gamedata import GameData
from game.catdata import CatData, CatType
from game.behaviourtree import BehaviourTreeCat, BehaviourTreeResourceCat, BehaviourTreeSlowCat, BehaviourTreeBoostCat


class Cat:
    def __init__(self, data: GameData, spawn: pyasge.Point2D, cat_type, targets):
        # Create sprite, position and data
        self.data = data
        self.sprite = pyasge.Sprite()
        # First textures for first frame of animation
        self.textures = ["/data/textures/cat_black_blocker_01.png", "/data/textures/cat_brown_01.png",
                         "/data/textures/cat_creme_01.png", "/data/textures/cat_radioactive_01.png",
                         "/data/textures/cat_blue_01.png", "/data/textures/cat_seal_point_01.png",
                         "/data/textures/cat_black_01.png", "/data/textures/cat_grey_tabby_01.png"]
        # Second textures for second frame of animation
        self.textures_2 = ["/data/textures/cat_black_blocker_02.png", "/data/textures/cat_brown_02.png",
                           "/data/textures/cat_creme_02.png", "/data/textures/cat_radioactive_02.png",
                           "/data/textures/cat_blue_02.png", "/data/textures/cat_seal_point_02.png",
                           "/data/textures/cat_black_02.png", "/data/textures/cat_grey_tabby_02.png"]
        self.sprite.loadTexture(self.textures[cat_type])
        self.sprite.texture.setMagFilter(pyasge.MagFilter.NEAREST)
        self.sprite.width = 128
        self.sprite.height = 128
        self.sprite.x = spawn.x
        self.sprite.y = spawn.y
        self.sprite.z_order = 50
        self.cat_data = CatData(cat_type)

        # Alter stats based on cat type
        if cat_type == CatType.SCRATCH:
            self.cat_data.attack_range = 128
            self.cat_data.reload_time = 1

        elif cat_type == CatType.RADIOACTIVE:
            self.cat_data.attack_range = 512
            self.cat_data.reload_time = 1

        # Create AI trees based on cat type
        if cat_type == CatType.RESOURCE:
            self.behaviour_tree = BehaviourTreeResourceCat(data, self)
            self.cat_data.reload_time = 3
        elif cat_type == CatType.TIME:
            self.behaviour_tree = BehaviourTreeSlowCat(data, self, targets, self.cat_data)
        elif cat_type == CatType.BOOSTER:
            self.behaviour_tree = BehaviourTreeBoostCat(data, self, targets, self.cat_data)
        elif cat_type == CatType.BLOCKER:
            self.behaviour_tree = None
            # Update the tile map costs if the cat is a blocker
            tile = self.data.game_map.tile(pyasge.Point2D(spawn.x + 32, spawn.y + 32))
            self.data.game_map.costs[tile[1]][tile[0]] += 20
        else:
            self.behaviour_tree = BehaviourTreeCat(data, self, targets, self.cat_data)

    def update(self, game_time: pyasge.GameTime):

        # Animation update
        self.cat_data.anim_timer += game_time.frame_time

        # If timer is reached, swap the sprites to animate the cat
        if self.cat_data.anim_timer >= self.cat_data.anim_speed:
            if self.cat_data.current_sprite_num == 0:
                self.sprite.loadTexture(self.textures_2[self.cat_data.cat_type])
                self.cat_data.current_sprite_num = 1
                self.sprite.texture.setMagFilter(pyasge.MagFilter.NEAREST)
                self.sprite.width = 128
                self.sprite.height = 128
            else:
                self.sprite.loadTexture(self.textures[self.cat_data.cat_type])
                self.cat_data.current_sprite_num = 0
                self.sprite.texture.setMagFilter(pyasge.MagFilter.NEAREST)
                self.sprite.width = 128
                self.sprite.height = 128
            self.cat_data.anim_timer = 0

        # AI update
        if self.behaviour_tree is not None:
            self.behaviour_tree.update(game_time)

        # Rodent in attack range -> [Attack]

    def render(self, renderer: pyasge.Renderer, game_time: pyasge.GameTime) -> None:
        renderer.render(self.sprite)
