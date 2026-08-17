import streamlit as st

def render_login(api):
    st.markdown("<div style='height:8vh'></div>", unsafe_allow_html=True)
    left, center, right = st.columns([1, 1.3, 1])

    with center:
        st.markdown("""
        <div class="hero" style="padding:36px;">
            <div class="eyebrow">SECURE ACCESS</div>
            <h1>AI Workforce Assistant</h1>
            <p>Sign in to access the project intelligence workspace and administration tools.</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login"):
            email = st.text_input("Email", placeholder="admin@company.com")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Sign in", type="primary", use_container_width=True)

        if submitted:
            if not email or not password:
                st.error("Enter both email and password.")
                return
            try:
                result = api.login(email, password)
                st.session_state.token = result["access_token"]
                api.token = result["access_token"]
                st.session_state.user = api.me()
                st.session_state.page = "Home"
                st.rerun()
            except Exception as exc:
                st.error(str(exc))

        st.markdown(
            "<div class='footer'>Administrator access only · admin@ai.com</div>",
            unsafe_allow_html=True
        )
