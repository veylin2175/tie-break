from screens.menu_screen import MenuScreen
from screens.menus.game_mode_menu import GameModeMenuScreen
from renders.button import Button
from renders.text_box import TextBox


class StartMenuScreen(MenuScreen):
    def __init__(self, screen, clock, options):
        super().__init__(screen, clock, options)
        self.texts += [TextBox(text="Тай-брейк", **self.title_params)]
        B_Y, B_GAP = 250, 120
        buttons_params = self.rect_params | {"x": "center", "width": 300, "height": 100}
        self.start_button = Button(y=B_Y + B_GAP, text="СТАРТ", **buttons_params)
        self.quit_button = Button(y=B_Y + B_GAP * 2, text="ВЫХОД", **buttons_params)

        self.button_sections += [
            [self.start_button],
            [self.quit_button],
        ]

    def button_click_up(self, button):
        super().button_click_up(button)
        if button is not None:
            if button == self.start_button:
                self.open_game_mode_menu()
            elif button == self.quit_button:
                self.quit()

    def open_game_mode_menu(self):
        game_mode_menu_screen = GameModeMenuScreen(
            self.screen, self.clock, self.options
        )
        game_mode_menu_screen.run()

    def escape(self):
        pass
