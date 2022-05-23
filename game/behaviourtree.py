import random
import pyasge
from game.pathfinding import resolve
from game.catdata import CatType
from enum import IntEnum


class NodeType(IntEnum):
    SELECTOR = 1
    SEQUENCE = 2
    DECORATOR = 3
    LEAF = 4
    ROOT = 5


class BehaviourTreeRodent:
    def __init__(self, data, rodent, cats):
        # Last branch with the path to door
        self.branch4 = SequenceNode(
            [DecoratorNode(OnDoorTile(data, rodent), data), GoToDoor(data, rodent)], data)
        # Branch if cat is in agro range
        self.branch3 = SequenceNode(
            [InRangeRodent(cats, rodent, rodent.rodent_data.sight_range),
             GoToCat(data, rodent, cats)], data)
        # Branch if cat is in attack range
        self.branch2 = SequenceNode(
            [InRangeRodent(cats, rodent, rodent.rodent_data.attack_range),
             GoToCat(data, rodent, cats), AttackCat(cats, rodent, rodent.rodent_data)], data)
        # Branch if rodent is low and needs to go to spawn
        self.branch1 = SequenceNode(
            [LowHP(rodent.rodent_data, rodent.rodent_data.low_hp_range), DecoratorNode(OnSpawnTile(data, rodent), data),
             GoToSpawn(data, rodent)], data)

        self.base_selector = SelectorNode(
            [self.branch1, self.branch2, self.branch3,
             self.branch4, GoToCat(data, rodent, cats)], data)

        self.root = RootNode(self.base_selector)

    def update(self, game_time: pyasge.GameTime):
        self.root.update(game_time)


class BehaviourTreeCat:
    def __init__(self, data, cat, rodents, cat_data):
        # If RODENTS are in CAT range
        self.range_node = InRangeCat(rodents, cat, cat_data)
        # Shoot projectile at closest RODENT
        self.shoot_node = ShootProjectile(rodents, cat, cat_data)

        self.branch1 = SequenceNode([self.range_node, self.shoot_node], data)
        self.base_selector = SelectorNode([self.branch1], data)
        self.root = RootNode(self.base_selector)

    def update(self, game_time: pyasge.GameTime):
        self.root.update(game_time)


class BehaviourTreeResourceCat:
    def __init__(self, data, cat):
        # Generate yarn on a timer
        self.generate_node = GenerateYarn(data, cat)

        self.branch1 = SequenceNode([self.generate_node], data)
        self.base_selector = SelectorNode([self.branch1], data)
        self.root = RootNode(self.base_selector)

    def update(self, game_time: pyasge.GameTime):
        self.root.update(game_time)


class BehaviourTreeSlowCat:
    def __init__(self, data, cat, rodents, cat_data):
        # Slow RODENTS in range
        self.slow_node = SlowRodent(rodents, cat, cat_data)

        self.branch1 = SequenceNode([self.slow_node], data)
        self.base_selector = SelectorNode([self.branch1], data)
        self.root = RootNode(self.base_selector)

    def update(self, game_time: pyasge.GameTime):
        self.root.update(game_time)


class BehaviourTreeBoostCat:
    def __init__(self, data, cat, cats, cat_data):
        # Boost CATS in range
        self.boost_node = BoostCat(cats, cat, cat_data)

        self.branch1 = SequenceNode([self.boost_node], data)
        self.base_selector = SelectorNode([self.branch1], data)
        self.root = RootNode(self.base_selector)

    def update(self, game_time: pyasge.GameTime):
        self.root.update(game_time)


class RootNode:
    def __init__(self, child):
        # Root node, returns what is child returns
        self.type = NodeType.ROOT
        self.child = child

    def update(self, game_time: pyasge.GameTime):
        return self.child.update(game_time)


class SequenceNode:
    def __init__(self, nodes, data):
        # Sequence node, goes through children until one fails or all are gone through
        # Returns true if all children succeeded, returns false if one child fails
        self.data = data
        self.type = NodeType.SEQUENCE
        self.children = nodes

    def update(self, game_time: pyasge.GameTime):
        for child in self.children:
            update = child.update(game_time)
            if not update:
                return update
        return True


class SelectorNode:
    def __init__(self, nodes, data):
        # Selector node, goes through children until one succeeds or all are gone through
        # Returns false if all children fail, returns true if one child succeeds
        self.data = data
        self.type = NodeType.SELECTOR
        self.children = nodes

    def update(self, game_time: pyasge.GameTime):
        for child in self.children:
            update = child.update(game_time)
            if update:
                return update
        return False


class DecoratorNode:
    def __init__(self, child, data):
        # Decorator node, returns opposite of child
        self.data = data
        self.type = NodeType.DECORATOR
        self.child = child

    def update(self, game_time: pyasge.GameTime):
        return not self.child.update(game_time)


