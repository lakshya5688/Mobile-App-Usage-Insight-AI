import os
import json
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
RUNPOD_TOKEN = os.getenv("RUNPOD_TOKEN")
RUNPOD_CHATBOT_URL = os.getenv("RUNPOD_CHATBOT_URL")
MODEL_NAME = os.getenv("MODEL_NAME")

client = OpenAI(
    api_key=os.getenv("RUNPOD_TOKEN"),
    base_url=os.getenv("RUNPOD_CHATBOT_URL"),
)
model_name = os.getenv("MODEL_NAME")

def get_chatbot_response(client, model_name, messages, temperature=0):  # FIXED
    input_messages = []
    for message in messages:
        input_messages.append({"role": message["role"], "content": message["content"]})

    response = client.chat.completions.create(
        model=model_name,
        messages=input_messages,
        temperature=0.0,
        max_tokens=2000,
        top_p=0.8,
    ).choices[0].message.content
    return response

file_map = {
    ("instagram", "usage"): "instagram_usage_forecast_filtered.json",
    ("instagram", "notifications"): "instagram_notifications_forecast_filtered.json",
    ("instagram", "times_opened"): "instagram_times_opened_forecast_filtered.json",
    ("whatsapp", "usage"): "whatsapp_usage_forecast_filtered.json",
    ("whatsapp", "notifications"): "whatsapp_notifications_forecast_filtered.json",
    ("whatsapp", "times_opened"): "whatsapp_times_opened_forecast_filtered.json",
}


def classify_query(query):
    query = query.lower()
    if "instagram" in query:
        app = "instagram"
    elif "whatsapp" in query:
        app = "whatsapp"
    else:
        app = None

    if "notification" in query:
        metric = "notifications"
    elif "time" in query and "open" in query:
        metric = "times_opened"
    elif "usage" in query or "used" in query:
        metric = "usage"
    else:
        metric = None

    return app, metric



def load_forecast_data(app, metric):
    file_map = {
        ("instagram", "usage"): "instagram_usage_forecast_filtered.json",
        ("instagram", "notifications"): "instagram_notifications_forecast_filtered.json",
        ("instagram", "times_opened"): "instagram_times_opened_forecast_filtered.json",
        ("whatsapp", "usage"): "whatsapp_usage_forecast_filtered.json",
        ("whatsapp", "notifications"): "whatsapp_notifications_forecast_filtered.json",
        ("whatsapp", "times_opened"): "whatsapp_times_opened_forecast_filtered.json",
    }
    key = (app, metric)
    if key not in file_map:
        return None

    path = os.path.join("json_data_filtered", file_map[key])
    with open(path, 'r') as f:
        data = json.load(f)
    return data


def format_forecast_summary(data, max_days=5):
    context = []
    for entry in data[-max_days:]:
        date = entry["ds"]
        trend = round(entry["trend"], 2)
        pred = round(entry["yhat"], 2)
        context.append(f"On {date}, predicted value is {pred} with trend {trend}.")
    return "\n".join(context)


def answer_user_query(query):
    app, metric = classify_query(query)
    if not app or not metric:
        return "Sorry, I couldn't detect which app or metric you're referring to."

    data = load_forecast_data(app, metric)
    if not data:
        return f"No data found for {app} - {metric}."

    context = format_forecast_summary(data)

    prompt = (
        f"You're an assistant analyzing forecasted mobile app usage.\n"
        f"Treat the current date as **2022-09-21**, and note that the forecast extends up to **2022-10-21**.\n\n"
        f"If the user asks for data of any particular data of past or future check the files and then give it to him if it exists"
        f"App: {app.capitalize()}\nMetric: {metric.replace('_', ' ').capitalize()}\n"
        f"Here is the forecast summary for recent days:\n"
        f"{context}\n\n"
        f"User Question: {query}\n"
        f"Answer the user's question in natural language, with reasoning if needed."
    )

#     prompt = (
#     f"You're an assistant analyzing forecasted mobile app usage behavior.\n\n"
#     f"The forecast data is for the mobile app: **{app.capitalize()}**, and the metric: **{metric.replace('_', ' ').capitalize()}**.\n"
#     f"You are given historical trends and forecasted values between past and future dates.\n"
#     f"Treat the current date as **2022-09-21**, and note that the forecast extends up to **2022-10-21**.\n\n"
#     f"Here is the forecast summary for recent days:\n"
#     f"{context}\n\n"
#     f"User Question: {query}\n\n"
#     f"Based on the forecasted trends, provide a helpful, natural language answer with reasoning if needed. "
#     f"Summarize patterns, highlight expected increases or decreases, and be clear about what the data shows."
# )


    messages = [
        {'role': 'system', 'content': prompt},
        {'role': 'user', 'content': query}
    ]

    return get_chatbot_response(client, model_name, messages)

# streamlit_app.py

import os
import json
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Mobile Usage Forecast Assistant",
    page_icon="",
    layout="centered",
)

st.set_page_config(layout="wide")


st.markdown(
        """
        <div style="display: flex; flex-direction: column; justify-content: center; height: 100%;">
            <h1 style="text-align: center;">Mobile Usage Forecast Assistant</h1>
            
        </div>
        """,
    unsafe_allow_html=True
)
st.markdown("---")

st.subheader("Ask About Your Forecasted Mobile Usage")
st.markdown(
    "Ask questions about how your usage of **Instagram** or **WhatsApp** will trend — based on intelligent forecasts powered by LLaMA-3.1 8B-Instruct."
)

query = st.text_input(" Your Question", placeholder="e.g. Will my WhatsApp notifications decrease this weekend?")
submit = st.button(" Ask")

if submit and query:
    with st.spinner("Analyzing trends and generating insights with LLaMA..."):
        response = answer_user_query(query)

    st.success("Assistant's Response")
    st.markdown(f"```markdown\n{response}\n```")

    st.markdown("---")

st.markdown(
    """
    <div style='text-align: center; font-size: 0.9em; color: gray; margin-top: 40px;'>
        Powered by <b>LLaMA 3.1 8B - Instruct</b> on RunPod · Forecasts by Prophet<br>
    </div>
    """,
    unsafe_allow_html=True,
)
