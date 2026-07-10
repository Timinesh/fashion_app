# WardrobeIQ

An AI-powered wardrobe manager built with Python and Streamlit.

## Features

- Upload clothing photos
- Automatic clothing classification using OpenAI Vision
- Dominant color detection
- Closet grouped by color
- Outfit recommendations
- Shopping suggestions
- Persistent local storage

## Installation

```bash
git clone <repo>

```

Create a `.env` file.

```text
OPENAI_API_KEY=your_key_here
```

Run:

```bash
streamlit run app.py
```

## Project Structure

```
ClosetAtelier/
│
├── app.py
├── classifier.py
├── image_processing.py
├── outfit_engine.py
├── database.py
├── constants.py
├── requirements.txt
├── .env
└── data/
```

## Technologies

- Python
- Streamlit
- OpenAI API
- Pillow
- NumPy
