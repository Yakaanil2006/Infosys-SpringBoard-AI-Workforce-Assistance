import os

import streamlit as st
from dotenv import load_dotenv

from services.api_client import APIClient
from utils.session import clear_session, is_authenticated, is_admin


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000",
)


# ============================================================
# STREAMLIT CONFIG
# ============================================================

st.set_page_config(
    page_title="AI-Powered Workforce Analytics & Talent Intelligence Dashboard",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# SESSION STATE
# ============================================================

if "token" not in st.session_state:
    st.session_state.token = None

if "user" not in st.session_state:
    st.session_state.user = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "page" not in st.session_state:
    st.session_state.page = "Home"


# ============================================================
# API CLIENT
# ============================================================

api = APIClient(
    API_BASE_URL,
    st.session_state.token,
)


# ============================================================
# GLOBAL UI / THEME
# ============================================================

st.markdown(
    """
<style>

/* =========================================================
   FONT
   ========================================================= */

@import url(
    'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap'
);

html,
body,
[class*="css"] {
    font-family: "Inter", sans-serif !important;
}


/* =========================================================
   GLOBAL APP
   ========================================================= */

.stApp {
    background: #F5F7FA !important;
    color: #101828 !important;
}

.main {
    background: #F5F7FA !important;
}

.block-container {
    max-width: 1440px !important;
    padding: 28px 42px 56px !important;
}


/* =========================================================
   GLOBAL TEXT
   ========================================================= */

.stApp p,
.stApp label,
.stApp span,
.stApp [data-testid="stMarkdownContainer"] p {
    color: #101828 !important;
}

h1,
h2,
h3,
h4,
h5,
h6 {
    color: #101828 !important;
    letter-spacing: -0.025em;
}

h1 {
    font-size: 2.15rem !important;
}

h2 {
    font-size: 1.35rem !important;
}

h3 {
    font-size: 1.02rem !important;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

[data-testid="stSidebar"] {
    background: #111827 !important;
    border-right: 1px solid #1F2937 !important;
}

[data-testid="stSidebar"] * {
    color: #E5E7EB !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color: #E5E7EB !important;
}


/* Sidebar navigation */

[data-testid="stSidebar"] .stRadio label {
    padding: 9px 10px !important;
    border-left: 2px solid transparent !important;
    border-radius: 4px !important;
    transition: all 0.15s ease;
}

[data-testid="stSidebar"] .stRadio label:hover {
    background: #1F2937 !important;
    border-left-color: #60A5FA !important;
}

[data-testid="stSidebar"] .stRadio label p {
    color: #F9FAFB !important;
}


/* Sidebar radio circle */

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
    color: #F9FAFB !important;
}


/* Sidebar caption */

[data-testid="stSidebar"] .stCaption,
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    color: #98A2B3 !important;
}


/* =========================================================
   BRAND
   ========================================================= */

.awa-brand {
    padding: 6px 4px 20px;
}

.awa-brand-mark {
    display: inline-flex;
    width: 36px;
    height: 36px;
    align-items: center;
    justify-content: center;
    background: #2563EB;
    color: #FFFFFF !important;
    font-weight: 700;
    margin-right: 9px;
    border-radius: 2px;
}

.awa-brand-title {
    font-size: 16px;
    font-weight: 700;
    color: #FFFFFF !important;
    vertical-align: middle;
}

.awa-brand-sub {
    color: #98A2B3 !important;
    font-size: 11px;
    margin: 6px 0 0 45px;
    letter-spacing: 0.03em;
}


/* =========================================================
   BUTTONS
   ========================================================= */

.stButton > button,
.stDownloadButton > button {
    background: #FFFFFF !important;
    color: #101828 !important;
    border: 1px solid #D0D5DD !important;
    border-radius: 4px !important;
    font-weight: 600 !important;
    min-height: 42px !important;
    box-shadow: none !important;
}

.stButton > button p,
.stButton > button span,
.stDownloadButton > button p,
.stDownloadButton > button span {
    color: #101828 !important;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background: #EFF6FF !important;
    color: #101828 !important;
    border-color: #2563EB !important;
}

.stButton > button:focus,
.stButton > button:active {
    color: #101828 !important;
    border-color: #2563EB !important;
}


/* =========================================================
   PRIMARY BUTTON
   ========================================================= */

.stButton > button[kind="primary"],
button[kind="primary"] {
    background: #175CD3 !important;
    color: #FFFFFF !important;
    border-color: #175CD3 !important;
}

.stButton > button[kind="primary"] p,
.stButton > button[kind="primary"] span,
button[kind="primary"] p,
button[kind="primary"] span {
    color: #FFFFFF !important;
}

.stButton > button[kind="primary"]:hover {
    background: #124DA6 !important;
    border-color: #124DA6 !important;
}


/* =========================================================
   SUGGESTED QUESTIONS
   ========================================================= */

div[data-testid="stHorizontalBlock"] .stButton > button {
    background: #FFFFFF !important;
    color: #101828 !important;
    border: 1px solid #D0D5DD !important;
    min-height: 48px !important;
    text-align: left !important;
}

div[data-testid="stHorizontalBlock"] .stButton > button p,
div[data-testid="stHorizontalBlock"] .stButton > button span {
    color: #101828 !important;
}

div[data-testid="stHorizontalBlock"] .stButton > button:hover {
    background: #EFF6FF !important;
    color: #101828 !important;
    border-color: #2563EB !important;
}


/* =========================================================
   TEXT INPUT
   ========================================================= */

.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    background: #FFFFFF !important;
    color: #101828 !important;
    border: 1px solid #D0D5DD !important;
    border-radius: 4px !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #667085 !important;
    opacity: 1 !important;
}

.stTextInput label,
.stTextArea label,
.stNumberInput label {
    color: #344054 !important;
    font-weight: 600 !important;
}


/* =========================================================
   SELECTBOX
   ========================================================= */

.stSelectbox label,
.stMultiSelect label {
    color: #344054 !important;
    font-weight: 600 !important;
}

.stSelectbox [data-baseweb="select"] > div,
.stMultiSelect [data-baseweb="select"] > div {
    background: #FFFFFF !important;
    color: #101828 !important;
    border-color: #D0D5DD !important;
}

.stSelectbox [data-baseweb="select"] span,
.stMultiSelect [data-baseweb="select"] span {
    color: #101828 !important;
}

.stSelectbox [data-baseweb="select"] input,
.stMultiSelect [data-baseweb="select"] input {
    color: #101828 !important;
}


/* Dropdown */

div[role="listbox"] {
    background: #FFFFFF !important;
}

div[role="option"] {
    background: #FFFFFF !important;
    color: #101828 !important;
}

div[role="option"]:hover {
    background: #EFF6FF !important;
    color: #101828 !important;
}


/* =========================================================
   NUMBER INPUT
   ========================================================= */

.stNumberInput button {
    color: #344054 !important;
    background: #FFFFFF !important;
    border-color: #D0D5DD !important;
}


/* =========================================================
   FILE UPLOADER
   ========================================================= */

.stFileUploader label {
    color: #344054 !important;
    font-weight: 600 !important;
}

.stFileUploader section {
    background: #FFFFFF !important;
    border: 1px dashed #98A2B3 !important;
    border-radius: 4px !important;
}

.stFileUploader section * {
    color: #344054 !important;
}

.stFileUploader section button {
    background: #FFFFFF !important;
    color: #101828 !important;
    border: 1px solid #D0D5DD !important;
}


/* =========================================================
   METRICS
   ========================================================= */

div[data-testid="stMetric"] {
    background: #FFFFFF !important;
    border: 1px solid #E4E7EC !important;
    border-radius: 4px !important;
    padding: 16px !important;
}

div[data-testid="stMetricLabel"] {
    color: #667085 !important;
}

div[data-testid="stMetricLabel"] p {
    color: #667085 !important;
}

div[data-testid="stMetricValue"] {
    color: #101828 !important;
}


/* =========================================================
   DATAFRAME
   ========================================================= */

.stDataFrame {
    border: 1px solid #E4E7EC !important;
    border-radius: 4px !important;
}


/* =========================================================
   CARDS
   ========================================================= */

.card {
    background: #FFFFFF;
    border: 1px solid #E4E7EC;
    padding: 20px;
    min-height: 145px;
    margin-bottom: 16px;
}

.card-title {
    color: #101828 !important;
    font-weight: 700;
    margin-bottom: 8px;
}

.card-copy {
    color: #667085 !important;
    line-height: 1.55;
    font-size: 13px;
}


/* =========================================================
   HERO
   ========================================================= */

.hero {
    background: #FFFFFF;
    border: 1px solid #D0D5DD;
    padding: 42px;
    margin-bottom: 24px;
}

.hero h1 {
    color: #101828 !important;
    margin: 0 0 10px;
    font-size: 36px !important;
}

.hero p {
    color: #667085 !important;
    max-width: 780px;
    font-size: 15px;
    line-height: 1.7;
}

.eyebrow {
    color: #175CD3 !important;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .08em;
    margin-bottom: 10px;
}


/* =========================================================
   SECTIONS
   ========================================================= */

.section {
    margin: 30px 0 14px;
}

.section-label {
    color: #667085 !important;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: .07em;
    text-transform: uppercase;
}

.kicker {
    color: #667085 !important;
    font-size: 13px;
}


/* =========================================================
   SOURCE / RAG CITATIONS
   ========================================================= */

.source {
    color: #475467 !important;
    background: #F9FAFB;
    border-left: 2px solid #98A2B3;
    padding: 8px 10px;
    font-size: 12px;
    margin-top: 8px;
}


/* =========================================================
   ADMIN BANNER
   ========================================================= */

.admin-banner {
    background: #0F172A;
    color: #FFFFFF !important;
    padding: 14px 18px;
    margin-bottom: 18px;
    border-left: 3px solid #60A5FA;
    font-weight: 600;
}

.admin-banner * {
    color: #FFFFFF !important;
}


/* =========================================================
   EXPANDER
   ========================================================= */

div[data-testid="stExpander"] {
    background: #FFFFFF !important;
    border: 1px solid #E4E7EC !important;
}

div[data-testid="stExpander"] summary {
    color: #101828 !important;
}


/* =========================================================
   ALERTS
   ========================================================= */

div[data-testid="stAlert"] {
    border-radius: 4px !important;
}

div[data-testid="stAlert"] * {
    color: #101828 !important;
}


/* =========================================================
   CHAT PAGE HELPERS
   ========================================================= */

.chat-page-header {
    background: #FFFFFF;
    border: 1px solid #E4E7EC;
    border-radius: 14px;
    padding: 20px 22px;
    margin-bottom: 18px;
    box-shadow: 0 2px 8px rgba(16, 24, 40, 0.04);
}

.chat-page-header h1 {
    margin: 0 !important;
    font-size: 28px !important;
}

.chat-page-header p {
    color: #667085 !important;
    margin: 4px 0 0 !important;
}

.chat-status {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 6px 10px;
    border-radius: 999px;
    background: #ECFDF3;
    color: #027A48 !important;
    border: 1px solid #ABEFC6;
    font-size: 12px;
    font-weight: 700;
}

.chat-status-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #12B76A;
}

/* =========================================================
   CHAT MESSAGES — READABLE LIGHT CHAT UI
   ========================================================= */

[data-testid="stChatMessage"] {
    background: #FFFFFF !important;
    color: #101828 !important;
    border: 1px solid #E4E7EC !important;
    border-radius: 12px !important;
    padding: 14px 18px !important;
    margin: 10px 0 !important;
    box-shadow: 0 2px 8px rgba(16, 24, 40, 0.04) !important;
}

/* Streamlit markdown can inherit the wrong color from theme/components.
   Explicitly style EVERY markdown element so lists and rich responses are
   never rendered as white text on a white background. */
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"],
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] li,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] ul,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] ol,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] span,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] div,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] strong,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] em {
    color: #101828 !important;
}

[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] ul,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] ol {
    margin-top: 8px !important;
    margin-bottom: 12px !important;
    padding-left: 24px !important;
}

[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] li {
    color: #344054 !important;
    line-height: 1.65 !important;
    margin-bottom: 5px !important;
}

[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] strong {
    color: #101828 !important;
    font-weight: 700 !important;
}

[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] a {
    color: #175CD3 !important;
    text-decoration: underline !important;
}

[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] blockquote {
    color: #475467 !important;
    background: #F9FAFB !important;
    border-left: 3px solid #98A2B3 !important;
    padding: 10px 14px !important;
    margin: 12px 0 !important;
}

[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] code {
    color: #344054 !important;
    background: #F2F4F7 !important;
    border: 1px solid #EAECF0 !important;
    border-radius: 5px !important;
    padding: 2px 5px !important;
}

[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] pre {
    background: #0F172A !important;
    border: 1px solid #1E293B !important;
    border-radius: 8px !important;
    padding: 14px !important;
    overflow-x: auto !important;
}

[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] pre code {
    color: #F8FAFC !important;
    background: transparent !important;
    border: 0 !important;
    padding: 0 !important;
}

/* Normal markdown outside chat should also remain readable. */
[data-testid="stMarkdownContainer"] ul,
[data-testid="stMarkdownContainer"] ol,
[data-testid="stMarkdownContainer"] li {
    color: #101828 !important;
}


/* =========================================================
   CHAT INPUT
   ========================================================= */

/* Clean white chat composer — avoids the old dark footer look. */
[data-testid="stChatInput"] {
    background: transparent !important;
    padding-top: 10px !important;
}

[data-testid="stChatInput"] > div {
    background: #FFFFFF !important;
    border: 1px solid #D0D5DD !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 14px rgba(16, 24, 40, 0.06) !important;
}

[data-testid="stChatInput"] textarea {
    background: #FFFFFF !important;
    color: #101828 !important;
    border: 0 !important;
    border-radius: 12px !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #667085 !important;
    opacity: 1 !important;
}

[data-testid="stChatInput"] label {
    color: #E5E7EB !important;
}


/* =========================================================
   CAPTIONS
   ========================================================= */

.stCaption,
[data-testid="stCaptionContainer"] {
    color: #667085 !important;
}


/* =========================================================
   LINKS
   ========================================================= */

a {
    color: #2563EB !important;
}


/* =========================================================
   DIVIDERS
   ========================================================= */

hr {
    border-color: #E4E7EC !important;
}


/* =========================================================
   FOOTER
   ========================================================= */

.footer {
    color: #98A2B3 !important;
    border-top: 1px solid #E4E7EC;
    padding-top: 18px;
    margin-top: 48px;
    font-size: 12px;
}


/* =========================================================
   MOBILE / SMALL SCREEN
   ========================================================= */

@media (max-width: 900px) {

    .block-container {
        padding: 20px 18px 40px !important;
    }

    .hero {
        padding: 28px;
    }

    .hero h1 {
        font-size: 28px !important;
    }

}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# AUTHENTICATION
# ============================================================

if not is_authenticated():
    from ui_pages.login import render_login

    render_login(api)
    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    # --------------------------------------------------------
    # BRAND
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="awa-brand">
            <span class="awa-brand-mark">◈</span>
            <span class="awa-brand-title">AI Workforce</span>
            <div class="awa-brand-sub">
                INTELLIGENCE PLATFORM
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    # --------------------------------------------------------
    # WORKSPACE
    # --------------------------------------------------------

    st.caption("WORKSPACE")

    public_pages = [
        ("Home", "Home"),
        ("AI Assistant", "AI Assistant"),
        ("Power BI", "Power BI"),
        ("Data Viewer", "Data Viewer"),
    ]

    # --------------------------------------------------------
    # ADMINISTRATION
    # --------------------------------------------------------

    if is_admin():

        st.caption("ADMINISTRATION")

        public_pages += [
            ("Admin Overview", "Admin Overview"),
            ("Admin Management", "Admin Management"),
            ("Team Members", "Team Members"),
            ("Documents", "Documents"),
            ("Power BI Settings", "Power BI Settings"),
            ("Recommendations", "Recommendations"),
        ]

    # --------------------------------------------------------
    # NAVIGATION
    # --------------------------------------------------------

    current = st.session_state.page

    labels = [
        item[0]
        for item in public_pages
    ]

    selected = st.radio(
        "Navigation",
        labels,
        index=(
            labels.index(current)
            if current in labels
            else 0
        ),
        label_visibility="collapsed",
    )

    st.session_state.page = selected

    st.divider()

    # --------------------------------------------------------
    # USER PROFILE
    # --------------------------------------------------------

    user = st.session_state.get("user") or {}

    user_name = user.get(
        "name",
        "Admin",
    )

    user_email = user.get(
        "email",
        "",
    )

    st.markdown(
        f"""
        <div style="
            color:#FFFFFF;
            font-size:15px;
            font-weight:700;
            margin-bottom:4px;
        ">
            {user_name}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption(user_email)

    # --------------------------------------------------------
    # SIGN OUT
    # --------------------------------------------------------

    if st.button(
        "Sign out",
        use_container_width=True,
    ):
        clear_session()
        st.rerun()


# ============================================================
# PAGE ROUTING
# ============================================================

page_map = {
    label: value
    for label, value in public_pages
}

selected_page = page_map[selected]


# ============================================================
# ADMIN PROTECTED BANNER
# ============================================================

admin_pages = {
    "Admin Overview",
    "Admin Management",
    "Team Members",
    "Documents",
    "Power BI Settings",
    "Recommendations",
}

if is_admin() and selected_page in admin_pages:

    st.markdown(
        """
        <div class="admin-banner">
            ADMIN CONTROL CENTER
            &nbsp;&nbsp;/&nbsp;&nbsp;
            Protected workspace
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# PAGE IMPORTS
# ============================================================

if selected_page == "Home":

    from ui_pages.home import render

elif selected_page == "AI Assistant":

    from ui_pages.assistant import render

elif selected_page == "Power BI":

    from ui_pages.powerbi import render

elif selected_page == "Data Viewer":

    from ui_pages.data_viewer import render

elif selected_page == "Admin Overview":

    from ui_pages.admin.overview import render

elif selected_page == "Admin Management":

    from ui_pages.admin.admins import render

elif selected_page == "Team Members":

    from ui_pages.admin.team import render

elif selected_page == "Documents":

    from ui_pages.admin.documents import render

elif selected_page == "Power BI Settings":

    from ui_pages.admin.powerbi import render

elif selected_page == "Recommendations":

    from ui_pages.admin.recommendations import render


# ============================================================
# RENDER SELECTED PAGE
# ============================================================

render(api)