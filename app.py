import streamlit as st
import re
from tools import (
    get_order_status,
    check_return_eligibility,
    search_products,
    get_recommendations,
    faq_answer
)

st.set_page_config(
    page_title="AI E-Commerce Support Agent",
    page_icon="🛒",
    layout="centered"
)

st.title("🛒 AI-Powered E-Commerce Customer Support Agent")
st.caption("Using Tool Calling and Memory")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "order_id" not in st.session_state:
    st.session_state.order_id = None

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def agent_response(user_input):
    text = user_input.lower()

    order_match = re.search(r"ord\d+", text, re.IGNORECASE)
    if order_match:
        st.session_state.order_id = order_match.group(0).upper()

    order_id = st.session_state.order_id

    if "order" in text and any(
        word in text for word in ["status", "track", "where", "delivery"]
    ):
        if not order_id:
            return "Sure! 😊 Could you please share your order ID?"
        return get_order_status(order_id)

    if "return" in text or "refund" in text:
        if not order_id:
            return "Sure! Please provide your order ID so I can check the return eligibility."
        return check_return_eligibility(order_id)

    if any(word in text for word in ["recommend", "recommendation", "suggest"]):
        return get_recommendations()

    if any(word in text for word in [
        "shoes", "sneakers", "headphones", "watch", "speaker"
    ]):
        if "shoes" in text:
            keyword = "shoes"
        elif "sneakers" in text:
            keyword = "sneakers"
        elif "headphones" in text:
            keyword = "headphones"
        elif "watch" in text:
            keyword = "watch"
        else:
            keyword = "speaker"
        return search_products(keyword)

    faq = faq_answer(text)
    if faq:
        return faq

    return (
        "🤖 I'm your AI E-Commerce Support Agent.\n\n"
        "I can help you with:\n\n"
        "• 📦 Order tracking\n"
        "• 🔄 Returns and refunds\n"
        "• 🛍️ Product search\n"
        "• ⭐ Product recommendations\n"
        "• 🚚 Shipping information\n"
        "• 💳 Payment information"
    )

user_input = st.chat_input("Ask me about your order or products...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("assistant"):
        response = agent_response(user_input)
        st.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })
