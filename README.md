Here’s a clean and descriptive `README.md` for your **Pile** project:

---

# 🗂️ Pile

**Pile** is a curated academic and professional journal digest app built with Streamlit. It pulls the most recent articles from 50+ journals in categories like Leadership, Change Management, and Higher Education — and presents them in a clean, searchable format with AI-generated summaries and keywords.

## Features

- Pulls and updates the 5 most recent articles per source
- Categorized into topics like Leadership, Auditing, and Campus Tech
- One-sentence summaries and extracted keywords using KeyBERT
- Users can select articles and send them to their email
- Modular structure — easy to expand with new feeds or categories

## Tech Stack

- Python 3.10+
- Streamlit
- feedparser
- KeyBERT + SentenceTransformer (MiniLM)
- SMTP (for email sending)

## Installation

1. **Clone the repo**

```bash
git clone git@github.com:grumpscat/pileapp.git
cd pileapp
```

2. **Create a virtual environment**

```bash
conda create -n pile310 python=3.10
conda activate pile310
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up email credentials**

Create a file named `.streamlit/secrets.toml`:

```toml
smtp_user = "your.email@gmail.com"
smtp_pass = "your_app_password"
```

## Run the app

```bash
streamlit run pileapp.py
```

Your browser will open automatically at [http://localhost:8501](http://localhost:8501).

## Next Steps

- Deploy to [Streamlit Cloud](https://streamlit.io/cloud)
- Add weekly email digests
- Enable search and filtering
- Enhance summarization with GPT-based summaries

## Name

“Pile” reflects the idea of a neatly stacked pile of useful, organized insights — academic and business, intelligently summarized.

---

> Built by [@grumpscat](https://github.com/grumpscat)

---

Let me know if you want me to:
- Add this directly to your repo
- Customize it for Render or Docker
- Include screenshots or badges

You ready to deploy to Streamlit Cloud next?
