import streamlit as st
from clickable_textbox import clickable_textbox
import base64
import time
# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run my_component/example.py`

st.subheader("Component with constant args")

# Create an instance of our component with a constant `name` arg, and
# print its output value.

if 'excerpt_selected' not in st.session_state:
    st.session_state.excerpt_selected = None

def clean_response_for_textbox(input, footnotes):
    for footnote in footnotes:
        input=input.replace(footnote, " </span><span style='color: blue; cursor: pointer;'><u>"+footnote+"</u></span><span>")
    input="<span>"+input+"</span>"
    # \n doesnt work, so replace with <br> for linebreaks
    input=input.replace("\n", "<br>")
    return input

sample_llm_response="""This result comes from Excerpt 1. Excerpt 2 is not mentioned, but maybe you can find what you want in excerpt 3? [1-3] A bi-directional Streamlit Component has two parts: A frontend, which is built out of HTML and any other web tech you like (JavaScript, React, Vue, etc.), and gets rendered in Streamlit apps via an iframe tag. 
A Python API, which Streamlit apps use to instantiate and talk to that frontend [1-47] [2-9] 
To make the process of creating bi-directional Streamlit Components easier, we've created a React template and a TypeScript-only template in the Streamlit Component-template GitHub repo. We also provide some example Components in the same repo.

not sure if a new para works, hopefully it does otherwise we are gonna have to troubleshoot again!"""

with st.spinner('sleeping'):
    time.sleep(1)

with open('clickable_textbox/robot.png', "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode()

def display_response(message, sender):
    
    html_template="""
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Messaging App Design</title>
    <style>
        body {
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        background-color: #f0f0f0; 
        }

        .message-container {
        display: flex;
        align-items: flex-start;
        gap: 20px;
        }

        .icon {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        overflow: hidden;
        }

        .icon img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        }

        .message-box {
        display: inline-block;
        padding: 15px;
        background-color: #ffffff;
        border-radius: 10px;
        color: #333;
        border: 1px solid #ccc; /* Border added */
        }
    </style>
    </head>
    <body>
        <div class="message-container">
            <div class="icon">
                <img src="data:image/jpeg;base64,{{img_base64}}" alt="Sender Icon">
            </div>
            <div class="message-box">
            {{message}}
            </div>
        </div>
    </body>
    </html>
    """
    html_with_msg = html_template.replace("{{message}}", message)
    img_fp='clickable_textbox/robot.png' if sender=='robot' else 'images/user.png'
    with open(img_fp, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode()
    html_with_msg = html_with_msg.replace("{{img_base64}}", img_base64)
    st.html(html_with_msg)

@st._fragment
def response_box(response, footnotes):
    excerpt_selected = clickable_textbox(text_to_display=response, img_path= 'clickable_textbox/robot.png',height=400, key='foo')
    if (excerpt_selected in footnotes) and (excerpt_selected != st.session_state.excerpt_selected):
        st.session_state.excerpt_selected=excerpt_selected
        st.rerun()

display_response('hello there', 'robot')
footnotes=["[1-3]", "[2-9]", "[1-47]"]
response=clean_response_for_textbox(sample_llm_response, footnotes)
response_box(response, footnotes)


st.markdown(f"You've selected {st.session_state.excerpt_selected}")

st.markdown("---")