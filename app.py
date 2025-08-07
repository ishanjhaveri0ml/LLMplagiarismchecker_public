import streamlit as st
from doc_reader import extract_text_from_pdf, extract_text_from_docx, chunk_text
from scraper import search_duckduckgo, scrape_text_from_url
from vector_store import create_index, search_similar
from rag_explainer import explain_similarity

st.set_page_config(page_title="LLM-Powered Plagiarism Checker", layout="wide")
st.title("LLM-Powered Plagiarism Checker")

uploaded_file = st.file_uploader("Upload a PDF or DOCX file", type=["pdf", "docx"])
user_chunks = []

if uploaded_file:
    try:
        if uploaded_file.name.lower().endswith(".pdf"):
            user_text = extract_text_from_pdf(uploaded_file)
        else:
            user_text = extract_text_from_docx(uploaded_file)
    except Exception as e:
        st.error(f"Failed to extract text: {e}")
        st.stop()

    user_chunks = chunk_text(user_text)
    st.success(f"Extracted and chunked into {len(user_chunks)} parts.")

if user_chunks:
    st.subheader("Search for Similar Web Content")
    query = st.text_input("Topic of the document:", placeholder="e.g., climate change, stock market trends")
    if query:
        if st.button("Check for Plagiarism"):
            with st.spinner("Searching and scraping..."):
                try:
                    urls = search_duckduckgo(query)
                    scraped_texts = [scrape_text_from_url(url) for url in urls]
                    web_chunks = []
                    for text in scraped_texts:
                        web_chunks.extend(chunk_text(text))
                except Exception as e:
                    st.error(f"Web search or scraping failed: {e}")
                    st.stop()

            if not web_chunks:
                st.error("No web content found for the given query.")
                st.stop()
            st.success(f"Scraped and chunked {len(web_chunks)} web content pieces.")

            st.subheader("Similarity Analysis")
            try:
                index, _ = create_index(web_chunks)
                matches = search_similar(user_chunks, web_chunks, index)
            except Exception as e:
                st.error(f"Similarity analysis failed: {e}")
                st.stop()

            for i, (chunk, top_matches) in enumerate(matches):
                st.markdown(f"### User Chunk {i+1}")
                st.text_area("User Text", chunk, height=100)
                for match_text, distance in top_matches:
                    st.markdown(f"**Similarity Score:** {1 - distance:.2f}")
                    with st.expander("Web Match and Explanation"):
                        st.text_area("Matched Web Text", match_text, height=100)
                        try:
                            explanation = explain_similarity(chunk, match_text)
                            st.markdown(f"Explanation:\n\n{explanation}")
                        except Exception as e:
                            st.warning(f"Explanation generation failed: {e}")