class InRangeCat:
    def __init__(self, targets, actor, data):
        # If there is a target is in range, return true [CHANGING RANGE, USED FOR CATS]
        self.targets = targets
        self.actor = actor
        self.data = data

    def update(self, game_time: pyasge.GameTime):
        att_range = self.data.attack_range * pow(self.data.stat_inc_per_level, self.data.upgrade_level-1)
        if self.data.boost_buff:
            att_range = att_range * self.data.boost_percent
        for target in self.targets:
            distance = pyasge.Point2D.distance(target.sprite.midpoint, self.actor.sprite.midpoint)
            if distance <= att_range and not target.rodent_data.invisible:
                return True
        return False


class InRangeRodent:
    def __init__(self, targets, actor, range_fixed):
        # If there is a target in range, return true [FIXED RANGE, USED FOR RODENTS]
        self.targets = targets
        self.actor = actor
        self.range = range_fixed

    def update(self, game_time: pyasge.GameTime):
        for target in self.targets:
            distance = pyasge.Point2D.distance(target.sprite.midpoint, self.actor.sprite.midpoint)
            if distance <= self.range and target.cat_data.cat_type == CatType.BLOCKER:
                self.actor.rodent_data.cat_in_range = True
                return True
        self.actor.rodent_data.cat_in_range = False
        return False


class ShootProjectile:
    def __init__(self, targets, actor, cat_data):
        # Shoot projectile at closest target
        self.targets = targets
        self.actor = actor
        self.timer = 0
        self.cat_data = cat_data

    def update(self, game_time: pyasge.GameTime):
        max_reload_timer = self.cat_data.reload_time / pow(self.cat_data.stat_inc_per_level, self.cat_data.upgrade_level-1)
        if self.cat_data.boost_buff:
            max_reload_timer = max_reload_timer / self.cat_data.boost_percent
        # If entity has had enough time between shots
        if self.timer >= max_reload_timer:
            # Find the closest target
            closest_target = None
            closest_dist = 1000
            for target in self.targets:
                distance = pyasge.Point2D.distance(target.sprite.midpoint, self.actor.sprite.midpoint)
                if distance < closest_dist and not target.rodent_data.invisible:
                    closest_dist = distance
                    closest_target = target
            # Shoot at closest target
            self.actor.cat_data.shooting = True
            self.actor.cat_data.targeted_rodent = closest_target
            self.timer = 0
        else:
            self.timer += game_time.frame_time
        return True


class LowHP:
    def __init__(self, data, low_hp):
        # Returns true if target is low hp
        self.data = data
        self.low_hp = low_hp

    def update(self, game_time: pyasge.GameTime):
        if self.data.fleeing:
            return True
        if self.data.hp <= self.low_hp:
            self.data.fleeing = True
            return True
        return False


class OnSpawnTile:
    def __init__(self, game_data, rodent):
        self.game_data = game_data
        self.rodent = rodent

    def update(self, game_time: pyasge.GameTime):
        # If rodent pos in range of game_data.spawn_tiles, de spawn the rodent and return true
        rodent_tile = self.game_data.game_map.tile(self.rodent.sprite.midpoint)
        for spawn in self.game_data.game_map.spawn_points:
            sp_point = pyasge.Point2D(spawn[0], spawn[1])
            spawn_tile = self.game_data.game_map.tile(sp_point)
            if spawn_tile == rodent_tile:
                self.rodent.rodent_data.on_spawn_tile = True
                return True
        return False


class OnDoorTile:
    def __init__(self, game_data, rodent):
        self.game_data = game_data
        self.rodent = rodent

    def update(self, game_time: pyasge.GameTime):
        # If rodent pos in range of game_data.home_points, de spawn the rodent and return true
        rodent_tile = self.game_data.game_map.tile(self.rodent.sprite.midpoint)
        for point in self.game_data.game_map.home_points:
            sp_point = pyasge.Point2D(point[0], point[1])
            spawn_tile = self.game_data.game_map.tile(sp_point)
            if spawn_tile == rodent_tile:
                self.rodent.rodent_data.on_home_tile = True
                return True
        return False


class GoToSpawn:
    def __init__(self, game_data, rodent):
        self.game_data = game_data
        self.rodent = rodent

    def update(self, game_time: pyasge.GameTime):
        # Path find to spawn
        if not self.rodent.rodent_data.update_path:
            return True
        self.rodent.rodent_data.update_path = False
        quickest_path = []
        quickest_cost = 0
        for spawn in self.game_data.game_map.spawn_points:
            path = resolve(pyasge.Point2D(spawn[0], spawn[1]), self.game_data,
                           self.rodent.sprite.midpoint, self.rodent.rodent_data.can_hidden_path)
            cost = path.pop(-1)
            if len(quickest_path) == 0 or cost < quickest_cost:
                quickest_path = path
                quickest_cost = cost
        self.rodent.destination = quickest_path
        return True


