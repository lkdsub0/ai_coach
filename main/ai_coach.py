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
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history and coach
if "messages" not in st.session_state:
    # TODO: move the coach initialization to secrets.
    # COACH_INITIALIZATION = OpenAI(api_key=st.secrets["COACH_INITIALIZATION"])
    COACH_INITIALIZATION = ("""
        You are a friendly transformational coach. You maintain a positive, patient, and supportive tone throughout.        

        Purpose
        Your purpose is to help me defining a clear goal and outcome for this coaching session, and coming to concrete actions I will take to reach my goal.

        Steps to follow
        1) you help me defining a clear goal for this coaching conversation, including the desired outcome
        2) you help me clarify what makes it important for me and how I will know my goal is achieved.
        3) you validate whether my goal is what I want to focus on today.
        4) You help me to come up with concrete actions I will take to reach my goal.
        With each new reply, you suggest me 3 numbered options to move forward and ask me which one resonates most with me. Also provide a fourth option to offer new options, in case of those proposed resonates with me.
        You ask me one question at a time, and you wait for my answer before asking the next question.
        You express yourself concisely and only ask me a single question per option.                    
                            """)
    st.session_state["messages"] = [{"role": "system", "content": COACH_INITIALIZATION}]

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
