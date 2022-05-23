from game.gamedata import Difficulty


class WaveData:

    def __init__(self, difficulty) -> None:

        # Statuses
        self.spawning = True
        self.difficulty = difficulty

        # Stats Data
        self.wave_number = 1
        self.timer = 0
        self.time_between_waves = 4
        self.rodents_spawned = 0

        self.max_waves = None
        self.rodents_per_wave = []
        self.time_between_rodents = []

        if difficulty == Difficulty.NORMAL:
            self.max_waves = 10
            self.rodents_per_wave = [5, 5, 6, 7, 8, 9, 10, 12, 15, 20]
            self.time_between_rodents = [2, 2, 2, 1.5, 1.5, 1.5, 1.5, 1.2, 1.2, 1.2]
        elif difficulty == Difficulty.EASY:
            self.max_waves = 5
            self.rodents_per_wave = [4, 5, 5, 6, 8]
            self.time_between_rodents = [2, 2, 2, 1.5, 1.5]
        elif difficulty == Difficulty.HARD:
            self.max_waves = 20
            self.rodents_per_wave = [6, 6, 7, 7, 9, 10, 11, 12, 15, 20,
                                     22, 25, 27, 30, 33, 36, 40, 43, 46, 50]
            self.time_between_rodents = [2, 1.8, 1.6, 1.5, 1.4, 1.3, 1.2, 1, 0.9, 0.8,
                                         0.6, 0.5, 0.4, 0.4, 0.4, 0.3, 0.3, 0.2, 0.2, 0.1]
