COLORS = ["red", "yellow", "green", "blue"]
ALL_COLORS = COLORS + ["black"]
SPECIAL = ["challenge", "reverse", "mistake", "unsportsmanlike_conduct", "motivation"] # TODO: специальные карты
WILD_SPECIAL = ["serve", "receive", "spike", "defence", "dump", "tip", "block", "dig", "pass"] # TODO: карты, отображаемые в квадрате на экране
COLOR_ACTION_VALUES = ["receive", "defence", "block", "spike", "dump", "pass", "dig", "tip", "mistake", "reverse", "motivation"] # TODO: обычные цветные
WILD_ACTION_VALUES = ["unsportsmanlike_conduct", "serve", "challenge"] # TODO: черные обычные
CARD_ABBREVIATIONS = {
    "unsportsmanlike_conduct": "+4",
    "reverse": "↔",
    "mistake": "ошибка",
    "motivation": "мотив",
    "challenge": "видео",
    "receive": "прием",
    "defence": "защита",
    "block": "блок",
    "spike": "удар",
    "dump": "обман",
    "pass": "пас",
    "dig": "стр",
    "tip": "прброс",
    "serve": "подача",
}

CARD_RULES = {
    "serve": ["receive", "defence", "motivation", "mistake", "reverse", "unsportsmanlike_conduct", "challenge", "serve"],
    "receive": ["pass", "dig"],
    "pass": ["spike", "tip"],
    "spike": ["block", "defence"],
    "tip": ["block", "defence"],
    "dig": ["dump"],
    "dump": ["pass"],
    "block": ["mistake"],
    "mistake": ["motivation"],
    "motivation": COLOR_ACTION_VALUES,  # После мотивации можно любую цветную
}