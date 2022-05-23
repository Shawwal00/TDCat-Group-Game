import pyasge
import math
from game.gamedata import GameData
from game.rodentdata import RodentData, RodentType
from game.behaviourtree import BehaviourTreeRodent
from game.gamedata import Difficulty


class Rodent:
    def __init__(self, data: GameData, spawn: pyasge.Point2D, rodent_type, cats):
        # Generate sprite, position and data
        self.data = data
        self.sprite = pyasge.Sprite()
        # First textures for first frame of animation
        self.textures = [
            "/data/textures/hamster_01.png", "/data/textures/guinea_01.png", "/data/textures/hedgehog_01.png"
            , "/data/textures/mouse_01.png", "/data/textures/squirrel_01.png", "/data/textures/gerbil_01.png"
            , "/data/textures/chinchilla_01.png", "/data/textures/chipmunk_01.png", "/data/textures/ferret_01.png"]
        # Second textures for second frame of animation
        self.textures_2 = [
            "/data/textures/hamster_02.png", "/data/textures/guinea_02.png", "/data/textures/hedgehog_02.png"
            , "/data/textures/mouse_02.png", "/data/textures/squirrel_02.png", "/data/textures/gerbil_02.png"
            , "/data/textures/chinchilla_02.png", "/data/textures/chipmunk_02.png", "/data/textures/ferret_02.png"]
        self.sprite.loadTexture(self.textures[rodent_type])
        self.sprite.texture.setMagFilter(pyasge.MagFilter.NEAREST)
        self.sprite.width = 32
        self.sprite.height = 32
        self.sprite.x = spawn.x - 16
        self.sprite.y = spawn.y - 16
        self.sprite.z_order = 50
        self.destination = []
        self.direction = pyasge.Point2D(0, 0)
        self.rodent_data = RodentData(rodent_type)

        # Alter stats depending on rodent type
        if rodent_type == RodentType.MICE:
            self.rodent_data.hp = self.rodent_data.hp * 0.5
            self.rodent_data.low_hp_range = 1
            self.rodent_data.speed = self.rodent_data.speed * 2
        elif rodent_type == RodentType.GUINEA:
            self.rodent_data.hp = self.rodent_data.hp * 2
            self.rodent_data.low_hp_range = 3
            self.rodent_data.speed = self.rodent_data.speed * 0.5
        elif rodent_type == RodentType.HEDGEHOG:
            self.rodent_data.hp = self.rodent_data.hp * 1.5
            self.rodent_data.low_hp_range = 3
            self.rodent_data.previous_hp = self.rodent_data.hp
            self.rodent_data.speed = self.rodent_data.speed * 0.75

        self.behaviour_tree = BehaviourTreeRodent(data, self, cats)
        if rodent_type == RodentType.MICE or rodent_type == RodentType.CHIPMUNK or rodent_type == RodentType.FERRET:
            self.rodent_data.can_hidden_path = True

        # Alter stats on difficulty
        if data.difficulty == Difficulty.EASY:
            self.rodent_data.hp = self.rodent_data.hp * 0.75
            self.rodent_data.speed = self.rodent_data.speed * 0.75
        elif data.difficulty == Difficulty.NORMAL:
            self.rodent_data.hp = self.rodent_data.hp
        elif data.difficulty == Difficulty.HARD:
            self.rodent_data.hp = self.rodent_data.hp * 1.25
            self.rodent_data.speed = self.rodent_data.speed * 1.25
        self.rodent_data.previous_hp = self.rodent_data.hp

    def fixed_update(self, game_time: pyasge.GameTime) -> None:
        """The fixed-update function moves the rodent at a constant speed"""
        # If there is a path made and they are alive
        if len(self.destination) > 0 and self.rodent_data.hp != 0:
            if abs(pyasge.Point2D.distance(self.sprite.midpoint, self.destination[0])) < 100 * 0.02:
                destination_temp = self.destination.pop(0)
                self.sprite.x = destination_temp.x - self.sprite.width/2
                self.sprite.y = destination_temp.y - self.sprite.height/2
                return
            if len(self.destination) > 1:
                # If the rodent is moving an unnecessary space, remove the first step
                if self.destination[0].x < self.sprite.midpoint.x < self.destination[1].x \
                        or self.destination[0].y < self.sprite.midpoint.y < self.destination[1].y or \
                        self.destination[0].x > self.sprite.midpoint.x > self.destination[1].x \
                        or self.destination[0].y > self.sprite.midpoint.y > self.destination[1].y:
                    self.destination.pop(0)
            self.direction.x = self.destination[0].x - self.sprite.midpoint.x
            self.direction.y = self.destination[0].y - self.sprite.midpoint.y
            # Make unit vector of direction
            length = self.direction.x * self.direction.x + self.direction.y * self.direction.y
            length = math.sqrt(length)
            self.direction.x = self.direction.x / length
            self.direction.y = self.direction.y / length
            # If they can't move then do nothing
            if self.rodent_data.healing or (self.rodent_data.stun_timer < self.rodent_data.stun_duration
                                            and not self.rodent_data.rodent_type == RodentType.FERRET):
                pass
            # But if they are slowed and not immune then move them with a slower speed
            elif self.rodent_data.slow_de_buff and not self.rodent_data.rodent_type == RodentType.FERRET:
                self.sprite.x += self.direction.x * self.rodent_data.speed * 40 * game_time.fixed_timestep
                self.sprite.y += self.direction.y * self.rodent_data.speed * 40 * game_time.fixed_timestep
            # Otherwise move at max speed
            else:
                self.sprite.x += self.direction.x * self.rodent_data.speed * 100 * game_time.fixed_timestep
                self.sprite.y += self.direction.y * self.rodent_data.speed * 100 * game_time.fixed_timestep

    def update(self, game_time: pyasge.GameTime):
        self.rodent_data.stun_timer += game_time.frame_time
        # Animation update
        self.rodent_data.anim_timer += game_time.frame_time
        if self.rodent_data.anim_timer >= self.rodent_data.anim_speed:
            if self.rodent_data.current_sprite_num == 0:
                self.sprite.loadTexture(self.textures_2[self.rodent_data.rodent_type])
                self.rodent_data.current_sprite_num = 1
                self.sprite.texture.setMagFilter(pyasge.MagFilter.NEAREST)
                self.sprite.width = 32
                self.sprite.height = 32
            else:
                self.sprite.loadTexture(self.textures[self.rodent_data.rodent_type])
                self.rodent_data.current_sprite_num = 0
                self.sprite.texture.setMagFilter(pyasge.MagFilter.NEAREST)
                self.sprite.width = 32
                self.sprite.height = 32
            self.rodent_data.anim_timer = 0
        # AI update
        self.behaviour_tree.update(game_time)
        # If HP changes for HEDGEHOG, set shoot to true
        if self.rodent_data.rodent_type == RodentType.HEDGEHOG:
            if self.rodent_data.hp != self.rodent_data.previous_hp:
                self.rodent_data.shoot_out = True

        elif self.rodent_data.rodent_type == RodentType.CHINCHILLA:
            # Update invisibility for CHINCHILLA
            self.rodent_data.invisible_timer += game_time.frame_time
            if self.rodent_data.invisible_timer >= self.rodent_data.time_between_invisible \
                    and self.rodent_data.hp != self.rodent_data.previous_hp:
                self.rodent_data.invisible = True
                self.rodent_data.invisible_timer = 0
                # Reset invisibility if hit after long enough time since last invisibility
            elif self.rodent_data.invisible_timer <= self.rodent_data.invisible_duration:
                self.rodent_data.invisible = True
            else:
                self.rodent_data.invisible = False

        elif self.rodent_data.rodent_type == RodentType.SQUIRREL:
            # Update healing for SQUIRREL
            self.rodent_data.healing_timer += game_time.frame_time
            if self.rodent_data.healing:
                if self.rodent_data.healing_timer >= self.rodent_data.time_between_heals:
                    self.rodent_data.hp += self.rodent_data.amount_per_heal
                    self.rodent_data.current_times_healed += 1
                    self.rodent_data.healing_timer = 0
                if self.rodent_data.current_times_healed >= self.rodent_data.number_of_heals:
                    self.rodent_data.healing = False
            elif self.rodent_data.healing_timer >= self.rodent_data.heal_cooldown\
                    and self.rodent_data.hp <= self.rodent_data.heal_hp_range:
                self.rodent_data.healing = True

        # Record hp to be used as prev hp
        self.rodent_data.previous_hp = self.rodent_data.hp

        # Flip to face move direction
        if self.direction.x < 0:
            self.sprite.flip_flags = pyasge.Sprite.FlipFlags.NORMAL
        elif self.direction.x > 0:
            self.sprite.flip_flags = pyasge.Sprite.FlipFlags.FLIP_X

        if self.rodent_data.fleeing != self.rodent_data.prev_fleeing:
            self.rodent_data.update_path = True

        if self.rodent_data.cat_in_range != self.rodent_data.prev_cat_in_range:
            self.rodent_data.update_path = True

        self.rodent_data.prev_fleeing = self.rodent_data.fleeing
        self.rodent_data.prev_cat_in_range = self.rodent_data.cat_in_range

    def render(self, renderer: pyasge.Renderer, game_time: pyasge.GameTime) -> None:
        renderer.render(self.sprite)
