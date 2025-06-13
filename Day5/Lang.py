import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable

# 👉 FIXED Google Gemini API Key (Replace with your actual key)
GOOGLE_API_KEY = "AIzaSyCvWgaZSSKd1VN272jb6FWOUlP4ecyZk_8"  # 👈 Replace this!

# Initialize the Gemini model
def load_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=GOOGLE_API_KEY,
        temperature=0.3
    )

# Streamlit App Layout
st.set_page_config(page_title="English to Hindi Translator", page_icon="🇫🇷")
st.title("🇬🇧 ➡️ 🇫🇷 English to Hindi Translator")
st.write("This app uses **Google Gemini** via **LangChain** to translate English sentences to Hindi.")

# Input field
input_text = st.text_input("Enter an English sentence:", "")

# On button click
if st.button("Translate"):
    if not input_text.strip():
        st.warning("Please enter a sentence to translate.")
    else:
        try:
            # Load LLM
            llm = load_llm()

            # Define prompt with system and user roles
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a helpful assistant that translates English to Hindi."),
                ("user", "Translate the following sentence to Hindi:\n{sentence}")
            ])

            # Create a simple chain
            chain: Runnable = prompt | llm

            # Run the chain
            result = chain.invoke({"sentence": input_text})

            # Display result
            st.success("Translation completed!")
            st.text_area("Hindi Translation:", value=result.content.strip(), height=150)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")