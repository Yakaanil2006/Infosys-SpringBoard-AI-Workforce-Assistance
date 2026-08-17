import streamlit as st

SUGGESTIONS = [
    "What is the project architecture?",
    "What technologies are being used?",
    "Summarize the project documentation.",
    "What are the major findings from the dataset?",
    "What recommendations can be made?",
    "Explain the RAG pipeline.",
]

def render(api):
    st.title("AI Assistant")
    st.markdown("<div class='kicker'>Project-grounded answers powered by retrieval-augmented generation.</div>", unsafe_allow_html=True)

    st.markdown('<div class="section"><div class="section-label">Suggested questions</div></div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, question in enumerate(SUGGESTIONS):
        with cols[i % 3]:
            if st.button(question, key=f"suggestion_{i}", use_container_width=True):
                st.session_state.pending_question = question

    st.markdown('<div class="section"><div class="section-label">Conversation</div></div>', unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if not st.session_state.messages:
        st.markdown("""
        <div class="card">
            <div class="card-title">Ask the project knowledge base</div>
            <div class="card-copy">
                Your question is embedded, matched against the top relevant document chunks
                in Neon pgvector, and then answered by Groq using that context.
            </div>
        </div>
        """, unsafe_allow_html=True)

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("sources"):
                st.markdown(
                    "<div class='source'><b>Sources:</b> " +
                    " · ".join(msg["sources"]) +
                    "</div>",
                    unsafe_allow_html=True,
                )

    question = st.chat_input("Ask about the project, documents or data...")
    question = question or st.session_state.pop("pending_question", None)

    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Retrieving context and generating answer..."):
                try:
                    result = api.chat(question)
                    answer = result["answer"]
                    source_names = [
                        f"{s['filename']}" + (f" · p.{s['page']}" if s.get("page") else "")
                        for s in result.get("sources", [])
                    ]
                except Exception as exc:
                    answer = f"Unable to answer: {exc}"
                    source_names = []
            st.markdown(answer)
            if source_names:
                st.markdown(
                    "<div class='source'><b>Sources:</b> " +
                    " · ".join(source_names) +
                    "</div>",
                    unsafe_allow_html=True,
                )

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "sources": source_names,
        })
