import streamlit as st

# ----------------------------
# USERS SIMULÉS (démo banque)
# ----------------------------
USERS = {
    "admin": "admin123",
    "data_officer": "data2026",
    "analyst": "analyst123"
}

# ----------------------------
# LOGIN PAGE
# ----------------------------
def login():

    st.title("🔐 CA Data Vision - Secure Access")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username in USERS and USERS[username] == password:
            st.session_state["authenticated"] = True
            st.session_state["user"] = username
            st.success("Access granted ✔")
        else:
            st.error("Invalid credentials ❌")


# ----------------------------
# CHECK AUTH
# ----------------------------
def is_authenticated():

    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    return st.session_state["authenticated"]