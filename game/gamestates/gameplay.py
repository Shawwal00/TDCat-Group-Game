import math
import random

import numpy as np
import pyasge
from game.gamedata import GameData
from game.gamestates.gamestate import GameState
from game.gamestates.gamestate import GameStateID
from game.gameobjects.cat import Cat
from game.catdata import CatType
from game.rodentdata import RodentType
from game.gameobjects.rodent import Rodent
from game.gameobjects.projectile import Projectile, RodentProjectile
from game.gameobjects.shop import Shop
from game.gameobjects.cursorsquare import Square
from game.gameobjects.projectile import ProjType
from game.wavedata import WaveData
from game.gamedata import Difficulty
from game.gameobjects.yarn_popup import YarnPopUp
from pyfmodex.flags import MODE


class GamePlay(GameState):
    """ The game play state is the core of the game itself.

    The role of this class is to process the game logic, update
    the players positioning and render the resultant game-world.
    The logic for deciding on victory or loss should be handled by
    this class and its update function should return GAME_OVER or
    GAME_WON when the end game state is reached.
    """

    def __init__(self, data: GameData) -> None:
        """ Creates the game world

        Use the constructor to initialise the game world in a "clean"
        state ready for the player. This includes resetting of player's
        health and the enemy positions.

        Args:
            data (GameData): The game's shared data
        """
        super().__init__(data)

        # Generate all UI variables
        self.id = GameStateID.GAMEPLAY
        self.data.renderer.setClearColour(pyasge.COLOURS.CORAL)
        self.yarn_ui = None
        self.yarn_ui_num = None
        self.wave_num = None

        self.health_ui_1 = self.data.renderer.loadTexture("./data/textures/heart_pixel.png")
        self.health_ui_2 = self.data.renderer.loadTexture("./data/textures/heart_pixel.png")
        self.health_ui_3 = self.data.renderer.loadTexture("./data/textures/heart_pixel.png")
        self.health_ui_4 = self.data.renderer.loadTexture("./data/textures/heart_pixel.png")
        self.health_ui_5 = self.data.renderer.loadTexture("./data/textures/heart_pixel.png")
        self.health_ui = [self.health_ui_5, self.health_ui_4, self.health_ui_3, self.health_ui_2, self.health_ui_1]
        self.init_ui()

        # sets up the camera and points it at the player
        map_mid = [
            self.data.game_map.width * self.data.game_map.tile_size[0] * 0.5,
            self.data.game_map.height * self.data.game_map.tile_size[1] * 0.5
        ]

        self.camera = pyasge.Camera(map_mid, self.data.game_res[0], self.data.game_res[1])
        self.camera.zoom = 1

        self.shop = None
        self.light_time = 1

        self.buy_menu = False
        self.cats = []
        self.rodents = []
        self.yarn_popups = []
        self.projectiles = []
        self.rodent_projectiles = []
        self.current_rodent = -1
        self.wave_data = WaveData(data.difficulty)

        self.cursor_tile = Square((15, 7), self.data.game_map.world((15, 7)))
        self.tile = (1, 1)
        self.shop_place = (1, 1)

        self.to_pause = False
        self.in_game = True
        self.to_win = False
        self.to_lose = False

        # The below sets up thee various sfx sounds that we use within our game
        self.sounds = {
            "win": self.data.audio_system.create_sound("./data/audio/small-applause-6695.ogg",
                                                       mode=MODE.LOOP_OFF),
            "die": self.data.audio_system.create_sound("./data/audio/goblin-death-6729.ogg",
                                                       mode=MODE.LOOP_OFF),
            "wave": self.data.audio_system.create_sound("./data/audio/kick-bass-808-drums-loop-6-11282.ogg",
                                                        mode=MODE.LOOP_OFF),
            "click": self.data.audio_system.create_sound("./data/audio/lclick-13694.ogg",
                                                         mode=MODE.LOOP_OFF),
            "lose": self.data.audio_system.create_sound("./data/audio/negative_beeps-6008 (1).ogg",
                                                        mode=MODE.LOOP_OFF)
        }

    def init_ui(self):
        """Initialises the UI elements"""
        self.yarn_ui = self.data.renderer.loadTexture("./data/textures/UI_TopL1.png")
        self.yarn_ui.setMagFilter(pyasge.MagFilter.NEAREST)
        self.yarn_ui_num = pyasge.Text(self.data.fonts["MenuFont"], "0", 452, 50)
        self.yarn_ui_num.colour = pyasge.COLOURS.SKYBLUE
        self.yarn_ui_num.z_order = 100
        self.yarn_ui_num.scale = 0.5
        self.wave_num = pyasge.Text(self.data.fonts["MenuFont"], "0", 690, 50)
        self.wave_num.colour = pyasge.COLOURS.SKYBLUE
        self.wave_num.z_order = 100
        self.wave_num.scale = 0.5

    def buy(self, place: pyasge.Point2D):
        self.data.audio_system.play_sound(self.sounds["click"])
        if not self.buy_menu:
            # if the tile is valid for the placing of a cat:
            placement = self.data.game_map.tile(place)
            terrain = self.data.game_map.costs[placement[1]][placement[0]]
            # make a new shop menu
            self.shop = Shop(self.data, self.data.game_map.world(placement), terrain, self.data.yarn)
            self.shop_place = placement
            # If any cat is already on this tile, don't progress further
            for cat in self.cats:
                tile = self.data.game_map.tile(cat.sprite.midpoint)
                if tile == placement:
                    return None
            self.buy_menu = True
            pass
        elif self.buy_menu:
            # if a shop menu has been opened, use it's clicking subroutine
            buy_cat = self.shop.menu_click(place.x, place.y, self.data.yarn)
            if buy_cat >= 0:
                # if the player clicked the tick, place a cat
                cat_location = pyasge.Point2D(self.data.game_map.world(self.shop_place).x - 64,
                                              self.data.game_map.world(self.shop_place).y - 64)
                if self.data.yarn >= self.data.cat_costs[buy_cat]:
                    self.data.yarn -= self.data.cat_costs[buy_cat]
                    if buy_cat == CatType.BOOSTER:
                        self.cats.append(Cat(self.data, cat_location, buy_cat, self.cats))
                    else:
                        self.cats.append(Cat(self.data, cat_location, buy_cat, self.rodents))

                    if buy_cat == CatType.BLOCKER:
                        for rodent in self.rodents:
                            rodent.rodent_data.update_path = True
                    self.buy_menu = False  # if a cat has been bought, close the shop menu

    def click_handler(self, event: pyasge.ClickEvent) -> None:
        if event.button is pyasge.MOUSE.MOUSE_BTN2 and \
                event.action is pyasge.MOUSE.BUTTON_PRESSED:
            self.buy_menu = False
            pass   # could use RMB to exit shop?

        if event.button is pyasge.MOUSE.MOUSE_BTN1 and \
                event.action is pyasge.MOUSE.BUTTON_PRESSED:
            self.buy(self.data.cursor)
            pass

    def move_handler(self, event: pyasge.MoveEvent) -> None:
        """ Listens for mouse movement events from the game engine """
        pass

    def key_handler(self, event: pyasge.KeyEvent) -> None:
        """ Listens for key events from the game engine """
        if event.action == pyasge.KEYS.KEY_PRESSED:
            if event.key == pyasge.KEYS.KEY_ESCAPE:
                self.to_pause = True

            # Remove before final release

            # if event.key == pyasge.KEYS.KEY_9:
            #     self.to_win = True
            #
            # if event.key == pyasge.KEYS.KEY_0:
            #     self.to_lose = True

    def fixed_update(self, game_time: pyasge.GameTime) -> None:
        """ Simulates deterministic time steps for the game objects"""
        self.checkProjectiles()
        for projectile in self.projectiles:
            projectile.fixed_update(game_time)
        for projectile in self.rodent_projectiles:
            projectile.fixed_update(game_time)
        for rodent in self.rodents:
            rodent.fixed_update(game_time)
        for popup in self.yarn_popups:
            popup.fixed_update(game_time)

    def update(self, game_time: pyasge.GameTime) -> GameStateID:
        """ Updates the game world

        Processes the game world logic. You should handle collisions,
        actions and AI actions here. At present cannonballs are
        updated and so are player collisions with the islands, but
        consider how the ships will react to each other

        Args:
            game_time (pyasge.GameTime): The time between ticks.
        """
        self.update_inputs()
        self.update_waves(game_time)
        self.tile = self.data.game_map.tile(self.data.cursor)
        if self.buy_menu:
            self.shop.Update(self.data.yarn)
        for cat in self.cats:
            # Updates each cat and removes any that are dead
            cat.update(game_time)
            # If cat has no hp
            if cat.cat_data.hp <= 0:
                # Update tile map cost if cat was a blocker
                if cat.cat_data.cat_type == CatType.BLOCKER:
                    tile = self.data.game_map.tile(pyasge.Point2D(cat.sprite.x + 32, cat.sprite.y + 32))
                    self.data.game_map.costs[tile[1]][tile[0]] -= 20
                    # And update all rodent paths
                    for rodent in self.rodents:
                        rodent.rodent_data.update_path = True
                self.cats.remove(cat)
            elif cat.cat_data.shooting:
                # If the cat wants to shoot, generate a projectile and set the target to the closest rodent
                if cat.cat_data.cat_type == CatType.RADIOACTIVE:
                    self.projectiles.append(
                        Projectile(cat.cat_data.targeted_rodent, cat.sprite.midpoint,
                                   cat.cat_data.damage_per_hit *
                                   pow(cat.cat_data.stat_inc_per_level, cat.cat_data.upgrade_level-1),
                                   ProjType.RADIOACTIVE))
                elif cat.cat_data.cat_type == CatType.STUN:
                    self.projectiles.append(
                        Projectile(cat.cat_data.targeted_rodent, cat.sprite.midpoint,
                                   cat.cat_data.damage_per_hit *
                                   pow(cat.cat_data.stat_inc_per_level, cat.cat_data.upgrade_level-1), ProjType.STUN))
                else:
                    self.projectiles.append(
                        Projectile(cat.cat_data.targeted_rodent, cat.sprite.midpoint,
                                   cat.cat_data.damage_per_hit *
                                   pow(cat.cat_data.stat_inc_per_level, cat.cat_data.upgrade_level-1), ProjType.NORMAL))
                cat.cat_data.shooting = False
        for rodent in self.rodents:
            # Updates each rodent and removes any that are dead
            rodent.update(game_time)
            # If rodent has no hp
            if rodent.rodent_data.hp <= 0:
                channel = self.data.audio_system.play_sound(self.sounds["die"])
                channel.volume = 0.3
                if rodent.rodent_data.rodent_type == RodentType.HEDGEHOG:
                    # Create 16 projectiles upon death if it is a HEDGEHOG
                    for i in range(16):
                        direction = np.array([128, 0])
                        rot_matrix = np.array([[math.cos(i * math.pi * 0.125), -math.sin(i * math.pi * 0.125)],
                                              [math.sin(i * math.pi * 0.125), math.cos(i * math.pi * 0.125)]])
                        new_dir = rot_matrix.dot(direction)
                        co_ords = pyasge.Point2D(new_dir[0] + rodent.sprite.midpoint.x,
                                                 new_dir[1] + rodent.sprite.midpoint.y)
                        self.rodent_projectiles.append(RodentProjectile(co_ords, rodent.sprite.midpoint, 1))
                elif rodent.rodent_data.rodent_type == RodentType.CHIPMUNK and not rodent.rodent_data.is_child:
                    # Create 3 CHIPMUNKS upon death, and set child to true and hp lower
                    child1 = Rodent(self.data, pyasge.Point2D(rodent.sprite.x + 20, rodent.sprite.y),
                                    RodentType.CHIPMUNK, self.cats)
                    self.rodents.append(child1)
                    child1.rodent_data.is_child = True
                    child1.rodent_data.hp = 4
                    child1.rodent_data.low_hp_range = 1

                    child2 = Rodent(self.data, pyasge.Point2D(rodent.sprite.x, rodent.sprite.y + 10),
                                    RodentType.CHIPMUNK, self.cats)
                    self.rodents.append(child2)
                    child2.rodent_data.is_child = True
                    child2.rodent_data.hp = 4
                    child2.rodent_data.low_hp_range = 1

                    child3 = Rodent(self.data, pyasge.Point2D(rodent.sprite.x - 20, rodent.sprite.y),
                                    RodentType.CHIPMUNK, self.cats)
                    self.rodents.append(child3)
                    child3.rodent_data.is_child = True
                    child3.rodent_data.hp = 4
                    child3.rodent_data.low_hp_range = 1
                # Create yarn popup
                self.yarn_popups.append(YarnPopUp(10, rodent.sprite.midpoint))
                self.rodents.remove(rodent)
                self.data.yarn += 10
            else:
                # Update invis timer
                if rodent.rodent_data.invisible_render_timer > 2.1:
                    rodent.rodent_data.invisible_render_timer = 0.1
                    rodent.rodent_data.invisible = False
                    rodent.rodent_data.hit_timer = 0.0
                    rodent.rodent_data.hit_render = False
                else:
                    rodent.rodent_data.invisible_render_timer += game_time.frame_time

                # Update heal timer
                if rodent.rodent_data.heal_timer > 0.7:
                    rodent.rodent_data.heal_timer = 0.0
                    rodent.rodent_data.heal_render = False
                else:
                    rodent.rodent_data.hit_timer += game_time.frame_time

                # Update hit timer
                if rodent.rodent_data.hit_timer > 0.7:
                    rodent.rodent_data.hit_timer = 0.0
                    rodent.rodent_data.hit_render = False
                else:
                    rodent.rodent_data.hit_timer += game_time.frame_time

                if rodent.rodent_data.shoot_out:
                    # If rodent wants to shoot, generate 8 projectiles at 45 degree angles of each other
                    for i in range(8):
                        # Create 2x1 matrix for initial direction
                        direction = np.array([128, 0])
                        rot_matrix = np.array([[math.cos(i * math.pi * 0.25), -math.sin(i * math.pi * 0.25)],
                                              [math.sin(i * math.pi * 0.25), math.cos(i * math.pi * 0.25)]])
                        # Multiply by 45-degree rotation matrix
                        new_dir = rot_matrix.dot(direction)
                        # Add to center point to create target point
                        co_ords = pyasge.Point2D(new_dir[0] + rodent.sprite.midpoint.x,
                                                 new_dir[1] + rodent.sprite.midpoint.y)
                        self.rodent_projectiles.append(RodentProjectile(co_ords, rodent.sprite.midpoint, 1))
                    rodent.rodent_data.shoot_out = False
                # De spawn rodent if on spawn tile
                elif rodent.rodent_data.on_spawn_tile:
                    self.rodents.remove(rodent)
                # De spawn rodent and lower hp if on home tile
                elif rodent.rodent_data.on_home_tile:
                    self.rodents.remove(rodent)
                    self.data.hp -= 1

                # If rodent wants to attack a cat
                if rodent.rodent_data.attacking:
                    rodent.rodent_data.targeted_cat.cat_data.hp -= rodent.rodent_data.damage_per_hit
                    rodent.rodent_data.attacking = False
                    rodent.rodent_data.targeted_cat.cat_data.hit_render = True
                    rodent.rodent_data.targeted_cat.cat_data.hit_timer = 0

        # Remove projectile if both delete axis are true
        for projectile in self.projectiles:
            projectile.update(game_time)
            if projectile.delete_x and projectile.delete_y:
                self.projectiles.remove(projectile)

        # Remove rodent projectile if both delete axis are true
        for projectile in self.rodent_projectiles:
            projectile.update(game_time)
            if projectile.delete_x and projectile.delete_y:
                self.rodent_projectiles.remove(projectile)

        # Remove popup if duration has ended
        for popup in self.yarn_popups:
            if popup.remove:
                self.yarn_popups.remove(popup)

        if self.data.hp <= 0:
            self.data.audio_system.play_sound(self.sounds["lose"])
            return GameStateID.GAME_OVER
        if self.to_pause:
            return GameStateID.PAUSE
        if self.to_win:
            self.data.audio_system.play_sound(self.sounds["win"])
            return GameStateID.WINNER_WINNER
        if self.to_lose:
            self.data.audio_system.play_sound(self.sounds["lose"])
            return GameStateID.GAME_OVER

        return GameStateID.GAMEPLAY

    def update_inputs(self):
        """ This is purely example code to show how gamepad events
        can be tracked """
        if self.data.gamepad.connected:
            x_shift = self.data.gamepad.AXIS_LEFT_X
            y_shift = self.data.gamepad.AXIS_LEFT_Y
            if (x_shift >= 0.5 or x_shift <= -0.5 or y_shift >= 0.5 or y_shift <= 0.5) and not self.buy_menu:
                if self.data.gamepad.AXIS_LEFT_X >= 0.5 and not self.data.prev_gamepad.AXIS_LEFT_X >= 0.5:
                    self.cursor_tile.tilex += 1
                elif self.data.gamepad.AXIS_LEFT_X <= -0.5 and not self.data.prev_gamepad.AXIS_LEFT_X <= -0.5:
                    self.cursor_tile.tilex -= 1
                elif self.data.gamepad.AXIS_LEFT_Y >= 0.5 and not self.data.prev_gamepad.AXIS_LEFT_Y >= 0.5:
                    self.cursor_tile.tiley += 1
                if self.data.gamepad.AXIS_LEFT_Y <= -0.5 and not self.data.prev_gamepad.AXIS_LEFT_Y <= -0.5:
                    self.cursor_tile.tiley -= 1
                cursor_pos = self.data.game_map.world((self.cursor_tile.tilex, self.cursor_tile.tiley))
                self.cursor_tile.move(cursor_pos)
            elif (x_shift >= 0.5 or x_shift <= -0.5 or y_shift >= 0.5 or y_shift <= 0.5) and self.buy_menu:
                if (self.data.gamepad.AXIS_LEFT_X >= 0.5 and not self.data.prev_gamepad.AXIS_LEFT_X >= 0.5) or \
                        (self.data.gamepad.AXIS_LEFT_X <= -0.5 and not self.data.prev_gamepad.AXIS_LEFT_X <= -0.5):
                    self.buy(self.data.cursor)
            if self.data.gamepad.A and not self.data.prev_gamepad.A:
                # A button is pressed
                # if the tile is valid for the placing of a cat:
                self.buy(self.data.game_map.world((self.cursor_tile.tilex, self.cursor_tile.tiley)))
                pass
            if self.data.gamepad.B:
                self.buy_menu = False
            if self.data.gamepad.START:
                self.to_pause = True

    def update_waves(self, game_time):
        # Update wave timer
        self.wave_data.timer += game_time.frame_time
        self.data.current_wave_num = self.wave_data.wave_number
        if self.wave_data.spawning:
            # If wave is spawning rodents, check if exceeded spawn amount and stop if true
            if self.wave_data.rodents_spawned >= self.wave_data.rodents_per_wave[self.wave_data.wave_number - 1]:
                self.wave_data.spawning = False
            # Otherwise, spawn if timer reaches time between rodents
            elif self.wave_data.timer >= self.wave_data.time_between_rodents[self.wave_data.wave_number - 1]:
                self.spawn_rodent()
                self.wave_data.timer = 0
                self.wave_data.rodents_spawned += 1
        # If there are no rodents and they are not being spawned, start a new wave
        elif len(self.rodents) == 0:
            if self.wave_data.timer >= self.wave_data.time_between_waves:
                self.wave_data.wave_number += 1
                if self.wave_data.wave_number <= self.wave_data.max_waves:
                    self.data.audio_system.play_sound(self.sounds["wave"])
                    self.wave_data.spawning = True
                    self.wave_data.rodents_spawned = 0
                # If there are no more waves left, player wins
                else:
                    self.to_win = True

    def render(self, game_time: pyasge.GameTime) -> None:
        """ Renders the game world and the UI """
        self.light_time = self.light_time + game_time.fixed_timestep
        self.data.renderer.setViewport(pyasge.Viewport(0, 0, self.data.game_res[0], self.data.game_res[1]))
        self.data.renderer.setProjectionMatrix(self.camera.view)

        self.data.shaders["main"].uniform("rgb").set([1, 1, 1])
        self.data.shaders["main"].uniform("alpha").set(float(1))
        self.data.renderer.shader = self.data.shaders["main"]

        # setting up the grass shader
        self.data.shaders["grass_test"].uniform("rgb").set([1, 1, 1])
        self.data.shaders["grass_test"].uniform("time").set(self.light_time)
        self.data.renderer.shader = self.data.shaders["grass_test"]
        self.data.game_map.render(self.data.renderer, game_time)

        # Render all projectiles normally
        self.data.renderer.shader = self.data.shaders["main"]
        for projectile in self.projectiles:
            projectile.render(self.data.renderer, game_time)
        for projectile in self.rodent_projectiles:
            projectile.render(self.data.renderer, game_time)
        self.render_cats(game_time)
        self.render_rodents(game_time)

        for popup in self.yarn_popups:
            self.data.shaders["invisibility"].uniform("rgb").set([1, 1, 1])
            self.data.shaders["invisibility"].uniform("time").set(float(popup.timer))
            self.data.renderer.shader = self.data.shaders["invisibility"]
            popup.render(self.data.renderer, game_time)

        self.data.renderer.shader = self.data.shaders["main"]
        if self.buy_menu:
            self.shop.render(self.data.renderer, game_time)
        if self.data.gamepad.connected:
            self.cursor_tile.render(self.data.renderer, game_time)
        self.render_ui()

    def render_rodents(self, game_time):
        for rodent in self.rodents:
            # The below activates the healing shader for the rodents
            if rodent.rodent_data.stun_timer < rodent.rodent_data.stun_duration:
                self.data.shaders["flash_stun"].uniform("rgb").set([0.6, 0.6, 1])
                self.data.shaders["flash_stun"].uniform("time").set(float(rodent.rodent_data.heal_timer))
                self.data.renderer.shader = self.data.shaders["flash_stun"]
                rodent.render(self.data.renderer, game_time)
            elif rodent.rodent_data.healing:
                self.data.shaders["flash_green"].uniform("rgb").set([0, 1, 0])
                self.data.shaders["flash_green"].uniform("time").set(float(rodent.rodent_data.heal_timer))
                self.data.renderer.shader = self.data.shaders["flash_green"]
                rodent.render(self.data.renderer, game_time)
                # The below activates the invisibility shader for the chinchilla
            elif rodent.rodent_data.invisible:
                self.data.shaders["invisibility"].uniform("rgb").set([1, 1, 1])
                self.data.shaders["invisibility"].uniform("time").set(float(rodent.rodent_data.invisible_render_timer))
                self.data.renderer.shader = self.data.shaders["invisibility"]
                rodent.render(self.data.renderer, game_time)
                # The below activates the hit shader for the rodents
            elif rodent.rodent_data.hit_render:
                self.data.shaders["flash"].uniform("rgb").set([1, 0, 0])
                self.data.shaders["flash"].uniform("time").set(float(rodent.rodent_data.hit_timer))
                self.data.renderer.shader = self.data.shaders["flash"]
                rodent.render(self.data.renderer, game_time)
            else:
                self.data.renderer.shader = self.data.shaders["main"]
                rodent.render(self.data.renderer, game_time)

    def render_cats(self, game_time):
        for cat in self.cats:
            # The below activates the hit shader for the cats
            if cat.cat_data.hit_render:
                self.data.shaders["flash"].uniform("rgb").set([1, 0, 0])
                self.data.shaders["flash"].uniform("time").set(float(cat.cat_data.hit_timer))
                self.data.renderer.shader = self.data.shaders["flash"]
                cat.render(self.data.renderer, game_time)
                if cat.cat_data.hit_timer > 0.7:
                    cat.cat_data.hit_timer = 0.0
                    cat.cat_data.hit_render = False
                else:
                    cat.cat_data.hit_timer += game_time.frame_time
            else:
                self.data.renderer.shader = self.data.shaders["main"]
                cat.render(self.data.renderer, game_time)

    def render_ui(self) -> None:
        """ Render the UI elements and map to the whole window """
        # set a new view that covers the width and height of game
        self.data.renderer.shader = self.data.shaders["main"]
        camera_view = pyasge.CameraView(self.data.renderer.resolution_info.view)
        vp = self.data.renderer.resolution_info.viewport
        self.data.renderer.setProjectionMatrix(0, 0, vp.w, vp.h)

        self.data.renderer.render(self.yarn_ui, 0, 0, 788, 80, 90)
        self.yarn_ui_num.string = f'{self.data.yarn}'
        self.data.renderer.render(self.yarn_ui_num)
        self.wave_num.string = f'{self.wave_data.wave_number}'
        self.data.renderer.render(self.wave_num)

        for i in range(self.data.max_hp):
            if self.data.hp > i:
                self.health_ui[i] = self.data.renderer.loadTexture("./data/textures/heart_pixel.png")
            else:
                self.health_ui[i] = self.data.renderer.loadTexture("./data/textures/heart_empty_pixel.png")
            self.health_ui[i].setMagFilter(pyasge.MagFilter.NEAREST)
            self.data.renderer.render(self.health_ui[i], 8 + (i*74), 8, 64, 64, 100)

        # this restores the original camera view
        self.data.renderer.setProjectionMatrix(camera_view)

    def to_world(self, pos: pyasge.Point2D) -> pyasge.Point2D:
        """
        Converts from screen position to world position
        :param pos: The position on the current game window camera
        :return: Its actual/absolute position in the game world
        """
        view = self.camera.view
        x = (view.max_x - view.min_x) / self.data.game_res[0] * pos.x
        y = (view.max_y - view.min_y) / self.data.game_res[1] * pos.y
        x = view.min_x + x
        y = view.min_y + y

        return pyasge.Point2D(x, y)

    def collision_detection(self, sp1: pyasge.Sprite, sp2: pyasge.Sprite):
        if sp2.x - sp1.width < sp1.x < sp2.x + sp2.width:
            if sp2.y - sp1.height < sp1.y < sp2.y + sp2.height:
                return True
        return False

    def checkProjectiles(self):
        # Checks if any projectiles are colliding with any target sprites and damages the target if hit
        for projectile in self.projectiles:
            for rodent in self.rodents:
                if self.projectiles.count(projectile) != 0:
                    if self.collision_detection(projectile.sprite, rodent.sprite):
                        if not rodent.rodent_data.invisible:
                            self.projectiles.remove(projectile)
                            if projectile.proj_type == ProjType.STUN:
                                rodent.rodent_data.stun_timer = 0
                            else:
                                rodent.rodent_data.hp -= projectile.damage
                                rodent.rodent_data.hit_render = True  # This will activate the shader for rodents
                                rodent.rodent_data.hit_timer = 0
                    
        for rodent_projectile in self.rodent_projectiles:
            for cat in self.cats:
                if pyasge.Point2D.distance(rodent_projectile.sprite.midpoint, cat.sprite.midpoint) <= 48:
                    if self.rodent_projectiles.count(rodent_projectile) != 0:
                        cat.cat_data.hit_render = True  # This will activate the shader for cats
                        cat.cat_data.hit_timer = 0
                        self.rodent_projectiles.remove(rodent_projectile)
                        cat.cat_data.hp -= rodent_projectile.damage

    def spawn_rodent(self):
        rands = random.sample(self.data.game_map.spawn_points, 1)
        rand_int = random.randint(0, 8)
        x, y = rands.pop()
        self.rodents.append(Rodent(self.data, pyasge.Point2D(x, y), rand_int, self.cats))
