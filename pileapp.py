import streamlit as st
import feedparser
from datetime import datetime
from urllib.parse import urlparse
import smtplib
from email.mime.text import MIMEText
from keybert import KeyBERT
import re
from collections import defaultdict
import hashlib


# ---------------- CONFIG ---------------- #
st.set_page_config(page_title="Pile", layout="wide")
st.title("🗂️ Pile")
st.caption("Curated, summarized, and categorized insights — neatly piled for you.")
st.caption(f"🔁 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# ---------------- FEEDS ---------------- #
FEEDS = {
    "Leadership": [
        "http://feeds.harvardbusiness.org/harvardbusiness/",
        "https://sloanreview.mit.edu/feed/",
        "https://chiefexecutive.net/feed/",
        "https://feeds.feedburner.com/StrategyBusiness-ThoughtLeaders",
    ],
    "Organizational Behavior": [
        "https://www.forbes.com/leadership/feed/",
        "https://www.businessnewsdaily.com/feed",
        "https://www.fastcompany.com/rss",
        "https://knowledge.wharton.upenn.edu/category/leadership-management/feed/",
        "https://www.management-issues.com/rss/"
    ],
    "Change Management": [
        "https://www.cio.com/index.rss",
        "https://www.torbenrick.eu/blog/feed/",
        "https://www.strategicmanagementinsight.com/feed/",
        "https://www.prosci.com/resources/articles/rss",
        "https://www.strategy-business.com/rss"
    ],
    "Auditing": [
        "https://www.journalofaccountancy.com/news/feed/",
        "https://www.cpajournal.com/feed/",
        "https://www.accountingtoday.com/feed",
        "https://feeds.feedburner.com/WoltersKluwerAccountingAudit",
        "https://www2.deloitte.com/rss.xml"
    ],
    "Consumer Behavior": [
        "https://www.marketingdive.com/feeds/news/",
        "https://www.marketingweek.com/feed/",
        "https://www.smartinsights.com/feed/",
        "https://blog.hubspot.com/marketing/rss.xml",
        "https://www.adweek.com/feed/"
    ],
    "Performance Management": [
        "https://www.business2community.com/performance-management/feed",
        "https://www.bersin.com/feed",
        "https://www.management-issues.com/rss/",
        "https://www.peoplematters.in/rss.xml",
        "https://www.hrtechnologist.com/rss.xml"
    ],
    "Work Culture": [
        "https://www.benefitnews.com/feed",
        "https://blog.bonus.ly/rss.xml",
        "https://www.tlnt.com/feed/",
        "https://www.glassdoor.com/blog/feed/",
        "https://www.workhuman.com/blog/feed/"
    ],
    "Campus Technology": [
        "https://campustechnology.com/rss-feeds/breaking-news.aspx",
        "https://edtechmagazine.com/higher/rss.xml",
        "https://www.ecampusnews.com/feed/",
        "https://www.chronicle.com/section/Technology/30/feed",
        "https://feeds.feedburner.com/edudemic"
    ]
}

CATEGORY_EMOJIS = {
    "Leadership": "🧑‍💼",
    "Organizational Behavior": "🧠",
    "Change Management": "🔄",
    "Auditing": "📊",
    "Consumer Behavior": "🛍️",
    "Performance Management": "📈",
    "Work Culture": "🏢",
    "Campus Technology": "💻"
}


# ---------------- MODELS ---------------- #
from sentence_transformers import SentenceTransformer

# Load sentence-transformer model on CPU and pass to KeyBERT
# embedding_model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
# kw_model = KeyBERT(model=embedding_model)
selected_articles = []

# ---------------- SIDEBAR EMAIL ---------------- #
st.sidebar.header("📬 Send Selected Articles")
recipient_email = st.sidebar.text_input("Enter your email address")
send_button = st.sidebar.button("Send Email")

# ---------------- HELPERS ---------------- #
def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    return re.sub(cleanr, '', raw_html)

def format_date(entry):
    try:
        return datetime(*entry.published_parsed[:6])
    except:
        try:
            return datetime(*entry.updated_parsed[:6])
        except:
            return None

def extract_keywords(text):
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=5)
    return [kw[0] for kw in keywords]

def summarize_text(text):
    return text[:300]  # Clean summary (no prefix)

