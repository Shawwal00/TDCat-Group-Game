import pyasge
from enum import IntEnum


class RodentType(IntEnum):
    HAMSTER = 0,
    GUINEA = 1,
    HEDGEHOG = 2,
    MICE = 3,
    SQUIRREL = 4,
    RABBIT = 5,
    CHINCHILLA = 6,
    CHIPMUNK = 7,
    FERRET = 8


class RodentData:

    def __init__(self, rodent_type) -> None:
        # SQUIRREL data
        self.healing = False
        self.heal_cooldown = 10
        self.healing_timer = 10
        self.time_between_heals = 1
        self.amount_per_heal = 1
        self.current_times_healed = 0
        self.number_of_heals = 4
        self.heal_hp_range = 5

        # CHIPMUNK data
        self.is_child = False

        # CHINCHILLA data
        self.time_between_invisible = 20
        self.invisible_duration = 8
        self.invisible_timer = 20
        self.invisible = False

        # HEDGEHOG data
        self.shoot_out = False

        # Statuses
        self.slow_de_buff = False
        self.attacking = False
        self.targeted_cat = None
        self.rodent_type = rodent_type
        self.on_spawn_tile = False
        self.on_home_tile = False

        # Stats data
        self.can_hidden_path = False
        self.low_hp_range = 2
        self.attack_range = 32
        self.sight_range = 128
        self.speed = 1
        self.damage_per_hit = 1
        self.time_between_hits = 1

        # Recorded data
        self.cat_in_range = False
        self.prev_cat_in_range = False
        self.fleeing = False
        self.prev_fleeing = False
        self.update_path = True
        self.previous_hp = 10
        self.hp = 10
        self.hit_render = False
        self.hit_timer = 0
        self.heal_timer = 0
        self.invisible_render_timer = 0
        self.stun_timer = 1.5
        self.stun_duration = 1.5

        # Animation data
        self.anim_timer = 0
        self.anim_speed = 0.5
        self.current_sprite_num = 0     # 0 is first sprite, 1 is second
