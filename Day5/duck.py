import streamlit as st
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain.tools.ddg_search.tool import DuckDuckGoSearchRun
from langchain_google_genai import ChatGoogleGenerativeAI
import time
from cachetools import TTLCache

# Hardcoded Gemini API Key (⚠️ Do not use this in production)
GOOGLE_API_KEY = "AIzaSyBBR15D1gueQ_tGRdtLfn-5SYRa7sfFBQ0"

# Configure the Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.2
)

# Add DuckDuckGo search tool
search_tool = DuckDuckGoSearchRun()

# Define tools for the agent
tools = [
    Tool(
        name="DuckDuckGo Search",
        func=search_tool.run,
        description="Use this tool to search for current events or factual answers from the internet."
    )
]

# Initialize the agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False
)

# Initialize cache (TTL of 1 hour for query results)
cache = TTLCache(maxsize=100, ttl=3600)

# Rate limiting variables
last_request_time = 0
MIN_REQUEST_INTERVAL = 2  # Minimum seconds between requests

# ------------- Streamlit UI -------------
st.set_page_config(page_title="🌐 Ask Anything (Live Agent)", page_icon="🤖")
st.title("🤖 Real-Time Q&A with Gemini + Web Search")
st.markdown("Ask about **news**, **facts**, or **trending topics**. Powered by `Gemini` + `DuckDuckGo`.")

# Store query in session state to debounce
if "query" not in st.session_state:
    st.session_state.query = ""

query = st.text_input("🔍 Enter your question:", key="query_input")
ask = st.button("Get Answer")

if ask:
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        # Check cache first
        if query in cache:
            st.markdown("### 🧠 Answer (from cache):")
            st.write(cache[query])
        else:
            # Rate limiting
            current_time = time.time()
            global last_request_time
            if current_time - last_request_time < MIN_REQUEST_INTERVAL:
                st.warning(f"Please wait {MIN_REQUEST_INTERVAL - (current_time - last_request_time):.1f} seconds before submitting another question.")
            else:
                try:
                    with st.spinner("Thinking..."):
                        response = agent.run(query)
                        cache[query] = response  # Store in cache
                        last_request_time = current_time
                    st.markdown("### 🧠 Answer:")
                    st.write(response)
                except Exception as e:
                    if "rate limit" in str(e).lower():
                        st.error("⚠️ API rate limit exceeded. Please try again later.")
                    else:
                        st.error(f"⚠️ Failed to get a response: {e}")