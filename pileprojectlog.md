# 📄 Pile App Development Log - April 20, 2025

## 🚀 Project Goals

Create a Streamlit-based app named **Pile** that:
- Pulls academic, business, and education-related articles from over 50+ RSS feeds
- Categorizes them by topic (e.g. Leadership, Work Culture)
- Shows the 5 most recent articles per journal
- Uses AI to extract a 1-sentence summary and keywords
- Allows the user to select articles and email them
- Offers a clean, user-friendly UI that opens via terminal

---

## ✅ What We Did

### ✔ Core Functionality Built
- Created a Streamlit app (`pileapp.py`)
- Added 8 subject categories and over 50 RSS feeds
- Grouped articles by subject and journal
- Used `KeyBERT` with `SentenceTransformer` (MiniLM) to extract keywords
- Summarized articles by trimming raw content to 300 characters
- Built email functionality using Gmail SMTP
- Let users select articles and send them via email

### ✔ UI Improvements
- Used `st.expander()` to collapse category sections
- Let users toggle individual journals inside each category
- Automatically selected all checkboxes by default
- Used emojis per category for visual clarity
- Displayed a summary footer ("X categories", "Y selected")

---

## ⚠️ Errors and How We Fixed Them

### ❌ `ImportError: libXrender.so.1`
**Fix**: Installed missing system library in the Render environment

### ❌ `StreamlitDuplicateElementKey`
**Fix**: Created a `key_counter` + `hashlib.md5` to ensure checkbox keys were unique

### ❌ `set_page_config` can only be called once
**Fix**: Ensured `st.set_page_config(...)` was the very first Streamlit call in the script

### ❌ `OfflineModeIsEnabled` / HuggingFace errors
**Fix**: Downgraded packages to compatible versions:
- `torch==2.0.1`
- `transformers==4.31.0`
- `sentence-transformers==2.2.2`
- `huggingface_hub==0.14.1`
- `keybert==0.7.0`

### ❌ `RuntimeError: Numpy is not available`
**Fix**: Reinstalled NumPy using:
```bash
pip uninstall -y numpy
pip install numpy==1.24.4
```

### ❌ Streamlit wouldn't open browser
**Fix**: Created `~/.streamlit/config.toml` and added:
```toml
[server]
headless = false
```
Now `streamlit run pileapp.py` auto-launches the browser.

---

## 🔄 What We Changed Along the Way
- Renamed the app from "Academic Journal Digest" to **Pile**
- Added emojis and visual tweaks to headers
- Reorganized the article rendering to group by category > journal
- Refactored toggle logic for journal selection
- Trimmed summaries to 300 characters for simplicity
- Removed deprecated or noisy sidebar log messages

---

## 🚡 Recommendations / Next Steps

### ✉️ Email Improvements
- Mask `smtp_user` and `smtp_pass` using `st.secrets` or Streamlit Cloud Secrets
- Add input validation to avoid failed sends

### 🌐 Deployment
- Deploy on **Streamlit Cloud** with `requirements.txt` and `secrets.toml`
- Alternative: use **Render** for greater control

### ✨ UX/UI Enhancements
- Add search or filter bar
- Let users choose how many articles to show per journal
- Add date range filtering or keyword filtering

### 🧐 AI Enhancements
- Replace simple summary with OpenAI/GPT-based one-liner
- Cluster or tag articles by topic using embeddings

### 🏋️ Admin Features
- Add daily/weekly digest email automation
- Add analytics to track category usage

---

## 🏑 Status
**Pile** is running locally, pulling and summarizing live articles, and able to email selections. Ready for polish and deployment.


