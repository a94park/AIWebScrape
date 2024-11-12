import streamlit as st
from scrape2 import (scrape_website, 
                    extract_body_content, 
                    clean_body_content,
                    split_dom_content)
from parse import parse_with_ollama

st. title("AI Web Scraper")
url = st.text_input("Enter a Website URL: ")

# Initialize session state to avoid missing attributes in reload
if "dom_content" not in st.session_state:
    st.session_state.dom_content = None
    print("no dom content")

if st.button("Scrape Site"):
    with st.spinner("Scraping the website"):
        try:
            result = scrape_website(url)
            body_content = extract_body_content(result)
            cleaned_content = clean_body_content(body_content)

            st.session_state.dom_content = cleaned_content

        except Exception as e:
                st.error(f"An error occurred: {e}")

if st.session_state.dom_content:
    with st.expander("View DOM Content"):
        st.text_area("DOM Content", st.session_state.dom_content, height=300)

if st.session_state.dom_content:
    parse_description = st.text_area("Describe what you want to parse")

    if st.button("Parse Content"):
        if parse_description and st.session_state.dom_content:
            with st.spinner("Parsing the content..."):
                dom_chunks = split_dom_content(st.session_state.dom_content)
                result = parse_with_ollama(dom_chunks, parse_description)
        st.write(result)