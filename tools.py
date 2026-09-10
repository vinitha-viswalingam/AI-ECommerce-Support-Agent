import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def load_json(filename):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)

def get_order_status(order_id):
    orders = load_json("orders.json")

    for order in orders:
        if order["order_id"].upper() == order_id.upper():
            return (
                f"📦 **Order {order_id}**\n\n"
                f"Product: **{order['product']}**\n\n"
                f"Status: **{order['status']}**\n\n"
                f"Expected Delivery: **{order['expected_delivery']}**"
            )

    return f"❌ Sorry, I couldn't find order **{order_id}**."

def check_return_eligibility(order_id):
    orders = load_json("orders.json")

    for order in orders:
        if order["order_id"].upper() == order_id.upper():
            if order["return_eligible"]:
                return (
                    f"✅ Yes! The product **{order['product']}** "
                    f"from order **{order_id}** is eligible for return.\n\n"
                    f"Return window: **{order['return_days']} days** from delivery."
                )

            return (
                f"❌ The product **{order['product']}** "
                f"from order **{order_id}** is currently not eligible for return."
            )

    return f"❌ Order **{order_id}** was not found."

def search_products(keyword):
    products = load_json("products.json")
    keyword = keyword.lower()
    results = []

    for product in products:
        if (
            keyword in product["name"].lower()
            or keyword in product["category"].lower()
        ):
            results.append(product)

    if not results:
        return "🔍 Sorry, I couldn't find matching products."

    response = "🛍️ **Products Found:**\n\n"

    for product in results:
        response += (
            f"**{product['name']}**\n"
            f"Category: {product['category']}\n"
            f"Price: ₹{product['price']}\n"
            f"Rating: ⭐ {product['rating']}\n\n"
        )

    return response

def get_recommendations():
    products = load_json("products.json")

    sorted_products = sorted(
        products,
        key=lambda x: x["rating"],
        reverse=True
    )

    response = "⭐ **Recommended Products:**\n\n"

    for product in sorted_products[:3]:
        response += (
            f"**{product['name']}**\n"
            f"₹{product['price']} | Rating ⭐ {product['rating']}\n\n"
        )

    return response

def faq_answer(question):
    question = question.lower()

    if "shipping" in question:
        return "🚚 **Shipping Information**\n\nStandard shipping usually takes 3–5 business days."

    if "payment" in question:
        return "💳 **Payment Information**\n\nWe support common online payment methods such as cards and UPI."

    if "cancel" in question:
        return "❌ **Cancellation Policy**\n\nOrders can be cancelled before they are shipped."

    if "return policy" in question:
        return "🔄 **Return Policy**\n\nProducts can be returned according to the return window applicable to the order."

    return None