def send_email(to_email, selected_articles):
    msg_content = ""
    for art in selected_articles:
        short_summary = art['summary'][:500] + "..." if len(art['summary']) > 500 else art['summary']
        msg_content += f"<h3><a href='{art['link']}'>{art['title']}</a></h3>"
        msg_content += f"<p><i>{art['source']} – {art['date']}</i></p>"
        msg_content += f"<p>{short_summary}</p>"
        msg_content += f"<p><b>Keywords</b>: {', '.join(art['keywords'])}</p><hr>"
    msg = MIMEText(msg_content, 'html')
    msg['Subject'] = 'Your Selected Journal Abstracts'
    msg['From'] = st.secrets["smtp_user"]
    msg['To'] = to_email

    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = st.secrets["smtp_user"]
    smtp_pass = st.secrets["smtp_pass"]

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(msg['From'], [msg['To']], msg.as_string())

# ---------------- FETCH ARTICLES ---------------- #
grouped_articles = defaultdict(lambda: defaultdict(list))

with st.spinner("🔍 Fetching and categorizing articles..."):
    for category, urls in FEEDS.items():
        for feed_url in urls:
            feed = feedparser.parse(feed_url)
            source = urlparse(feed.href).netloc.replace("www.", "")
            #st.sidebar.text(f"{category} | {source}: {len(feed.entries)} entries")

            for entry in feed.entries:
                published = format_date(entry)
                if not published:
                    continue
                content = clean_html(entry.get("summary", ""))
                grouped_articles[category][source].append({
                    "category": category,
                    "source": source,
                    "title": entry.title,
                    "link": entry.link,
                    "published": published,
                    "content": content
                })

    # Sort + keep only top 5 per journal
    for cat in grouped_articles:
        for journal in grouped_articles[cat]:
            grouped_articles[cat][journal].sort(key=lambda x: x["published"], reverse=True)
            grouped_articles[cat][journal] = grouped_articles[cat][journal][:5]

from itertools import count
import hashlib

key_counter = count()

for category in grouped_articles:
    emoji = CATEGORY_EMOJIS.get(category, "📘")
    with st.expander(f"{emoji} {category}", expanded=False):
        st.markdown("**Select Journals to View:**")
        selected_journals = {}
        
        # Generate toggles
        for journal in sorted(grouped_articles[category].keys()):
            toggle_key = f"{category}-{journal}-toggle"
            selected_journals[journal] = st.checkbox(f"📰 {journal}", key=toggle_key, value=True)
        
        for journal, show in selected_journals.items():
            if show:
                st.subheader(f"📰 {journal}")
                for art in grouped_articles[category][journal]:
                    raw_key = f"{art['title']}{art['link']}{art['published']}{art['content']}"
                    unique_hash = hashlib.md5(raw_key.encode()).hexdigest()
                    key = f"{unique_hash}-{next(key_counter)}"

                    summary = summarize_text(art["content"])
                    # keywords = extract_keywords(art["content"])
                    art["summary"] = summary
                    art["keywords"] = keywords
                    art["date"] = art["published"].strftime("%Y-%m-%d")

                    if st.checkbox(art["title"], key=key):
                        selected_articles.append(art)

                    st.markdown(f"*Published: {art['date']} | Source: {art['source']}*")
                    st.markdown(f"**Summary**: {summary}")
                    st.markdown("**Keywords**: " + " ".join([f"`{k}`" for k in keywords]))
                    st.markdown("---")


# ---------------- STATUS BAR ---------------- #
st.markdown("---")
st.markdown(f"✅ Loaded **{sum(len(journals) for journals in grouped_articles.values())} journals** across **{len(grouped_articles)} categories**.")
st.markdown(f"📬 You have **{len(selected_articles)} articles** selected for emailing.")


# ---------------- EMAIL HANDLER ---------------- #
if send_button:
    if not recipient_email:
        st.sidebar.error("Please enter your email address.")
    elif not selected_articles:
        st.sidebar.error("Please select at least one article.")
    else:
        try:
            send_email(recipient_email, selected_articles)
            st.sidebar.success(f"Sent {len(selected_articles)} articles to {recipient_email}")
        except Exception as e:
            st.sidebar.error(f"Error sending email: {e}")

