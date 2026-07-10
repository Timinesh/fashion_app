# outfit_engine.py

from constants import CATEGORIES, STYLE_TAGS


def score_item(item, prompt):
    """
    Scores a clothing item based on how well it matches
    the user's outfit request.
    """

    prompt = prompt.lower()

    score = 0

    for tag in item.get("styleTags", []):
        if tag.lower() in prompt:
            score += 2

    if item.get("colorName", "").lower() in prompt:
        score += 1

    if item.get("category", "").lower() in prompt:
        score += 1

    return score


def group_by_category(items):

    grouped = {}

    for category in CATEGORIES:
        grouped[category] = []

    for item in items:
        grouped[item["category"]].append(item)

    return grouped


def pick_best(items, prompt):

    if not items:
        return None

    best = items[0]
    best_score = score_item(best, prompt)

    for item in items[1:]:
        s = score_item(item, prompt)

        if s > best_score:
            best = item
            best_score = s

    return best


def suggest_outfit(items, prompt):

    grouped = group_by_category(items)

    outfit = {}

    missing = []

    dress = pick_best(
        grouped["dress"],
        prompt,
    )

    if dress and score_item(dress, prompt) > 0:
        outfit["dress"] = dress

    else:
        top = pick_best(
            grouped["top"],
            prompt,
        )

        bottom = pick_best(
            grouped["bottom"],
            prompt,
        )

        if top:
            outfit["top"] = top
        else:
            missing.append("top")

        if bottom:
            outfit["bottom"] = bottom
        else:
            missing.append("bottom")

    shoes = pick_best(
        grouped["shoes"],
        prompt,
    )

    if shoes:
        outfit["shoes"] = shoes
    else:
        missing.append("shoes")

    outerwear = pick_best(
        grouped["outerwear"],
        prompt,
    )

    if outerwear and score_item(outerwear, prompt) > 0:
        outfit["outerwear"] = outerwear

    accessory = pick_best(
        grouped["accessory"],
        prompt,
    )

    if accessory and score_item(accessory, prompt) > 0:
        outfit["accessory"] = accessory

    return outfit, missing


def amazon_link(category, prompt=""):

    tags = []

    prompt = prompt.lower()

    for tag in STYLE_TAGS:
        if tag in prompt:
            tags.append(tag)

    query = " ".join(tags + [category])

    query = query.replace(" ", "+")

    return f"https://www.amazon.com/s?k={query}"


def build_shopping_list(missing_categories, prompt):

    shopping = []

    for category in missing_categories:
        shopping.append(
            {
                "category": category,
                "url": amazon_link(
                    category,
                    prompt,
                ),
            }
        )

    return shopping
