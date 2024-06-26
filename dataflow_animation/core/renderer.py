import os
import sys
from typing import Optional
import logging
import traceback

from pygame import Surface
import pygame

from dataflow_animation.settings.config import get_config, reset_config
from dataflow_animation import Dataflow, __version__
from dataflow_animation.types import Milliseconds


class PygameRenderer:
    def __init__(self):
        self.animation: Optional[Dataflow] = None
        self.screen: Surface = None
        self.clock: pygame.time.Clock = None
        self.running = True

        # Logic
        self.tick_duration: Milliseconds = 0

    @property
    def is_ready(self):
        if not self.animation:
            return False
        return self.animation.engine.is_ready

    def set_animation(self, animation):
        self.animation = animation
        self.build_animation_sequence()

    def init(self):
        os.environ["SDL_VIDEO_WINDOW_POS"] = get_config().sdl_video_window_pos
        pygame.init()
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        pygame.display.set_caption(
            f"Dataflow Animation {__version__} | Python {python_version}"
        )

        self.screen = pygame.display.set_mode(
            (get_config().width, get_config().height),
        )
        self.animation.engine.set_surface(self.screen)

        self.clock = pygame.time.Clock()

    def run(self):
        try:
            while self.running:
                self.parse_events()
                self.render()

        finally:
            pygame.quit()
            logging.info("Pygame stopped.")

    def parse_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def render(self):
        self.screen.fill(get_config().background_color)
        if self.animation:
            self.animation.engine.render(self.tick_duration)

        pygame.display.update()
        self.tick_duration = self.clock.tick(get_config().fps)

    def build_animation_sequence(self):
        if self.animation is None:
            return

        try:
            reset_config()
            if self.screen:
                self.animation.engine.set_surface(self.screen)

            self.animation.setup()
            if not self.animation.engine.is_ready:
                raise ValueError(
                    "Animation is not ready. Please register atleast one:"
                    + " Entity, Information, and AnimationStep"
                    + "(via animate function)."
                )

            self.animation.engine.setup()

        except pygame.error as e:
            logging.error("Pygame error: %s", e)

        # pylint: disable=W0718
        except Exception:
            logging.error(
                "Error building the animations:\n%s",
                traceback.format_exc(),
            )
            self.set_animation(None)

    def stop(self):
        self.running = False