class GoToDoor:
    def __init__(self, game_data, rodent):
        self.game_data = game_data
        self.rodent = rodent

    def update(self, game_time: pyasge.GameTime):
        # Path find to door
        if not self.rodent.rodent_data.update_path:
            return True
        self.rodent.rodent_data.update_path = False
        quickest_path = []
        quickest_cost = 0
        for home_point in self.game_data.game_map.home_points:
            path = resolve(pyasge.Point2D(home_point[0], home_point[1]), self.game_data,
                           self.rodent.sprite.midpoint, self.rodent.rodent_data.can_hidden_path)
            cost = path.pop(-1)
            if len(quickest_path) == 0 or cost < quickest_cost:
                quickest_path = path
                quickest_cost = cost
        self.rodent.destination = quickest_path
        return True


class AttackCat:
    def __init__(self, targets, actor, rodent_data):
        # Attacks closest target [USED FOR RODENTS]
        self.targets = targets
        self.actor = actor
        self.timer = 0
        self.rodent_data = rodent_data

    def update(self, game_time: pyasge.GameTime):
        max_reload_timer = self.rodent_data.time_between_hits
        # If entity has had enough time between hits
        if self.timer >= max_reload_timer:
            # Find closest target
            closest_target = None
            closest_dist = 1000
            for target in self.targets:
                distance = pyasge.Point2D.distance(target.sprite.midpoint, self.actor.sprite.midpoint)
                if distance < closest_dist and target.cat_data.cat_type == CatType.BLOCKER:
                    closest_dist = distance
                    closest_target = target
            # Attack closest target
            self.actor.rodent_data.attacking = True
            self.actor.rodent_data.targeted_cat = closest_target
            self.timer = 0
        else:
            self.timer += game_time.frame_time
        #print("Attacking cat")
        return True


class GoToCat:
    def __init__(self, game_data, actor, targets):
        self.game_data = game_data
        self.actor = actor
        self.targets = targets

    def update(self, game_time: pyasge.GameTime):
        # Find closest target
        if not self.actor.rodent_data.update_path:
            return True
        self.actor.rodent_data.update_path = False
        closest_target = None
        closest_dist = 1000
        for target in self.targets:
            distance = pyasge.Point2D.distance(target.sprite.midpoint, self.actor.sprite.midpoint)
            if distance < closest_dist and target.cat_data.cat_type == CatType.BLOCKER:
                closest_dist = distance
                closest_target = target
        self.actor.rodent_data.targeted_cat = closest_target
        # Path find to target cat
        path = resolve(pyasge.Point2D(closest_target.sprite.midpoint.x, closest_target.sprite.midpoint.y),
                       self.game_data, self.actor.sprite.midpoint, self.actor.rodent_data.can_hidden_path)
        path.pop(-1)
        self.actor.destination = path
        return True


class GenerateYarn:
    def __init__(self, game_data, cat):
        self.game_data = game_data
        self.cat = cat
        self.timer = 0

    def update(self, game_time: pyasge.GameTime):
        # Inc Yarn
        if self.timer >= self.cat.cat_data.reload_time:
            self.game_data.yarn += self.cat.cat_data.yarn_per_resource
            self.timer = 0
        else:
            self.timer += game_time.frame_time

        return True


class SlowRodent:
    def __init__(self, targets, actor, data):
        # Slow all targets in range
        self.targets = targets
        self.actor = actor
        self.data = data

    def update(self, game_time: pyasge.GameTime):
        # Determines if target is in range
        att_range = self.data.attack_range * pow(self.data.stat_inc_per_level, self.data.upgrade_level-1)
        for target in self.targets:
            distance = pyasge.Point2D.distance(target.sprite.midpoint, self.actor.sprite.midpoint)
            # De buffs them if in range
            if distance <= att_range:
                target.rodent_data.slow_de_buff = True
            else:
                target.rodent_data.slow_de_buff = target.rodent_data.slow_de_buff
        return True


class BoostCat:
    def __init__(self, targets, actor, data):
        # Boost all targets in range
        self.targets = targets
        self.actor = actor
        self.data = data

    def update(self, game_time: pyasge.GameTime):
        # Determines if in range
        att_range = self.data.attack_range * pow(self.data.stat_inc_per_level, self.data.upgrade_level-1)
        for target in self.targets:
            distance = pyasge.Point2D.distance(target.sprite.midpoint, self.actor.sprite.midpoint)
            # Buffs them if in range
            if distance <= att_range:
                target.cat_data.boost_buff = True
            else:
                target.cat_data.boost_buff = False
        return True
