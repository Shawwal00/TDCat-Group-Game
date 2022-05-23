import pyasge
from enum import IntEnum


class ProjType(IntEnum):
    NORMAL = 0,
    RADIOACTIVE = 1,
    STUN = 2


class Projectile:
    def __init__(self, target: pyasge.Sprite, spawn: pyasge.Point2D, damage: float, proj_type: ProjType):
        self.sprite = pyasge.Sprite()
        self.textures = ["/data/textures/projectile.png", "/data/textures/projectile_radioactive.png"
                         , "/data/textures/projectile_stun.png"]
        self.sprite.loadTexture(self.textures[proj_type])
        self.sprite.texture.setMagFilter(pyasge.MagFilter.NEAREST)
        self.sprite.width = 32
        self.sprite.height = 32
        self.sprite.x = spawn.x - 32
        self.sprite.y = spawn.y - 32
        self.sprite.z_order = 50
        self.speed = 512
        self.proj_type = proj_type
        self.target = target
        self.damage = damage
        self.delete_x = False
        self.delete_y = False

    def fixed_update(self, game_time: pyasge.GameTime) -> None:
        # Create direction vector between current pos and target pos
        vec_dif = pyasge.Point2D()
        vec_dif.x = self.target.sprite.midpoint.x - self.sprite.midpoint.x
        vec_dif.y = self.target.sprite.midpoint.y - self.sprite.midpoint.y
        dist_mag = pyasge.Point2D.distance(self.target.sprite.midpoint, self.sprite.midpoint)
        # If the distance is 0 exit and state it needs to be deleted
        if dist_mag == 0:
            self.delete_x = True
            self.delete_y = True
            return None
        vec_dif.x = vec_dif.x / pyasge.Point2D.distance(self.target.sprite.midpoint, self.sprite.midpoint)
        vec_dif.y = vec_dif.y / pyasge.Point2D.distance(self.target.sprite.midpoint, self.sprite.midpoint)
        # Multiply by speed and delta time to create change in position vector
        move_x = vec_dif.x * self.speed * game_time.fixed_timestep
        move_y = vec_dif.y * self.speed * game_time.fixed_timestep

        # If target will move past the target point on both x and y, then delete it
        if abs(self.target.sprite.x - self.sprite.x) < move_x:
            self.sprite.x = self.target.sprite.x
            self.delete_x = True

        if abs(self.target.sprite.y - self.sprite.y) < move_y:
            self.sprite.y = self.target.sprite.y
            self.delete_y = True

        self.sprite.x += move_x
        self.sprite.y += move_y

    def update(self, game_time: pyasge.GameTime):
        # If target is 1 pixel away on both x and y, delete it
        if abs(self.target.sprite.x - self.sprite.x) < 1:
            self.sprite.x = self.target.sprite.x
            self.delete_x = True

        if abs(self.target.sprite.y - self.sprite.y) < 1:
            self.sprite.y = self.target.sprite.y
            self.delete_y = True

    def render(self, renderer: pyasge.Renderer, game_time: pyasge.GameTime) -> None:
        renderer.render(self.sprite)


class RodentProjectile:
    def __init__(self, target: pyasge.Point2D, spawn: pyasge.Point2D, damage: float):
        # Identical to normal projectile other than the target is a position and not a sprite
        self.sprite = pyasge.Sprite()
        self.textures = ["/data/textures/projectile_small_wood.png"]
        self.sprite.loadTexture(self.textures[0])
        self.sprite.texture.setMagFilter(pyasge.MagFilter.NEAREST)
        self.sprite.width = 16
        self.sprite.height = 16
        self.sprite.x = spawn.x - 8
        self.sprite.y = spawn.y - 8
        self.sprite.z_order = 50
        self.speed = 64
        self.target = target
        self.damage = damage
        self.delete_x = False
        self.delete_y = False

    def fixed_update(self, game_time: pyasge.GameTime) -> None:
        # Create direction vector between current pos and target pos
        vec_dif = pyasge.Point2D()
        vec_dif.x = self.target.x - self.sprite.midpoint.x
        vec_dif.y = self.target.y - self.sprite.midpoint.y
        dist_mag = pyasge.Point2D.distance(self.target, self.sprite.midpoint)
        # If the distance is 0 exit and state it needs to be deleted
        if dist_mag == 0:
            self.delete_x = True
            self.delete_y = True
            return None
        vec_dif.x = vec_dif.x / pyasge.Point2D.distance(self.target, self.sprite.midpoint)
        vec_dif.y = vec_dif.y / pyasge.Point2D.distance(self.target, self.sprite.midpoint)
        # Multiply by speed and delta time to create change in position vector
        move_x = vec_dif.x * self.speed * game_time.fixed_timestep
        move_y = vec_dif.y * self.speed * game_time.fixed_timestep

        if abs(self.target.x - self.sprite.x) < move_x:
            self.sprite.x = self.sprite.x
            self.delete_x = True

        if abs(self.target.y - self.sprite.y) < move_y:
            self.sprite.y = self.sprite.y
            self.delete_y = True

        self.sprite.x += move_x
        self.sprite.y += move_y

    def update(self, game_time: pyasge.GameTime):
        # Slightly scale projectile down over time
        self.sprite.scale = self.sprite.scale - 0.001

        # If target will move past the target point on both x and y, then delete it
        if abs(self.target.x - self.sprite.midpoint.x) < 16:
            self.sprite.x = self.sprite.x
            self.delete_x = True

        if abs(self.target.y - self.sprite.midpoint.y) < 16:
            self.sprite.y = self.sprite.y
            self.delete_y = True

    def render(self, renderer: pyasge.Renderer, game_time: pyasge.GameTime) -> None:
        renderer.render(self.sprite)
