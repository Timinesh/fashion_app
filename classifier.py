# classifier.py

import json
import os
import time

from dotenv import load_dotenv
from openai import OpenAI

from constants import CATEGORIES, STYLE_TAGS

VALID_CATEGORIES = [
    "top",
    "bottom",
    "dress",
    "outerwear",
    "shoes",
    "accessory",
]

VALID_COLORS = [
    "black",
    "white",
    "gray",
    "navy",
    "blue",
    "red",
    "maroon",
    "green",
    "olive",
    "mustard",
    "orange",
    "brown",
    "beige",
    "pink",
    "purple",
    "teal",
    "cream",
    "denim",
]

VALID_STYLE_TAGS = [
    "casual",
    "formal",
    "work",
    "party",
    "summer",
    "winter",
    "sport",
    "date-night",
]

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


SYSTEM_PROMPT = """
You are an expert fashion classifier.

Return ONLY valid JSON.

You MUST ONLY use the following values.

Categories:
- top
- bottom
- dress
- outerwear
- shoes
- accessory

Primary Color:
- black
- white
- gray
- navy
- blue
- red
- maroon
- green
- olive
- mustard
- orange
- brown
- beige
- pink
- purple
- teal
- cream
- denim

Style Tags (choose 1-3 only):
- casual
- formal
- work
- party
- summer
- winter
- sport
- date-night

Return this schema exactly:

{
  "category": "...",
  "primaryColor": "...",
  "styleTags": ["..."]
}

Rules:

- Return exactly one category.
- Return exactly one primary color.
- Return between one and three style tags.
- Never invent new categories.
- Never invent new colors.
- Never invent new style tags.
- Return ONLY JSON.
"""


def classify_once(base64_image):

    response = client.responses.create(
        model="gpt-5.5",
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": SYSTEM_PROMPT,
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    }
                ],
            },
        ],
    )

    text = response.output_text.strip()

    start = text.find("{")
    end = text.rfind("}")

    if start == -1:
        raise ValueError("No JSON returned.")

    data = json.loads(text[start : end + 1])

    category = data["category"]
    if category not in VALID_CATEGORIES:
        raise ValueError("Invalid category")

    primary_color = data["primaryColor"]
    if primary_color not in VALID_COLORS:
        raise ValueError("Invalid color")

    style_tags = [tag for tag in data["styleTags"] if tag in VALID_STYLE_TAGS]

    if not style_tags:
        style_tags = ["casual"]

    tags = []

    for tag in data.get("styleTags", []):
        if tag in STYLE_TAGS:
            tags.append(tag)

    tags = tags[:3]

    if len(tags) == 0:
        tags.append("casual")

    return {
        "category": category,
        "primaryColor": primary_color,
        "styleTags": style_tags,
    }


def classify_garment(base64_image, retries=3):

    last_error = None

    for attempt in range(retries):
        try:
            return classify_once(base64_image)

        except Exception as e:
            last_error = e

            time.sleep(1 + attempt)

    print(last_error)

    return {
        "category": "top",
        "primaryColor": "black",
        "styleTags": ["casual"],
        "failed": True,
    }
