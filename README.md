# 🗂️ Pile

**Pile** is a curated academic and professional journal digest app built with Streamlit. It pulls the most recent articles from 50+ journals in categories like Leadership, Change Management, and Higher Education — and presents them in a clean, searchable format with AI-generated summaries and keywords.

##  Features

-  Pulls and updates the 5 most recent articles per source
-  Categorized into topics like Leadership, Auditing, and Campus Tech
-  One-sentence summaries and extracted keywords using KeyBERT
-  Users can select articles and send them to their email
-  Modular structure — easy to expand with new feeds or categories

## Tools

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
