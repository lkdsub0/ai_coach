# Source: https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps
# To view this Streamlit app on a browser, run it with the following command:
# streamlit run w:/Sync/Workspace/Python/AI_Coach/main/ai_coach.py


import streamlit as st
from openai import OpenAI

st.title("AI Coach")

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set a default model
if "openai_model" not in st.session_state:
    # st.session_state["openai_model"] = "gpt-3.5-turbo"
    st.session_state["openai_model"] = "gpt-4o-mini"  # Use a more capable model for coaching

# Initialize chat history and coach
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": st.secrets["COACH_INITIALIZATION"]}]

# Display chat messages from history on app rerun
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

if st.session_state.messages:
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
