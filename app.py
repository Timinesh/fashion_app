import streamlit as st
import uuid
from collections import defaultdict
from constants import COLOR_RGB
from PIL import Image
import json
import os
import shutil

from constants import (
    PALETTE,
    STYLE_TAGS,
    CATEGORIES,
    NAMED_COLORS,
)

from database import (
    load_items,
    save_items,
)

from image_processing import (
    prepare_image,
)

from classifier import (
    classify_garment,
)

from outfit_engine import (
    suggest_outfit,
    build_shopping_list,
)


st.set_page_config(
    page_title="WardrobeIQ",
    page_icon="👔",
    layout="wide",
)


if "closet" not in st.session_state:
    st.session_state.closet = load_items()

if "outfit" not in st.session_state:
    st.session_state.outfit = None

if "shopping" not in st.session_state:
    st.session_state.shopping = []

if "prompt" not in st.session_state:
    st.session_state.prompt = ""


def save():
    save_items(st.session_state.closet)


def remove_item(item_id):

    st.session_state.closet = [
        item for item in st.session_state.closet if item["id"] != item_id
    ]

    save()


def update_item(item_id, key, value):

    for item in st.session_state.closet:
        if item["id"] == item_id:
            item[key] = value
            break

    save()


def classify_and_add(upload):

    prepared = prepare_image(upload)

    result = classify_garment(prepared["base64"])

    os.makedirs("images", exist_ok=True)

    image_id = str(uuid.uuid4())
    image_path = f"images/{image_id}.jpg"

    prepared["image"].save(image_path)

    item = {
        "id": image_id,
        "image": image_path,
        "rgb": COLOR_RGB[result["primaryColor"]],
        "colorName": result["primaryColor"],
        "category": result["category"],
        "styleTags": result["styleTags"],
    }

    st.session_state.closet.append(item)

    save()


def group_items():

    groups = defaultdict(list)

    for item in st.session_state.closet:
        groups[item["colorName"]].append(item)

    return dict(groups)


def color_circle(rgb):

    return (
        f"<div style='width:18px;"
        f"height:18px;"
        f"border-radius:50%;"
        f"background:rgb({rgb[0]},{rgb[1]},{rgb[2]});"
        f"border:1px solid #888;'>"
        f"</div>"
    )


st.markdown(
    f"""
<style>

.main {{

background:{PALETTE["paper"]};

}}

h1,h2,h3 {{

color:{PALETTE["ink"]};

}}

.stButton>button {{

background:{PALETTE["thread"]};

color:white;

border:none;

}}

div[data-testid="stFileUploader"] {{

border:2px dashed {PALETTE["faint"]};

padding:20px;

border-radius:10px;

}}

</style>
""",
    unsafe_allow_html=True,
)


st.title("WardrobeIQ")

st.caption("Upload clothing • Organize your wardrobe • Build outfits")

uploaded = st.file_uploader(
    "Upload garments",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
)

if "processed_files" not in st.session_state:
    st.session_state.processed_files = set()

if uploaded:
    new_files = [f for f in uploaded if f.name not in st.session_state.processed_files]

    if new_files:
        with st.spinner("Analyzing garments..."):
            for file in new_files:
                classify_and_add(file)
                st.session_state.processed_files.add(file.name)

groups = group_items()

if len(st.session_state.closet) == 0:
    st.info("Your closet is empty. Upload some clothing photos to begin.")

