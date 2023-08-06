import pygame
from coopstructs.vectors import Vector2
from coopstructs.geometry import Rectangle
from coopgame.colors import Color
import functools
from coopgame.pygbutton import PygButton
from coopbugger.monitoredclass import MonitoredClass
from typing import Callable, List, Dict, Optional
import coopgame.pygamehelpers as help
from coopgame.logger import logger
from coopgame.sprites import AnimatedSprite
from coopstructs.geometry import Rectangle as cRect
from coopgame.monitoredClassLogger import MonitoredClassLogger
from cooptools.coopEnum import CoopEnum
from enum import auto
import inspect
from pygame_k_constant_names import pygame_key_mapper

def try_handler(func):
    @functools.wraps(func)
    def wrapper_handler(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except NotImplementedError as e:
            error = f"Inherited class should implement logic for {func.__name__}"
            logger.debug(error)
        except Exception as e:
            logger.exception(e)

    return wrapper_handler

class BuiltInSurfaceType(CoopEnum):
    BACKGROUND = auto()
    FOREGROUND = auto()
    HELP = auto()

class GameTemplate(MonitoredClass):

    def __init__(self, fullscreen: bool = False, screen_width: int = 1600, screen_height: int = 1000,
                 max_fps: int = 120, debug_mode=False):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.fullscreen = fullscreen
        self.screen = None
        self._init_screen(self.fullscreen)

        self.ticks = 0
        self.frame_times = []
        self.fps = None
        self.max_fps = max_fps
        self.clock = pygame.time.Clock()

        self.buttons = {}
        self._key_handlers = {
            (pygame.K_ESCAPE,): (self.quit, False),
            (pygame.K_F12,): (self.toggle_fullscreen, False),
            (pygame.K_F11,): (self.toggle_debug_mode, False)

        }
        self.register_keys()

        self.sprites = {}

        self.running = False
        self._debug_mode = debug_mode

        self._monitored_class_logger = MonitoredClassLogger(monitored_classes=[self])

        # build in surfaces
        self.built_in_surfaces: Dict[BuiltInSurfaceType, Optional[pygame.Surface]] = {
            BuiltInSurfaceType.BACKGROUND: None,
            BuiltInSurfaceType.FOREGROUND: None,
            BuiltInSurfaceType.HELP: None
        }

        pygame.init()

    def quit(self):
        self.running = False

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self._init_screen(self.fullscreen)

    def _init_screen(self, fullscreen):
        if fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

    def register_button(self, id, text, callback, postion_rect):
        self.buttons[id] = PygButton(postion_rect, caption=text, callback=callback)

    def main(self):

        self.initialize_game()

        self.running = True
        ii = 0
        while self.running:
            self._update()
            self._draw(frames=ii)
            self.clock.tick(self.max_fps)
            ii += 1

        pygame.quit()

    def calculate_fps(self, ticks_last_frame: int):
        if len(self.frame_times) > 20:
            self.frame_times.pop(0)

        self.frame_times.append(ticks_last_frame)

        avg_sec_per_frame = sum(self.frame_times) / len(self.frame_times) / 1000.0
        self.fps = 1 / avg_sec_per_frame if avg_sec_per_frame > 0 else 0

    def _update(self):
        """:return
            Update environment based on time delta and any input
        """

        ''' Calculate the ticks between update calls so that the update functions can handle correct time deltas '''
        t = pygame.time.get_ticks()
        delta_time_ms = (t - self.ticks)
        self.ticks = t
        self.calculate_fps(delta_time_ms)

        '''Log Stats'''
        self._monitored_class_logger.check_and_log(delta_time_ms)

        '''Update Model'''
        self._model_updater(delta_time_ms)

        '''Update Sprites'''
        self.sprite_updater(delta_time_ms)

        '''Animate Sprites'''
        self._sprite_animator(delta_time_ms)

        '''Handle Events'''
        self._handle_events()

    def _handle_events(self):
        """:return
            handle all of the registered events that have been captured since last iteration
        """

        '''Get next event'''
        for event in pygame.event.get():

            '''Get pressed keys'''
            pressed_keys = pygame.key.get_pressed()

            '''Check and handle button press'''
            self.handle_buttons(event)

            '''Debug Printer'''
            if event.type not in (0, 1, 4, 6):
                logger.debug(f"Pygame EventType: {event.type}")

            '''Event Type Switch'''
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN:
                self._handle_key_pressed(pressed_keys)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                logger.info(f"Left Mouse Down")
                self.handle_left_mouse_down(pressed_keys)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                logger.info(f"Left Mouse Up")
                self.handle_left_mouse_up(pressed_keys)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                logger.info(f"Right Mouse Down")
                self.handle_right_mouse_down(pressed_keys)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                logger.info(f"Right Mouse Up")
                self.handle_right_mouse_up(pressed_keys)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                logger.info(f"Scroll Up")
                self.handle_mouse_scroll_up(pressed_keys)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                logger.info(f"Scroll Down")
                self.handle_mouse_scroll_down(pressed_keys)
            elif event.type == pygame.VIDEORESIZE:
                logger.info(f"Window Resized [{self.screen.get_width()}x{self.screen.get_height()}]")
                self.on_resize()

        '''Get pressed keys'''
        pressed_keys = pygame.key.get_pressed()

        '''Handle Held Keys'''
        if pressed_keys is not None:
            self._handle_held_keys(pressed_keys)

        '''Handle hover over'''
        self._handle_hover_over()

    def register_action_to_keys(self, keys_tuple, func: Callable, react_while_holding: bool = False):
        """
            Takes a tuple of keys (integers) and maps that key combo to a callable function

            :param keys_tuple a list of keys (integers) that will be mapped to the input callable. Note that a single
            value Tuple is input as ([key],) *note the comma
            :param func a callable that is mapped to the key combo
        """
        self._key_handlers[keys_tuple] = (func, react_while_holding)

    @MonitoredClass.timer
    @try_handler
    def handle_buttons(self, event):
        for id, button in self.buttons:
            if 'click' in button.handleEvent(event):
                button.callback()

    @MonitoredClass.timer
    @try_handler
    def _handle_key_pressed(self, pressed_keys):
        buttons = [pygame.key.name(k) for k, v in enumerate(pressed_keys) if v]
        logger.info(f"Keys pressed: {buttons}")
        for mapped_keys, reaction in self._key_handlers.items():
            func = reaction[0]
            if (all(pressed_keys[key] for key in mapped_keys)):
                func()

    @MonitoredClass.timer
    @try_handler
    def _handle_held_keys(self, pressed_keys):
        for mapped_keys, reaction in self._key_handlers.items():
            func = reaction[0]
            react_while_holding = reaction[1]
            if (all(pressed_keys[key] for key in mapped_keys)) and react_while_holding:
                func()

    @MonitoredClass.timer
    @try_handler
    def _handle_hover_over(self):
        mouse_pos_as_vector = help.mouse_pos_as_vector()
        if mouse_pos_as_vector:
            self.handle_hover_over(mouse_pos_as_vector)

    @MonitoredClass.timer
    @try_handler
    def _model_updater(self, delta_time_ms: int):
        return self.model_updater(delta_time_ms)

    @try_handler
    def initialize_game(self):
        raise NotImplementedError()

    @try_handler
    def handle_left_mouse_down(self, pressed_keys):
        raise NotImplementedError()

    @try_handler
    def handle_left_mouse_up(self, pressed_keys):
        raise NotImplementedError()

    @try_handler
    def handle_right_mouse_down(self, pressed_keys):
        raise NotImplementedError()

    @try_handler
    def handle_right_mouse_up(self, pressed_keys):
        raise NotImplementedError()

    @try_handler
    def handle_hover_over(self, mouse_pos_as_vector: Vector2):
        raise NotImplementedError()

    @try_handler
    def handle_mouse_scroll_up(self, pressed_keys):
        raise NotImplementedError()

    @try_handler
    def handle_mouse_scroll_down(self, pressed_keys):
        raise NotImplementedError()

    @try_handler
    def draw(self, frames: int, debug_mode: bool = False):
        raise NotImplementedError()

    @try_handler
    def model_updater(self, delta_time_ms: int):
        raise NotImplementedError()

    @try_handler
    def sprite_updater(self, delta_time_ms: int):
        raise NotImplementedError()

    @try_handler
    def on_resize(self):
        raise NotImplementedError()

    @try_handler
    def register_keys(self):
        raise NotImplementedError()

    @try_handler
    def update_built_in_surfaces(self, surface_types: List[BuiltInSurfaceType]):
        raise NotImplementedError()

    @MonitoredClass.timer
    def _draw(self, frames: int):
        self.screen.fill(Color.BLACK.value)
        self.draw(frames, self._debug_mode)

        '''Draw Sprites'''
        self.sprite_drawer(self.screen)

        if self._debug_mode:
            self.draw_mouse_coord(self.screen)
            self.draw_fps(self.screen, offset_rect=cRect(0, self.screen.get_height() - 100, 20, 100))
            self.draw_game_time(self.screen, offset_rect=cRect(0, self.screen.get_height() - 150, 20, 200))
            self.draw_text(f"Sprite Count: {len(self.sprites)}", self.screen, offset_rect=Rectangle(0, 90, 100, 200))

        # Update the display
        pygame.display.flip()

    def draw_mouse_coord(self, hud: pygame.Surface, font: pygame.font.Font = None, offset_rect: Rectangle = None,
                         color: Color = None):
        mouse_pos_as_vector = help.mouse_pos_as_vector()
        txt = f"M:<{int(mouse_pos_as_vector.x)}, {int(mouse_pos_as_vector.y)}>"
        self.draw_text(txt, hud=hud, font=font, offset_rect=offset_rect, color=color)

    def draw_game_time(self, hud: pygame.Surface, font: pygame.font.Font = None, offset_rect: Rectangle = None,
                       color: Color = None):
        txt = f"GameTime: {self.ticks / 1000}"
        self.draw_text(txt, hud=hud, font=font, offset_rect=offset_rect, color=color)

    def draw_fps(self, hud: pygame.Surface, font: pygame.font.Font = None, offset_rect: Rectangle = None,
                 color: Color = None):
        txt = f"FPS: {int(self.fps)}"
        self.draw_text(txt, hud=hud, font=font, offset_rect=offset_rect, color=color)

    def draw_text(self, text: str, hud: pygame.Surface, font: pygame.font.Font = None, offset_rect: Rectangle = None,
                  color: Color = None):
        if font is None:
            font = pygame.font.Font(None, 30)

        if offset_rect is None:
            offset_rect = Rectangle(0, hud.get_height() - 50, 20, hud.get_width())

        if color is None:
            color = Color.BLUE

        rendered_txt = font.render(text, True, color.value)
        display1 = hud.subsurface(offset_rect.x, offset_rect.y, offset_rect.width, offset_rect.height)
        display1.blit(rendered_txt, display1.get_rect())

    def window_rect(self):
        return Rectangle(0, 0, self.screen.get_height(), self.screen.get_width())

    def toggle_debug_mode(self):
        self._debug_mode = not self._debug_mode

    def draw_monitoredclass_stats(self, monitoredClass: MonitoredClass, surface: pygame.Surface,
                                  font: pygame.font.SysFont = None, offset_rectangle: Rectangle = None):
        if font is None:
            font = pygame.font.SysFont(None, 18)

        if offset_rectangle is None:
            offset_rectangle = Rectangle(0, 0, font.get_height() + 3, 300)

        tracked_time = [(key, val) for key, val in monitoredClass.tracked_time.items()]
        tracked_time.sort(key=lambda x: x[1], reverse=True)

        y_off = offset_rectangle.y
        offset_rectangle.y = y_off
        self.draw_text(f"RunTime Stats for {type(monitoredClass).__name__}", surface, color=Color.LEMON_CHIFFON,
                       offset_rect=offset_rectangle, font=font)
        y_off += font.get_height() + 3
        for key, val in tracked_time:
            offset_rectangle.y = y_off
            self.draw_text(f"{key}: {round(val, 2)} sec", surface, color=Color.LEMON_CHIFFON,
                           offset_rect=offset_rectangle, font=font)
            y_off += font.get_height() + 3

    @property
    def game_area_rectangle(self):
        return Rectangle(0, 0, self.screen.get_height(), self.screen.get_width())

    def _sprite_animator(self,
                         delta_time_ms: int):

        for name, sprite in self.sprites.items():
            if type(sprite) == AnimatedSprite:
                sprite.animate(delta_time_ms)

    def sprite_drawer(self,
                      surface: pygame.surface):

        sprites = list(self.sprites.values())
        sprites.sort(key=lambda x: x.bottom_center_pos.y)
        for sprite in sprites:
            sprite.blit(surface, display_handle=self._debug_mode, display_rect=self._debug_mode)

    def register_monitored_classes(self, new_classes: List[MonitoredClass]):
        self._monitored_class_logger.register_classes(new_classes)

    def init_builtin_surfaces(self, types: List[BuiltInSurfaceType] = None, colorkey: Color = None):
        if colorkey is None: colorkey = Color.BLACK
        if types is None: types = [e for e in BuiltInSurfaceType]

        for type in types:
            self.built_in_surfaces[type] = pygame.Surface(self.screen.get_size()).convert()
            self.built_in_surfaces[type].set_colorkey(colorkey.value)

    def _update_help_surface(self):
        text = self._help_txt()

        self.built_in_surfaces[BuiltInSurfaceType.HELP].fill(Color.WHEAT.value)

        font = pygame.font.Font(None, 20)
        fontsize = font.get_height()
        offSet = 0

        for idx, line in enumerate(text):
            self.draw_text(line,
                           self.built_in_surfaces[BuiltInSurfaceType.HELP],
                           font=font,
                           offset_rect=Rectangle(0,
                                                 idx * fontsize + offSet,
                                                 fontsize + 3,
                                                 self.built_in_surfaces[BuiltInSurfaceType.HELP].get_width()))

    def _help_txt(self):

        txt = []
        txt.append("HELP")
        txt.append("\n--------")
        txt.append("\n")
        for k, v in self._key_handlers.items():
            if len(v) > 2:
                callback_txt = v[2]
            elif v[0].__name__ == "<lambda>":
                callback_txt = inspect.getsource(v[0])
                callback_txt = callback_txt.split("lambda:", 1)[1].split('(', 1)[0].replace("self.", "")
            else:
                callback_txt = v[0].__name__
            k_tup = [pygame_key_mapper(x) for x in k]
            txt.append(f"{k_tup} -- {callback_txt}")

        return txt