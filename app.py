
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler


# ==========================================
# PAGE SETTINGS
# ==========================================

st.set_page_config(
    page_title="AI Shopping List Optimizer",
    page_icon="🛍️",
    layout="wide"
)


# ==========================================
# CUTE CUSTOM DESIGN
# ==========================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #fff0f6, #f3e8ff, #e0f7fa);
}

/* Main title */
.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #8e44ad;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #6c5ce7;
    font-size: 18px;
    margin-bottom: 30px;
}

/* Cards */
.card {
    background: white;
    padding: 20px;
    border-radius: 20px;
    box-shadow: 0px 5px 15px rgba(142, 68, 173, 0.15);
    margin-bottom: 15px;
}

/* Section headings */
.section-title {
    color: #8e44ad;
    font-size: 25px;
    font-weight: bold;
}

/* Success box */
.success-card {
    background: #e8fff3;
    padding: 18px;
    border-radius: 18px;
    border-left: 6px solid #2ecc71;
}

/* Warning box */
.warning-card {
    background: #fff4e6;
    padding: 18px;
    border-radius: 18px;
    border-left: 6px solid #ff9f43;
}

/* AI box */
.ai-card {
    background: linear-gradient(135deg, #fce4ec, #ede7f6);
    padding: 20px;
    border-radius: 20px;
    border-left: 6px solid #9b59b6;
    margin: 10px 0;
}

/* Button */
.stButton > button {
    background: linear-gradient(90deg, #ff69b4, #9b59b6);
    color: white;
    border: none;
    border-radius: 25px;
    padding: 10px 25px;
    font-weight: bold;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #9b59b6, #ff69b4);
    color: white;
}

/* Metrics */
[data-testid="stMetric"] {
    background: white;
    padding: 15px;
    border-radius: 18px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}

/* Footer */
.footer {
    text-align: center;
    color: #8e44ad;
    font-size: 15px;
    padding: 20px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# TITLE
# ==========================================

st.markdown(
    '<div class="main-title">🛍️ AI Shopping List Optimizer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">✨ Shop smarter • Save money • Stay within your budget ✨</div>',
    unsafe_allow_html=True
)


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.markdown("## 🌸 Shopping Settings")

budget = st.sidebar.number_input(
    "💰 Your Budget (₹)",
    min_value=0.0,
    value=2000.0,
    step=100.0
)

st.sidebar.markdown("---")

st.sidebar.info(
    "💡 Enter your items, quantity and price. "
    "The app will calculate your shopping cost and give simple saving suggestions."
)


# ==========================================
# DEFAULT SHOPPING DATA
# ==========================================

default_data = pd.DataFrame({
    "Item": [
        "Rice",
        "Milk",
        "Eggs",
        "Bread",
        "Chicken"
    ],

    "Quantity": [
        5,
        2,
        12,
        2,
        1
    ],

    "Price per Unit (₹)": [
        60,
        50,
        7,
        40,
        250
    ]
})


# ==========================================
# SHOPPING LIST
# ==========================================

st.markdown(
    '<div class="section-title">🛒 1. Your Shopping List</div>',
    unsafe_allow_html=True
)

st.write("Add, remove or edit your shopping items below. 💕")

data = st.data_editor(
    default_data,
    num_rows="dynamic",
    use_container_width=True
)


# ==========================================
# CLEAN DATA
# ==========================================

data["Item"] = data["Item"].fillna("").astype(str)

data = data[
    data["Item"].str.strip() != ""
].copy()

data["Quantity"] = pd.to_numeric(
    data["Quantity"],
    errors="coerce"
).fillna(0)

data["Price per Unit (₹)"] = pd.to_numeric(
    data["Price per Unit (₹)"],
    errors="coerce"
).fillna(0)


# ==========================================
# TOTAL PRICE
# ==========================================

data["Total Price (₹)"] = (
    data["Quantity"] *
    data["Price per Unit (₹)"]
)

total_cost = data["Total Price (₹)"].sum()

remaining_budget = budget - total_cost


# ==========================================
# SUMMARY
# ==========================================

st.markdown(
    '<div class="section-title">💰 2. Shopping Summary</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "🛍️ Total Cost",
        f"₹{total_cost:.2f}"
    )

with col2:
    st.metric(
        "💵 Budget",
        f"₹{budget:.2f}"
    )

with col3:
    st.metric(
        "✨ Remaining",
        f"₹{remaining_budget:.2f}"
    )


# ==========================================
# BUDGET STATUS
# ==========================================

if total_cost <= budget:

    st.markdown(
        f"""
        <div class="success-card">
        🎉 <b>Great job!</b><br>
        Your shopping list is within your budget.<br>
        You have <b>₹{remaining_budget:.2f}</b> remaining. 💚
        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.markdown(
        f"""
        <div class="warning-card">
        ⚠️ <b>Oops!</b><br>
        Your shopping list is over budget by
        <b>₹{abs(remaining_budget):.2f}</b>.<br>
        Let's find some ways to save! 💡
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================
# SHOPPING TABLE
# ==========================================

st.markdown(
    '<div class="section-title">📋 3. Shopping Details</div>',
    unsafe_allow_html=True
)

display_data = data[
    [
        "Item",
        "Quantity",
        "Price per Unit (₹)",
        "Total Price (₹)"
    ]
]

st.dataframe(
    display_data,
    use_container_width=True,
    hide_index=True
)


# ==========================================
# AI OPTIMIZATION
# ==========================================

st.markdown(
    '<div class="section-title">🤖 4. AI Shopping Suggestions</div>',
    unsafe_allow_html=True
)

if len(data) > 0:

    prices = data[["Total Price (₹)"]].values

    scaler = MinMaxScaler()

    if len(data) > 1 and prices.max() != prices.min():

        data["Price Score"] = scaler.fit_transform(
            prices
        ).flatten()

    else:

        data["Price Score"] = 0.5


    # Sort expensive items first

    expensive_items = data.sort_values(
        by="Total Price (₹)",
        ascending=False
    )


    # --------------------------------------
    # AI SUGGESTIONS
    # --------------------------------------

    if total_cost > budget:

        st.markdown(
            """
            <div class="ai-card">
            🤖 <b>AI Recommendation</b><br><br>
            Your shopping list is currently above your budget.
            Start by checking the most expensive items first. 💰
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class="ai-card">
            🤖 <b>AI Recommendation</b><br><br>
            Your shopping list is within your budget! 🎉
            You can still compare prices to find extra savings. ✨
            </div>
            """,
            unsafe_allow_html=True
        )


    # --------------------------------------
    # MOST EXPENSIVE ITEM
    # --------------------------------------

    most_expensive = expensive_items.iloc[0]

    st.info(
        f"🔎 Your highest-cost item is "
        f"**{most_expensive['Item']}** "
        f"with a total cost of "
        f"**₹{most_expensive['Total Price (₹)']:.2f}**."
    )


    # ======================================
    # PRIORITY LIST
    # ======================================

    st.markdown(
        "### ⭐ Shopping Priority"
    )

    optimized = data.copy()

    optimized["Priority"] = np.where(
        optimized["Price Score"] >= 0.7,
        "🔴 Check Price",
        "🟢 Normal"
    )

    optimized = optimized.sort_values(
        by="Total Price (₹)",
        ascending=False
    )

    priority_table = optimized[
        [
            "Item",
            "Quantity",
            "Price per Unit (₹)",
            "Total Price (₹)",
            "Priority"
        ]
    ]

    st.dataframe(
        priority_table,
        use_container_width=True,
        hide_index=True
    )


    # ======================================
    # SAVING TIPS
    # ======================================

    st.markdown(
        "### 💡 Cute Little Saving Tips"
    )

    tips = [
        "🛒 Compare prices before buying expensive items.",
        "🏷️ Look for discounts and offers.",
        "📦 Buy larger quantities only when you really need them.",
        "💰 Set a budget before shopping.",
        "🔎 Check the highest-cost items first."
    ]

    for tip in tips:

        st.write(tip)


    # ======================================
    # SAVING TARGET
    # ======================================

    if total_cost > budget:

        amount_to_save = total_cost - budget

        st.warning(
            f"💸 You need to reduce your shopping cost by "
            f"₹{amount_to_save:.2f} to stay within budget."
        )

    else:

        possible_saving = total_cost * 0.10

        st.success(
            f"✨ You could try to save around "
            f"₹{possible_saving:.2f} by comparing prices."
        )


    # ======================================
    # CHART
    # ======================================

    st.markdown(
        '<div class="section-title">📊 5. Shopping Cost Chart</div>',
        unsafe_allow_html=True
    )

    chart_data = data.sort_values(
        by="Total Price (₹)",
        ascending=False
    )

    fig, ax = plt.subplots(
        figsize=(10, 5)
    )

    ax.bar(
        chart_data["Item"],
        chart_data["Total Price (₹)"]
    )

    ax.set_xlabel("Shopping Items")

    ax.set_ylabel(
        "Total Cost (₹)"
    )

    ax.set_title(
        "🛍️ Cost of Each Shopping Item"
    )

    plt.xticks(
        rotation=45
    )

    plt.tight_layout()

    st.pyplot(fig)


# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.markdown(
    """
    <div class="footer">
    💕 Made with Python + Streamlit 💕<br>
    🛍️ AI Shopping List Optimizer
    </div>
    """,
    unsafe_allow_html=True
)
