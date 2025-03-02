import os
import ctypes

SIZE_RATIO = {"small": 1 / 2, "medium": 3 / 4, "large": 1}

user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
w = user32.GetSystemMetrics(0)
h = user32.GetSystemMetrics(1)

# Screen properties
class SCREEN:
    WIDTH_BASE = w
    HEIGHT_BASE = h
    TITLE_Y = 80
    WIDTH = {"large": w}
    HEIGHT = {"large": h}
    SIZE = {
        "large": (WIDTH["large"], HEIGHT["large"]),
    }
    BACKGROUND_COLOR = (255, 195, 113)
    FONT_SIZE = 30
    FPS = 60


# PATHS

SOUNDS_PATH = os.path.join("assets", "sounds")
IMAGES_PATH = os.path.join("assets", "images")


class SOUND:
    # SOUND
    BUTTON_CLICK = os.path.join(SOUNDS_PATH, "button_click.mp3")
    CARD_MOVE = os.path.join(SOUNDS_PATH, "card_move.mp3")
    CARD_FLIP = os.path.join(SOUNDS_PATH, "card_flip.mp3")
    ERROR = os.path.join(SOUNDS_PATH, "error.mp3")
    UNO = os.path.join(SOUNDS_PATH, "uno.mp3")
    FAILED = os.path.join(SOUNDS_PATH, "failed.mp3")
    # change path to os path


class MUSIC:
    MENU_BACKGROUND = os.path.join(SOUNDS_PATH, "sinnesloschen-beam.mp3")
    GAME_BACKGROUND = os.path.join(SOUNDS_PATH, "cool-jazz-loops-2641.mp3")
    RED_ZONE_BACKGROUND = os.path.join(SOUNDS_PATH, "japan-koto-folk-background-music-124876.mp3")
    GREEN_ZONE_BACKGROUND = os.path.join(SOUNDS_PATH, "secret-garden-mystically-chill-out-music-7489.mp3")
    YELLOW_ZONE_BACKGROUND = os.path.join(SOUNDS_PATH, "middle-east-127104.mp3")
    BLUE_ZONE_BACKGROUND = os.path.join(SOUNDS_PATH, "cinematic-landscape-118672.mp3")

# Colors
COLORS_DICT = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 50, 50),
    "green": (50, 255, 50),
    "blue": (50, 50, 255),
    "yellow": (255, 255, 50),
    "dark_gray": (50, 50, 50),
    "morning": (255, 95, 109),
}
COLOR_BLIND_FRIENDLY_COLORS_DICT = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (216, 27, 96),
    "green": (17, 218, 197),
    "blue": (30, 136, 229),
    "yellow": (255, 193, 7),
    "dark_gray": (40, 40, 40),
    "morning": (255, 95, 109),
}

COLORS = COLORS_DICT.keys()
COLOR_BLIND_FRIENDLY_COLORS = COLOR_BLIND_FRIENDLY_COLORS_DICT.keys()

# Font properties
FONT_SIZE_BASE = 10
FONT_SIZES = {
    "large": FONT_SIZE_BASE * SIZE_RATIO["large"],
}


# Card properties
class CARD:
    WIDTH = 100
    HEIGHT = 150
    FONT_SIZE = 30
    TEXT_COLOR = "white"
    BACKGROUND_COLOR = "black"
    BACK_COLOR = "black"


# Button properties
class BUTTON:
    WIDTH = 180
    HEIGHT = 60
    FONT_SIZE = 40
    COLOR = "black"
    HOVER_COLOR = "white"
    SELECT_COLOR = "dark_gray"
    TEXT_COLOR = "white"
    TEXT_HOVER_COLOR = "black"
    TEXT_SELECT_COLOR = "white"
    BORDER_COLOR = "white"
    TEXT_DISABLE_COLOR = "dark_gray"


class TEXTBOX:
    FONT = "Commodore-64-v6.3"
    FONT_SIZE = 60
    TEXT_COLOR = "white"
    BORDER_COLOR = "white"


class INPUTBOX:
    FONT_SIZE = 40
    TEXT_COLOR = "white"
    BORDER_COLOR = "white"
    BACKGROUND_COLOR = "black"
    WIDTH = 300
    HEIGHT = 60
    BORDER_WIDTH = 0
    HOVERED_BORDER_WIDTH = 2
    SELECTED_BORDER_WIDTH = 4