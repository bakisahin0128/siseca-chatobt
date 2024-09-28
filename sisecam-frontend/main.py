import streamlit as st
from streamlit.web import cli as stcli
from config import app_logger, AUTHORIZATION_TOKEN, API_URL
import sys
import requests
import json


# Allowing customized avatars
CUSTOMIZE_AVATARS = True

# Title and Caption of the Streamlit App
TITLE = "💬 Şişecam PoC - Chatbot"
CAPTION = "🚀 Powered by NTT Data Business Solutions Türkiye - Data Science Team"

# Avatars Sources for Chat Parties
ai_avatar = "https://yt3.googleusercontent.com/bj0jJo-qXk0g2lwBYzmelRYKsg1IQDSFWwfvogRBINlBRK8fyvY_tzXhXVE9lHWvXjpnNLnaogw=s900-c-k-c0x00ffffff-no-rj"
human_avatar = "https://cdn-icons-png.freepik.com/512/6406/6406635.png"


def make_request(**kwargs):
    """
    Makes an HTTP request using the provided parameters and returns the response status code and content.

    Args:
        **kwargs: Arbitrary keyword arguments for customizing the request.
            - url (str): The URL of the request.
            - payload (dict, optional): The payload data for the request. Defaults to None.
            - headers (dict, optional): The headers for the request. Defaults to {"Content-Type": "application/json"}.
            - method (str, optional): The HTTP method for the request. Defaults to 'POST'.

    Returns:
        tuple[int, dict]: A tuple containing the response status code and content.
   """
    url = kwargs.get('url')
    payload = kwargs.get('payload', None)
    headers = kwargs.get('headers', {"Content-Type": "application/json"})
    method = kwargs.get('method', 'POST')
    status_code, content = 500, {}
    response = requests.request(
        method=method, url=url, headers=headers, json=payload,
        verify=False
    )
    try:
        status_code = response.status_code
        content = json.loads(response.content)
    except Exception as e:
        app_logger.info(e)
    return status_code, content


def initialize_session():
    """
    Initialize the chat session by clearing all session states including chat history, messages, etc.

    Args:
        N/A

    Returns:
        N/A
    """
    if "messages" not in st.session_state:
        add_initial_message()


def reset_chat():
    """
    Reset the chat by clearing the session state, initializing new session, adding the
    initial message, and rerunning the streamlit app.

    Args:
        N/A

    Returns:
        N/A
    """
    st.session_state.clear()
    initialize_session()
    add_initial_message()
    st.rerun()


def add_initial_message():
    """
    Initialize the chat session by checking if messages exist in the session state. If not,
    set a default message.

    Args:
        N/A

    Returns:
        N/A
    """
    if "messages" not in st.session_state.keys() or len(st.session_state.messages) == 0:
        st.session_state["messages"] = [{"role": "assistant", "content": "How may I assist you?"}]


def display_chat():
    """
    Loops through messages in session state and displays them in the chat with the
    appropriate avatar.

    Args:
        N/A

    Returns:
        N/A
    """
    for msg in st.session_state.messages:
        if CUSTOMIZE_AVATARS:
            st.chat_message(msg["role"], avatar=ai_avatar if msg["role"] == "assistant" else human_avatar).write(msg["content"])
        else:
            st.chat_message(msg["role"]).write(msg["content"])


def streamlit_main():
    # Setting Title and Description for the Streamlit App
    st.title(TITLE)
    st.caption(CAPTION)
    _, _, col3 = st.columns(3)
    initialize_session()

    # Creating Button for Resetting the Chat History
    with col3:
        new_chat = st.button(label='💬 New Chat', help="this button will delete your chat history and create a "
                                                      "new chat", use_container_width=True)
        if new_chat:
            with st.spinner(text="Creating New Chat ..."):
                reset_chat()

    st.markdown("""---""")

    # Implementing the Chat Component with the Chat History
    display_chat()

    # Creating User Input Field
    prompt = st.chat_input("Write something here")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        if CUSTOMIZE_AVATARS:
            st.chat_message("user", avatar=human_avatar).write(prompt)
        else:
            st.chat_message("user").write(prompt)

        # -------------- Getting AI Response --------------
        # Deleting initial message from chat history
        history = st.session_state.messages[1:]
        # Getting last 4 Messages (except the user's last input)
        # [user, assistant, user, assistant]
        if len(history) == 1:
            history = []
        elif len(history) > 1 and len(history) <= 5:
            history = history[:-1]
        elif len(history) > 5:
            history = history[-5:-1]
        status, content = make_request(url=API_URL,
                                       method='POST', payload={'input': prompt, 'history': history},
                                       headers={
                                           "Content-Type": "application/json",
                                           "authorization-token": AUTHORIZATION_TOKEN
                                       })
        if status == 200 and content.get("data").get('response'):
            response_msg = content.get("data").get('response')
            if CUSTOMIZE_AVATARS:
                st.chat_message("assistant", avatar=ai_avatar).write(response_msg)
            else:
                st.chat_message("assistant").write(response_msg)

            st.session_state.messages.append({"role": "assistant", "content": response_msg})
            st.rerun()
        else:
            st.error("Something went wrong. Please try again.")


if __name__ == '__main__':
    if st.runtime.exists():
        streamlit_main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())
