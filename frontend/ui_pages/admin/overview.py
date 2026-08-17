import streamlit as st

def render(api):
    st.title("Admin Overview")
    st.markdown("<div class='kicker'>Platform health, knowledge base and administration activity.</div>", unsafe_allow_html=True)

    try:
        docs = api.documents()
        admins = api.admins()
        team = api.team()
        recs = api.recommendations()
    except Exception as exc:
        st.error(str(exc))
        return

    cols = st.columns(4)
    cols[0].metric("Knowledge documents", len(docs))
    cols[1].metric("Administrators", len(admins))
    cols[2].metric("Team members", len(team))
    cols[3].metric("Recommendations", len(recs))

    st.markdown('<div class="section"><div class="section-label">Knowledge base</div></div>', unsafe_allow_html=True)
    indexed = sum(d.get("chunk_count", 0) for d in docs)
    st.metric("Indexed chunks", f"{indexed:,}")

    if docs:
        st.dataframe(
            [{"Document": d["filename"], "Type": d["file_type"].upper(), "Chunks": d["chunk_count"], "Status": d["status"]} for d in docs],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("Upload documents from the Documents page to build the RAG knowledge base.")
