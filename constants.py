# constants.py

PALETTE = {
    "ink": "#211D1A",
    "paper": "#EFEAE0",
    "card": "#FBF9F4",
    "thread": "#2E6B4F",
    "rust": "#B14B2A",
    "mustard": "#C8941B",
    "line": "#D8D2C4",
    "faint": "#8A8377",
}

NAMED_COLORS = [
    ("black", (24, 22, 20)),
    ("white", (246, 244, 238)),
    ("gray", (130, 128, 122)),
    ("navy", (24, 33, 66)),
    ("blue", (52, 92, 176)),
    ("red", (178, 42, 40)),
    ("maroon", (98, 24, 30)),
    ("green", (46, 108, 62)),
    ("olive", (108, 106, 46)),
    ("mustard", (198, 158, 42)),
    ("orange", (214, 118, 42)),
    ("brown", (108, 72, 42)),
    ("beige", (208, 188, 152)),
    ("pink", (224, 148, 168)),
    ("purple", (108, 62, 138)),
    ("teal", (32, 118, 118)),
    ("cream", (232, 222, 200)),
    ("denim", (70, 95, 130)),
]

COLOR_RGB = {
    "black": (24, 22, 20),
    "white": (246, 244, 238),
    "gray": (130, 128, 122),
    "navy": (24, 33, 66),
    "blue": (52, 92, 176),
    "red": (178, 42, 40),
    "maroon": (98, 24, 30),
    "green": (46, 108, 62),
    "olive": (108, 106, 46),
    "mustard": (198, 158, 42),
    "orange": (214, 118, 42),
    "brown": (108, 72, 42),
    "beige": (208, 188, 152),
    "pink": (224, 148, 168),
    "purple": (108, 62, 138),
    "teal": (32, 118, 118),
    "cream": (232, 222, 200),
    "denim": (70, 95, 130),
}

CATEGORIES = [
    "top",
    "bottom",
    "dress",
    "outerwear",
    "shoes",
    "accessory",
]

STYLE_TAGS = [
    "casual",
    "formal",
    "work",
    "party",
    "summer",
    "winter",
    "sport",
    "date-night",
]

MAX_IMAGE_SIZE = 380
CENTER_SAMPLE_SIZE = 18
JPEG_QUALITY = 85

DATABASE_FILE = "data/wardrobe.json"