else:
    st.header("Your Closet")

    for color_name in sorted(groups.keys()):
        sample = groups[color_name][0]

        st.markdown("---")

        c1, c2 = st.columns([1, 12])

        with c1:
            st.markdown(
                color_circle(sample["rgb"]),
                unsafe_allow_html=True,
            )

        with c2:
            st.subheader(f"{color_name.title()} ({len(groups[color_name])})")

        cols = st.columns(4)

        for index, item in enumerate(groups[color_name]):
            with cols[index % 4]:
                if item["image"] is not None:
                    st.image(
                        item["image"],
                        use_container_width=True,
                    )

                else:
                    st.info("Image unavailable")

                st.caption(f"{item['colorName']} • {item['category']}")

                category = st.selectbox(
                    "Category",
                    CATEGORIES,
                    index=CATEGORIES.index(item["category"]),
                    key=f"cat_{item['id']}",
                )

                if category != item["category"]:
                    update_item(
                        item["id"],
                        "category",
                        category,
                    )

                color_names = [c[0] for c in NAMED_COLORS]

                selected_color = st.selectbox(
                    "Color",
                    color_names,
                    index=color_names.index(item["colorName"]),
                    key=f"color_{item['id']}",
                )

                if selected_color != item["colorName"]:
                    update_item(
                        item["id"],
                        "colorName",
                        selected_color,
                    )

                    rgb = dict(NAMED_COLORS)[selected_color]

                    update_item(
                        item["id"],
                        "rgb",
                        rgb,
                    )

                tags = st.multiselect(
                    "Style Tags",
                    STYLE_TAGS,
                    default=item["styleTags"],
                    key=f"tags_{item['id']}",
                )

                if tags != item["styleTags"]:
                    update_item(
                        item["id"],
                        "styleTags",
                        tags,
                    )

                if st.button(
                    "Remove",
                    key=f"remove_{item['id']}",
                    use_container_width=True,
                ):
                    remove_item(item["id"])

                    st.rerun()

st.markdown("---")

st.header("✨ Ask the Stylist")

prompt = st.text_input(
    "Describe your outfit",
    value=st.session_state.prompt,
    placeholder="e.g. casual summer brunch outfit",
)

st.session_state.prompt = prompt


if st.button(
    "Suggest Outfit",
    use_container_width=True,
):
    outfit, missing = suggest_outfit(
        st.session_state.closet,
        prompt,
    )

    st.session_state.outfit = outfit

    st.session_state.shopping = build_shopping_list(
        missing,
        prompt,
    )


if st.session_state.outfit:
    st.subheader("Recommended Outfit")

    cols = st.columns(5)

    for i, (role, item) in enumerate(st.session_state.outfit.items()):
        with cols[i % 5]:
            if item["image"] is not None:
                st.image(
                    item["image"],
                    use_container_width=True,
                )

            else:
                st.info("Image unavailable")

            st.markdown(f"**{role.title()}**")

            st.caption(f"{item['colorName']} • {item['category']}")

            if item["styleTags"]:
                st.write(", ".join(item["styleTags"]))


elif prompt:
    st.info("Nothing matched your request.")

if st.session_state.shopping:
    st.markdown("---")

    st.subheader("🛍 Missing From Your Closet")

    for item in st.session_state.shopping:
        st.markdown(
            f"""
### {item["category"].title()}

[Search on Amazon]({item["url"]})
"""
        )

st.markdown("---")

st.header("Closet Statistics")

left, right = st.columns(2)

with left:
    st.metric(
        "Total Items",
        len(st.session_state.closet),
    )

with right:
    colors = len(group_items())

    st.metric(
        "Colors",
        colors,
    )

# ===========================
# Sidebar
# ===========================

with st.sidebar:
    st.title("WardrobeIQ")

    st.write(f"Items: {len(st.session_state.closet)}")

    st.write(f"Colors: {len(group_items())}")

    st.divider()

    export_data = []

    for item in st.session_state.closet:
        export_data.append(
            {
                "id": item["id"],
                "rgb": item["rgb"],
                "colorName": item["colorName"],
                "category": item["category"],
                "styleTags": item["styleTags"],
            }
        )

    st.download_button(
        label="Export Closet",
        data=json.dumps(export_data, indent=4),
        file_name="closet.json",
        mime="application/json",
        use_container_width=True,
    )

    uploaded_json = st.file_uploader(
        "Import Closet",
        type=["json"],
        key="json_import",
    )

    if uploaded_json is not None:
        try:
            imported = json.load(uploaded_json)

            if isinstance(imported, list):
                for entry in imported:
                    entry["image"] = None

                st.session_state.closet = imported

                save()

                st.success("Closet imported.")

        except Exception as e:
            st.error(str(e))
