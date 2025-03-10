from screens.menu_screen import MenuScreen
from screens.menus.join_menu import JoinMenuScreen
from screens.menus.multiplay_lobby_menu import MultiplayLobbyMenuScreen
from renders.button import Button
from renders.text_box import TextBox


class MultiplayMenuScreen(MenuScreen):
    def __init__(self, screen, clock, options):
        super().__init__(screen, clock, options)
        self.texts += [TextBox(text="МУЛЬТИПЛЕЕР", **self.title_params)]
        B_Y, B_GAP = 250, 150
        buttons_params = self.rect_params | {"x": "center", "width": 300, "height": 100}
        self.host_button = Button(y=B_Y, text="ХОСТ", **buttons_params)
        self.join_button = Button(y=B_Y + B_GAP, text="ПРИСОЕДИНИТЬСЯ", **buttons_params)
        self.back_button = Button(y=B_Y + B_GAP * 2, text="НАЗАД", **buttons_params)

        self.button_sections += [
            [self.host_button],
            [self.join_button],
            [self.back_button],
        ]

    def button_click_up(self, button):
        super().button_click_up(button)
        if button is not None:
            if button == self.host_button:
                self.host()
            elif button == self.join_button:
                self.join()
            elif button == self.back_button:
                self.back()

    def host(self):
        host_menu_screen = MultiplayLobbyMenuScreen(
            self.screen, self.clock, self.options, isHost=True
        )
        host_menu_screen.run()
        pass

    def join(self):
        join_menu_screen = JoinMenuScreen(self.screen, self.clock, self.options)
        join_menu_screen.run()
