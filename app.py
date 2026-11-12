import sqlite3
from datetime import datetime
from pathlib import Path

import requests
import streamlit as st

DB_PATH = Path(__file__).with_name("callsense.db")

st.set_page_config(page_title="CallSense AI", page_icon="🎧", layout="wide")


# ---------- DATABASE ----------
def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def init_db():
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS calls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                language TEXT,
                transcript TEXT,
                sentiment TEXT,
                intent TEXT,
                summary TEXT,
                created_at TEXT NOT NULL
            )
            """
        )


def save_call(filename, language, transcript, sentiment, intent, summary):
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO calls
            (filename, language, transcript, sentiment, intent, summary, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                filename,
                language,
                transcript,
                sentiment,
                intent,
                summary,
                datetime.now().strftime("%Y-%m-%d %H:%M"),
            ),
        )


def load_calls():
    with get_conn() as conn:
        return conn.execute(
            """
            SELECT id, filename, language, transcript, sentiment, intent, summary, created_at
            FROM calls ORDER BY id DESC
            """
        ).fetchall()


def get_stats():
    with get_conn() as conn:
        total = conn.execute("SELECT COUNT(*) FROM calls").fetchone()[0]
        positive = conn.execute(
            "SELECT COUNT(*) FROM calls WHERE lower(sentiment)='positive'"
        ).fetchone()[0]
        negative = conn.execute(
            "SELECT COUNT(*) FROM calls WHERE lower(sentiment)='negative'"
        ).fetchone()[0]
        return total, positive, negative


init_db()


# ---------- UI STYLE ----------
st.markdown(
    """
    <style>
    :root { color-scheme: light; }
    .stApp, [data-testid="stAppViewContainer"] {
        background: #f5f7fb;
        color: #172033;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2.5rem;
        max-width: 1400px;
    }
    h1, h2, h3, h4, p, label, .stMarkdown, .stCaption,
    [data-testid="stMetricLabel"], [data-testid="stMetricValue"],
    [data-testid="stMetricDelta"] {
        color: #172033 !important;
    }
    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
    [data-testid="stSidebar"] * { color: #172033 !important; }
    [data-testid="stMetric"] {
        background: #ffffff !important;
        border: 1px solid #dbe3ef !important;
        border-radius: 14px;
        padding: 18px 20px;
        box-shadow: 0 2px 8px rgba(20, 35, 60, 0.05);
    }
    [data-testid="stMetricLabel"] {
        color: #526078 !important;
        font-size: 0.9rem !important;
    }
    [data-testid="stMetricValue"] {
        color: #172033 !important;
        font-weight: 700 !important;
    }
    div[data-baseweb="input"] input,
    div[data-baseweb="textarea"] textarea {
        background: #ffffff !important;
        color: #172033 !important;
    }
    div[data-baseweb="select"] > div {
        background: #ffffff !important;
        color: #172033 !important;
    }
    [data-testid="stFileUploader"] {
        background: #ffffff;
        border: 1px dashed #9aa9bf;
        border-radius: 12px;
        padding: 12px;
    }
    [data-testid="stDataFrame"] {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
    }
    .stButton > button {
        border-radius: 9px;
        font-weight: 600;
    }
    hr { border-color: #e2e8f0 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("# 🎧 CallSense AI")
    st.caption("Multilingual Call-Center Voice Analytics")
    page = st.radio("NAVIGATION", ["Dashboard", "Analyze Call", "Call History"])
    st.divider()
    st.subheader("Colab connection")
    api_url = (
        st.text_input(
            "Colab API URL",
            placeholder="https://xxxx.ngrok-free.app",
        )
        .strip()
        .rstrip("/")
    )
    api_key = st.text_input(
        "API key",
        type="password",
        help="Paste the key printed by your Colab API cell.",
    ).strip()
    engine_label = st.selectbox(
        "Speech recognition",
        ["Whisper (multilingual)", "Wav2Vec2 (English)"],
    )
    engine = "whisper" if engine_label.startswith("Whisper") else "wav2vec2"

    if st.button("Test Colab connection", use_container_width=True):
        if not api_url:
            st.error("Enter the Colab API URL first.")
        else:
            try:
                response = requests.get(api_url + "/health", timeout=15)
                response.raise_for_status()
                st.success("Colab API is online.")
            except requests.RequestException as exc:
                st.error(f"Connection failed: {exc}")

    st.divider()
    st.caption("Mini Project • Deep Learning + NLP")


# ---------- PAGES ----------
if page == "Dashboard":
    st.title("Call Analytics Dashboard")
    st.write("Monitor customer conversations and review AI-generated insights.")

    total, positive, negative = get_stats()
    c1, c2, c3 = st.columns(3)
    c1.metric("Total calls analyzed", total)
    c2.metric("Positive calls", positive)
    c3.metric("Negative calls", negative)

    st.subheader("Recent calls")
    rows = load_calls()
    if rows:
        st.dataframe(
            [
                {
                    "ID": row[0],
                    "File": row[1],
                    "Language": row[2],
                    "Sentiment": row[4],
                    "Intent": row[5],
                    "Date": row[7],
                }
                for row in rows[:10]
            ],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No calls analyzed yet. Open Analyze Call to upload your first recording.")

    st.caption("Call results are stored locally in SQLite.")


elif page == "Analyze Call":
    st.title("Analyze a customer call")
    st.write("Upload a recording. The audio is sent to your running Google Colab model pipeline.")

    uploaded = st.file_uploader(
        "Choose an audio file",
        type=["wav", "mp3", "m4a", "ogg"],
    )

    if uploaded:
        st.audio(uploaded.getvalue())
        st.caption(f"{uploaded.name} • {uploaded.size / 1024:.1f} KB")

        if st.button("Analyze call", type="primary", use_container_width=True):
            if not api_url or not api_key:
                st.error("Enter both the Colab API URL and API key in the sidebar.")
            else:
                try:
                    with st.spinner(
                        "Sending audio to Colab. Deep-learning inference may take a few minutes..."
                    ):
                        response = requests.post(
                            api_url + "/analyze",
                            headers={"X-API-Key": api_key},
                            files={
                                "file": (
                                    uploaded.name,
                                    uploaded.getvalue(),
                                    uploaded.type or "application/octet-stream",
                                )
                            },
                            data={"engine": engine},
                            timeout=900,
                        )
                        response.raise_for_status()
                        result = response.json()

                    summary_obj = result.get("summary", {})
                    if isinstance(summary_obj, dict):
                        summary_text = "\n".join(
                            f"{key.replace('_', ' ').title()}: {value}"
                            for key, value in summary_obj.items()
                        )
                    else:
                        summary_text = str(summary_obj)

                    transcript = (
                        result.get("transcript_redacted")
                        or result.get("transcript", "")
                    )
                    save_call(
                        uploaded.name,
                        result.get("language", "Unknown"),
                        transcript,
                        result.get("sentiment", "Unknown"),
                        result.get("intent", "Unknown"),
                        summary_text,
                    )
                    st.session_state["latest_result"] = result
                    st.success("Analysis completed. Results saved to SQLite.")

                except requests.Timeout:
                    st.error(
                        "The request timed out. Colab may still be processing; "
                        "check that the Colab runtime is active and try a shorter recording."
                    )
                except requests.RequestException as exc:
                    detail = ""
                    if getattr(exc, "response", None) is not None:
                        detail = f" Server response: {exc.response.text[:500]}"
                    st.error(f"Could not analyze the recording: {exc}.{detail}")
                except ValueError as exc:
                    st.error(f"The API returned an invalid response: {exc}")

    result = st.session_state.get("latest_result")
    if result:
        st.divider()
        st.subheader("Analysis results")

        sentiment = str(result.get("sentiment", "Unknown")).upper()
        risk = result.get("risk_score", "N/A")
        risk_level = result.get("risk_level", "Unknown")

        a, b, c, d = st.columns(4)
        a.metric("Sentiment", sentiment)
        b.metric("Intent", result.get("intent", "Unknown"))
        c.metric("Risk score", risk)
        d.metric("Risk level", risk_level)

        if result.get("ESCALATION_FLAG"):
            st.error("Escalation flag: this call may need supervisor review.")
        else:
            st.success("No escalation flag raised by the model pipeline.")

        st.markdown("#### Transcript")
        st.text_area(
            "Transcript (PII-redacted when available)",
            result.get("transcript_redacted") or result.get("transcript", ""),
            height=150,
        )

        st.markdown("#### Structured call summary")
        summary = result.get("summary", {})
        if isinstance(summary, dict):
            for key, label in [
                ("issue", "Customer issue"),
                ("agent_action", "Agent response"),
                ("outcome", "Outcome"),
                ("one_line", "One-line summary"),
            ]:
                if summary.get(key):
                    st.write(f"**{label}:** {summary[key]}")
        else:
            st.info(str(summary))

        with st.expander("More model insights"):
            st.write("**Detected language:**", result.get("language", "Not returned"))
            st.write("**Voice emotion:**", result.get("voice_emotion", {}))
            st.write("**Sentiment scores:**", result.get("sentiment_scores", {}))
            st.write("**Call metrics:**", result.get("call_metrics", {}))
            st.write("**Intent confidence:**", result.get("intent_confidence", "Not returned"))
            st.write(
                "**Escalating sentiment:**",
                result.get("escalating_sentiment", "Not returned"),
            )


elif page == "Call History":
    st.title("Call history")
    st.write("Previously analyzed calls saved in your local SQLite database.")

    rows = load_calls()
    if not rows:
        st.info("No saved calls yet.")
    else:
        for row in rows:
            with st.expander(f"#{row[0]} • {row[1]} • {row[7]}"):
                st.write(f"**Language:** {row[2]}")
                st.write(f"**Sentiment:** {row[4]}")
                st.write(f"**Intent:** {row[5]}")
                st.write("**Transcript:**")
                st.write(row[3])
                st.write("**Summary:**")
                st.write(row[6])
