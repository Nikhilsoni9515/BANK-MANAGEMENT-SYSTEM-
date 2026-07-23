import streamlit as st
import json
import random
import string
from pathlib import Path
from datetime import datetime

# ------------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Apka Apna Bank",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------------
# STYLING
# ------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .stApp {
        background: linear-gradient(180deg, #0b1f16 0%, #0f2b1e 100%);
    }

    .bank-hero {
        background: linear-gradient(135deg, #0f5132 0%, #14824b 55%, #1fa25f 100%);
        border-radius: 20px;
        padding: 28px 34px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.35);
        border: 1px solid rgba(255,255,255,0.08);
    }
    .bank-hero h1 {
        color: #ffffff;
        font-size: 2.1rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: 0.5px;
    }
    .bank-hero p {
        color: #d7f4e4;
        margin: 4px 0 0 0;
        font-size: 0.95rem;
    }

    .bank-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 22px 24px;
        margin-bottom: 18px;
        box-shadow: 0 4px 18px rgba(0,0,0,0.25);
    }

    .metric-box {
        background: linear-gradient(135deg, #123d29, #1a5c3d);
        border-radius: 14px;
        padding: 18px 20px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.08);
    }
    .metric-box .label {
        color: #a9e4c4;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .metric-box .value {
        color: #ffffff;
        font-size: 1.6rem;
        font-weight: 700;
        margin-top: 4px;
    }

    .acc-chip {
        display: inline-block;
        background: #1fa25f;
        color: #06180f;
        font-weight: 700;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 0.85rem;
        letter-spacing: 1px;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a1912 0%, #0d2318 100%);
        border-right: 1px solid rgba(255,255,255,0.06);
    }

    div.stButton > button {
        background: linear-gradient(135deg, #14824b, #1fa25f);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.55rem 1.2rem;
        font-weight: 600;
        transition: all 0.2s ease;
        width: 100%;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #1fa25f, #26c274);
        box-shadow: 0 4px 14px rgba(31,162,95,0.45);
        transform: translateY(-1px);
    }

    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
        border-radius: 10px !important;
    }

    h2, h3 {
        color: #eafff2 !important;
    }
    p, label, span, div {
        color: #e6f3ec;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# BACKEND LOGIC  (adapted from the original Bank class, input()-free)
# ------------------------------------------------------------------
class Bank:
    database = "database.json"
    data = []

    if Path(database).exists():
        try:
            with open(database, "r") as fs:
                content = fs.read().strip()
                data = json.loads(content) if content else []
        except Exception as error:
            st.error(f"Could not load database: {error}")
            data = []

    @classmethod
    def _update(cls):
        with open(cls.database, "w") as fs:
            fs.write(json.dumps(cls.data, indent=2))

    @staticmethod
    def _generate_account_no():
        letters = random.choices(string.ascii_uppercase, k=4)
        digits = random.choices(string.digits, k=8)
        return "".join(letters + digits)

    @classmethod
    def create_account(cls, name, age, mail, number, pin):
        if age < 18:
            return False, "You must be 18 or older to open an account."
        if len(str(pin)) != 4:
            return False, "PIN must be exactly 4 digits."

        info = {
            "name": name,
            "age": age,
            "mail": mail,
            "number": number,
            "balance": 0,
            "account_no": cls._generate_account_no(),
            "pin": pin,
            "created": datetime.now().strftime("%d-%b-%Y %H:%M"),
        }
        cls.data.append(info)
        cls._update()
        return True, info

    @classmethod
    def _find_user(cls, acc_no, pin):
        matches = [u for u in cls.data if u["account_no"] == acc_no and u["pin"] == pin]
        return matches[0] if matches else None

    @classmethod
    def deposit_money(cls, acc_no, pin, amount):
        user = cls._find_user(acc_no, pin)
        if not user:
            return False, "Invalid account number or PIN."
        if amount > 100000 or amount <= 0:
            return False, "You cannot deposit more than ₹1,00,000 or an amount ≤ 0."
        user["balance"] += amount
        cls._update()
        return True, user

    @classmethod
    def withdraw_money(cls, acc_no, pin, amount):
        user = cls._find_user(acc_no, pin)
        if not user:
            return False, "Invalid account number or PIN."
        if amount > user["balance"]:
            return False, "Insufficient balance."
        if amount <= 0:
            return False, "Enter an amount greater than 0."
        user["balance"] -= amount
        cls._update()
        return True, user

    @classmethod
    def check_details(cls, acc_no, pin):
        user = cls._find_user(acc_no, pin)
        if not user:
            return False, "Invalid account number or PIN."
        return True, user

    @classmethod
    def update_details(cls, acc_no, pin, new_name, new_mail, new_number, new_pin):
        user = cls._find_user(acc_no, pin)
        if not user:
            return False, "Invalid account number or PIN."
        if new_name:
            user["name"] = new_name
        if new_mail:
            user["mail"] = new_mail
        if new_number:
            user["number"] = new_number
        if new_pin:
            if len(str(new_pin)) != 4:
                return False, "New PIN must be exactly 4 digits."
            user["pin"] = new_pin
        cls._update()
        return True, user

    @classmethod
    def delete_user(cls, acc_no, pin):
        user = cls._find_user(acc_no, pin)
        if not user:
            return False, "Invalid account number or PIN."
        cls.data.remove(user)
        cls._update()
        return True, "Account closed successfully."


# ------------------------------------------------------------------
# HEADER
# ------------------------------------------------------------------
st.markdown("""
<div class="bank-hero">
    <h1>🏦 Apka Apna Bank</h1>
    <p>Trusted • Secure • Always with you — banking made simple.</p>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# SIDEBAR NAV
# ------------------------------------------------------------------
menu = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Home",
        "🆕 Create Account",
        "💰 Deposit Money",
        "💸 Withdraw Money",
        "📄 Check Details",
        "✏️ Update Details",
        "❌ Close Account",
    ],
)

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Total Accounts:** {len(Bank.data)}")
st.sidebar.markdown(f"**Total Deposits Held:** ₹{sum(u['balance'] for u in Bank.data):,}")
st.sidebar.markdown("---")
st.sidebar.caption("Apka Apna Bank © 2026")

# ------------------------------------------------------------------
# HOME
# ------------------------------------------------------------------
if menu == "🏠 Home":
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""<div class="metric-box"><div class="label">Total Accounts</div>
        <div class="value">{len(Bank.data)}</div></div>""", unsafe_allow_html=True)
    with col2:
        total_balance = sum(u["balance"] for u in Bank.data)
        st.markdown(f"""<div class="metric-box"><div class="label">Total Balance</div>
        <div class="value">₹{total_balance:,}</div></div>""", unsafe_allow_html=True)
    with col3:
        avg = int(total_balance / len(Bank.data)) if Bank.data else 0
        st.markdown(f"""<div class="metric-box"><div class="label">Avg. Balance</div>
        <div class="value">₹{avg:,}</div></div>""", unsafe_allow_html=True)

    st.write("")
    st.markdown("""
    <div class="bank-card">
    <h3>Welcome to Apka Apna Bank 👋</h3>
    <p>Use the menu on the left to create a new account, deposit or withdraw money,
    check your account details, update your profile, or close your account.</p>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------------
# CREATE ACCOUNT
# ------------------------------------------------------------------
elif menu == "🆕 Create Account":
    st.markdown('<div class="bank-card">', unsafe_allow_html=True)
    st.subheader("Open a New Account")

    with st.form("create_account_form"):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Full Name")
            age = st.number_input("Age", min_value=0, max_value=120, step=1)
            mail = st.text_input("Email Address")
        with c2:
            number = st.text_input("Phone Number")
            pin = st.text_input("Set a 4-digit PIN", type="password", max_chars=4)

        submitted = st.form_submit_button("Create Account")

    if submitted:
        if not name or not mail or not number or not pin:
            st.error("Please fill in all the fields.")
        elif not pin.isdigit():
            st.error("PIN must contain only digits.")
        else:
            ok, result = Bank.create_account(name, int(age), mail, number, int(pin))
            if ok:
                st.success("🎉 Account created successfully!")
                st.markdown(f"""
                <div class="bank-card">
                    <p>Account Number: <span class="acc-chip">{result['account_no']}</span></p>
                    <p>Name: {result['name']}</p>
                    <p>Balance: ₹{result['balance']}</p>
                </div>
                """, unsafe_allow_html=True)
                st.info("Please save your account number and PIN safely — you'll need them for every transaction.")
            else:
                st.error(result)
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# DEPOSIT
# ------------------------------------------------------------------
elif menu == "💰 Deposit Money":
    st.markdown('<div class="bank-card">', unsafe_allow_html=True)
    st.subheader("Deposit Money")

    with st.form("deposit_form"):
        acc_no = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password", max_chars=4)
        amount = st.number_input("Amount to Deposit (₹)", min_value=0, step=100)
        submitted = st.form_submit_button("Deposit")

    if submitted:
        if not acc_no or not pin:
            st.error("Please enter your account number and PIN.")
        else:
            try:
                ok, result = Bank.deposit_money(acc_no, int(pin), int(amount))
                if ok:
                    st.success(f"✅ ₹{amount:,} deposited successfully! New balance: ₹{result['balance']:,}")
                else:
                    st.error(result)
            except ValueError:
                st.error("PIN must be numeric.")
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# WITHDRAW
# ------------------------------------------------------------------
elif menu == "💸 Withdraw Money":
    st.markdown('<div class="bank-card">', unsafe_allow_html=True)
    st.subheader("Withdraw Money")

    with st.form("withdraw_form"):
        acc_no = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password", max_chars=4)
        amount = st.number_input("Amount to Withdraw (₹)", min_value=0, step=100)
        submitted = st.form_submit_button("Withdraw")

    if submitted:
        if not acc_no or not pin:
            st.error("Please enter your account number and PIN.")
        else:
            try:
                ok, result = Bank.withdraw_money(acc_no, int(pin), int(amount))
                if ok:
                    st.success(f"✅ ₹{amount:,} withdrawn successfully! New balance: ₹{result['balance']:,}")
                else:
                    st.error(result)
            except ValueError:
                st.error("PIN must be numeric.")
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# CHECK DETAILS
# ------------------------------------------------------------------
elif menu == "📄 Check Details":
    st.markdown('<div class="bank-card">', unsafe_allow_html=True)
    st.subheader("Check Account Details")

    with st.form("check_form"):
        acc_no = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password", max_chars=4)
        submitted = st.form_submit_button("Check Details")

    if submitted:
        if not acc_no or not pin:
            st.error("Please enter your account number and PIN.")
        else:
            try:
                ok, result = Bank.check_details(acc_no, int(pin))
                if ok:
                    st.success("Account found ✅")
                    c1, c2 = st.columns(2)
                    with c1:
                        st.write(f"**Name:** {result['name']}")
                        st.write(f"**Age:** {result['age']}")
                        st.write(f"**Email:** {result['mail']}")
                    with c2:
                        st.write(f"**Phone:** {result['number']}")
                        st.write(f"**Account No.:** {result['account_no']}")
                        st.write(f"**Balance:** ₹{result['balance']:,}")
                else:
                    st.error(result)
            except ValueError:
                st.error("PIN must be numeric.")
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# UPDATE DETAILS
# ------------------------------------------------------------------
elif menu == "✏️ Update Details":
    st.markdown('<div class="bank-card">', unsafe_allow_html=True)
    st.subheader("Update Account Details")
    st.caption("Leave a field blank to keep it unchanged.")

    with st.form("update_form"):
        acc_no = st.text_input("Account Number")
        pin = st.text_input("Current PIN", type="password", max_chars=4)
        st.markdown("---")
        new_name = st.text_input("New Name (optional)")
        new_mail = st.text_input("New Email (optional)")
        new_number = st.text_input("New Phone Number (optional)")
        new_pin = st.text_input("New 4-digit PIN (optional)", type="password", max_chars=4)
        submitted = st.form_submit_button("Update Details")

    if submitted:
        if not acc_no or not pin:
            st.error("Please enter your account number and current PIN.")
        else:
            try:
                new_pin_val = int(new_pin) if new_pin else None
                ok, result = Bank.update_details(acc_no, int(pin), new_name, new_mail, new_number, new_pin_val)
                if ok:
                    st.success("✅ Details updated successfully!")
                else:
                    st.error(result)
            except ValueError:
                st.error("PIN must be numeric.")
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# DELETE / CLOSE ACCOUNT
# ------------------------------------------------------------------
elif menu == "❌ Close Account":
    st.markdown('<div class="bank-card">', unsafe_allow_html=True)
    st.subheader("Close Account")
    st.warning("This action is permanent and cannot be undone.")

    with st.form("delete_form"):
        acc_no = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password", max_chars=4)
        confirm = st.checkbox("I understand this will permanently close my account.")
        submitted = st.form_submit_button("Close Account")

    if submitted:
        if not acc_no or not pin:
            st.error("Please enter your account number and PIN.")
        elif not confirm:
            st.error("Please confirm before proceeding.")
        else:
            try:
                ok, result = Bank.delete_user(acc_no, int(pin))
                if ok:
                    st.success(result)
                else:
                    st.error(result)
            except ValueError:
                st.error("PIN must be numeric.")
    st.markdown("</div>", unsafe_allow_html=True)