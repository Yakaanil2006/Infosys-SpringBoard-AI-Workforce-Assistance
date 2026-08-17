import streamlit as st

def render(api):
    st.title("Documents")
    st.markdown("<div class='kicker'>Control the knowledge base used by the AI Assistant.</div>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("**Upload knowledge source**")
        st.caption("Supported: PDF, DOCX, TXT and CSV. Files are extracted, chunked, embedded and indexed in Neon pgvector.")
        uploaded = st.file_uploader("Choose file", type=["pdf", "docx", "txt", "csv"], label_visibility="collapsed")
        if uploaded and st.button("Upload and index", type="primary"):
            try:
                result = api.upload_document(uploaded.name, uploaded.getvalue())
                st.success(f"Indexed {result['filename']} · {result['chunks']} chunks")
                st.rerun()
            except Exception as exc:
                st.error(str(exc))

    st.markdown('<div class="section"><div class="section-label">Knowledge sources</div></div>', unsafe_allow_html=True)
    try:
        docs = api.documents()
        if not docs:
            st.info("No documents indexed yet.")
            return
        for doc in docs:
            with st.container(border=True):
                c1, c2, c3, c4 = st.columns([4, 1, 1, 1])
                c1.markdown(f"**{doc['filename']}**")
                c2.caption(doc["file_type"].upper())
                c3.caption(f"{doc['chunk_count']} chunks")
                if c4.button("Delete", key=f"delete_doc_{doc['id']}"):
                    api.delete_document(doc["id"])
                    st.rerun()
    except Exception as exc:
        st.error(str(exc))
