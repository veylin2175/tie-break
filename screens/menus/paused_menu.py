import pygame
from screens.menu_screen import MenuScreen
from renders.button import Button
from renders.text_box import TextBox
from utils.constants import MUSIC as M


class PausedMenuScreen(MenuScreen):
    def __init__(self, screen, clock, options):
        super().__init__(screen, clock, options)
        pygame.mixer.music.pause()
        self.texts += [TextBox(text="ТАЙМАУТ", **self.title_params)]

        B_Y, B_GAP = 250, 150
        buttons_params = self.rect_params | {"x": "center", "width": 300, "height": 100}
        self.resume_button = Button(y=B_Y + B_GAP, text="ПРОДОЛЖИТЬ", **buttons_params)
        self.home_button = Button(y=B_Y + B_GAP * 2, text="ДОМОЙ", **buttons_params)

        self.button_sections += [
            [self.resume_button],
            [self.home_button],
        ]

    def button_click_up(self, button):
        super().button_click_up(button)
        if button is not None:
            if button == self.resume_button:
                self.resume()
            elif button == self.home_button:
                self.open_start_menu()

    def resume(self):
        pygame.mixer.music.unpause()
        self.running = False

    def open_start_menu(self):
        from screens.menus.start_menu import StartMenuScreen

        pygame.mixer.music.load(M.MENU_BACKGROUND)
        pygame.mixer.music.play(-1)
        start_menu = StartMenuScreen(self.screen, self.clock, self.options)
        start_menu.run()

    def run(self):
        super().run()
        return self.options

    def escape(self):
        self.resume()
