import pyasge
from enum import IntEnum


class CatType(IntEnum):
    BLOCKER = 0,
    FURBALL = 1,
    SCRATCH = 2,
    RADIOACTIVE = 3,
    TIME = 4,
    BOOSTER = 5,
    RESOURCE = 6,
    STUN = 7


class CatData:

    def __init__(self, cat_type) -> None:

        # Statuses
        self.boost_buff = False
        self.shooting = False
        self.cat_type = cat_type

        # Stats Data
        self.boost_percent = 1.1
        self.stat_inc_per_level = 1.1
        self.max_hp = 10
        self.attack_range = 256
        self.yarn_per_resource = 2
        self.damage_per_hit = 2
        self.reload_time = 2

        # Recorded data
        self.hit_timer = 0
        self.hit_render = False
        self.hp = self.max_hp
        self.targeted_rodent = None
        self.upgrade_level = 1

        # Animation data
        self.anim_timer = 0
        self.anim_speed = 0.5
        self.current_sprite_num = 0     # 0 is first sprite, 1 is second
