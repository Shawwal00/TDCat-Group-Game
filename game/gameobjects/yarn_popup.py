import pyasge


class YarnPopUp:
    def __init__(self, yarn: int, pos: pyasge.Point2D):
        # Create yarn sprite
        self.yarn = yarn
        self.sprite = pyasge.Sprite()
        self.sprite.loadTexture("/data/textures/ui_yarn.png")
        self.sprite.setMagFilter(pyasge.MagFilter.NEAREST)
        self.sprite.width = 64
        self.sprite.height = 64
        self.sprite.x = pos.x - 32
        self.sprite.y = pos.y - 32
        self.sprite.z_order = 70
        self.duration = 0.7
        self.timer = 0
        self.move_speed = 50
        self.remove = False

    def fixed_update(self, game_time: pyasge.GameTime):
        # Move up the screen slowly
        self.sprite.y -= self.move_speed * game_time.fixed_timestep
        self.timer += game_time.fixed_timestep
        # Delete it if duration ended
        if self.timer >= self.duration:
            self.remove = True

    def render(self, renderer: pyasge.Renderer, game_time: pyasge.GameTime) -> None:
        renderer.render(self.sprite)
