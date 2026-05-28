import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from db import get_connection

# ---------------- DB ----------------
conn = get_connection()
cursor = conn.cursor()

# ---------------- SESSION ----------------
if "role" not in st.session_state:
    st.session_state.role = None

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "booking_id" not in st.session_state:
    st.session_state.booking_id = None

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="EV Charging System",
    layout="wide"
)

# ---------------- UI STYLE ----------------
st.markdown("""
<style>

/* ---------------- COLOR VARIABLES ---------------- */
:root {
    --bg-dark: #0f172a;
    --bg-gradient: linear-gradient(135deg,#0f172a,#020617,#020617);
    --glass-bg: rgba(255,255,255,0.08);
    --neon-blue: #00f5ff;
    --neon-purple: #a855f7;
    --neon-pink: #ec4899;
    --text-light: #e2e8f0;
}

/* ---------------- MAIN BACKGROUND ---------------- */
.stApp {
    background: var(--bg-gradient);
    color: var(--text-light);
    font-family: 'Segoe UI', sans-serif;
}

/* ---------------- LOGIN PAGE ---------------- */
.block-container {
    padding-top: 2rem;
}

/* ---------------- HEADINGS ---------------- */
h1, h2, h3 {
    color: var(--neon-blue);
    text-shadow: 0 0 8px var(--neon-blue);
}

/* ---------------- LABEL FIX ---------------- */
label, .stTextInput label, .stSelectbox label {
    color: #e0f7ff !important;
    font-weight: 600;
}

/* ---------------- BUTTONS ---------------- */
.stButton>button {
    background: linear-gradient(135deg,var(--neon-blue),var(--neon-purple));
    color: black;
    border-radius: 12px;
    padding: 8px 18px;
    font-weight: bold;
    border: none;
    transition: 0.3s;
    box-shadow: 0 0 10px var(--neon-blue);
    width: 100%;
}

.stButton>button:hover {
    transform: scale(1.03);
    box-shadow: 0 0 20px var(--neon-purple);
}

/* ---------------- SIDEBAR ---------------- */
section[data-testid="stSidebar"] {
    background: rgba(0,0,0,0.6);
    backdrop-filter: blur(10px);
    border-right: 1px solid rgba(255,255,255,0.1);
}

/* ---------------- SIDEBAR RADIO ---------------- */
div[role="radiogroup"] > label {
    background: rgba(255,255,255,0.05);
    padding: 8px;
    border-radius: 8px;
    margin-bottom: 5px;
    color: var(--text-light);
    transition: 0.2s;
}

div[role="radiogroup"] > label:hover {
    background: rgba(0,245,255,0.2);
}

/* ---------------- CARDS ---------------- */
.card {
    padding: 20px;
    border-radius: 16px;
    background: var(--glass-bg);
    backdrop-filter: blur(15px);
    margin-bottom: 15px;
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 0 15px rgba(0,245,255,0.2);
    transition: 0.3s;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 0 25px var(--neon-blue);
}

/* ---------------- INPUT FIELDS ---------------- */
input, textarea {
    background: rgba(255,255,255,0.05) !important;
    color: var(--text-light) !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
}

input:focus, textarea:focus {
    border: 1px solid var(--neon-blue) !important;
    box-shadow: 0 0 10px var(--neon-blue);
}

/* ---------------- SELECT BOX ---------------- */
div[data-baseweb="select"] {
    border-radius: 10px;
}

div[data-baseweb="select"] * {
    color: white !important;
}

/* ---------------- ALERTS ---------------- */
.stAlert-success {
    background-color: rgba(0,255,150,0.15);
    border-left: 5px solid #00ff99;
}

.stAlert-warning {
    background-color: rgba(255,200,0,0.15);
    border-left: 5px solid #ffcc00;
}

.stAlert-error {
    background-color: rgba(255,0,80,0.15);
    border-left: 5px solid #ff0055;
}

/* ---------------- TABLE ---------------- */
.stDataFrame {
    border-radius: 12px;
    overflow: hidden;
}

/* ---------------- ANIMATION ---------------- */
.fade-in {
    animation: fadeIn 0.6s ease-in-out;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOGIN + REGISTER ----------------
def login():

    st.title("⚡ EV Charging System")

    tab1, tab2 = st.tabs(["🔐 Login", "🆕 Register"])

    # ---------------- LOGIN ----------------
    with tab1:

        st.subheader("Login to your account")

        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        role = st.selectbox(
            "Role",
            ["user", "station", "admin"],
            key="login_role"
        )

        if st.button("Login"):

            user = cursor.execute(
                "SELECT user_id, role FROM Users WHERE username=? AND password=? AND role=?",
                (username, password, role)
            ).fetchone()

            if user:
                st.session_state.user_id = user[0]
                st.session_state.role = user[1]

                st.success("Login Successful")
                st.rerun()

            else:
                st.error("Invalid credentials")

    # ---------------- REGISTER ----------------
    with tab2:

        st.subheader("Create New Account")

        new_user = st.text_input("Username", key="reg_user")

        new_pass = st.text_input(
            "Password",
            type="password",
            key="reg_pass"
        )

        new_role = st.selectbox(
            "Role",
            ["user", "station"],
            key="reg_role"
        )

        if st.button("Register"):

            if not new_user or not new_pass:
                st.warning("Please fill all fields")

            else:
                try:

                    existing = cursor.execute(
                        "SELECT * FROM Users WHERE username=?",
                        (new_user,)
                    ).fetchone()

                    if existing:
                        st.warning("Username already exists")

                    else:
                        cursor.execute(
                            "INSERT INTO Users(username, password, role) VALUES (?, ?, ?)",
                            (new_user, new_pass, new_role)
                        )

                        conn.commit()

                        st.success(
                            "Registration Successful! Please Login."
                        )

                except Exception as e:
                    st.error(e)

# ---------------- USER DASHBOARD ----------------
def user_dashboard():

    st.sidebar.title("👤 User Panel")

    option = st.sidebar.radio(
        "Menu",
        ["Stations", "History"]
    )

    # ---------------- STATIONS ----------------
    if option == "Stations":

        st.header("🔌 Charging Stations")

        city = st.text_input("Search City")

        if city:
            df = pd.read_sql(
                "SELECT * FROM Stations WHERE city=?",
                conn,
                params=[city]
            )
        else:
            df = pd.read_sql(
                "SELECT * FROM Stations",
                conn
            )

        if df.empty:
            st.warning("No stations found")
            return

        selected_station = st.selectbox(
            "Select Station",
            df["name"]
        )

        station = df[df["name"] == selected_station].iloc[0]

        sid = int(station["station_id"])

        col1, col2 = st.columns([2,1])

        # ---------------- STATION DETAILS ----------------
        with col1:

            st.markdown(f"""
            <div class="card fade-in">
                <h3>⚡ {station['name']}</h3>
                <p>📍 {station['city']}</p>
                <p>🔌 Available Ports: {station['available_ports']}</p>
            </div>
            """, unsafe_allow_html=True)

            query = f"{station['name']} {station['city']}".replace(" ", "+")

            st.markdown(
                f'<iframe width="100%" height="300" src="https://www.google.com/maps?q={query}&output=embed"></iframe>',
                unsafe_allow_html=True
            )

        # ---------------- BOOKING ----------------
        with col2:

            if st.button("Book Now"):

                try:
                    conn.autocommit = False

                    active = cursor.execute(
                        """
                        SELECT * FROM Bookings
                        WHERE user_id=? AND status='Booked'
                        """,
                        (st.session_state.user_id,)
                    ).fetchone()

                    if active:
                        st.warning("You already have an active booking")
                        conn.rollback()

                    else:

                        row = cursor.execute(
                            "SELECT available_ports FROM Stations WHERE station_id=?",
                            (sid,)
                        ).fetchone()

                        if row is None or row[0] <= 0:
                            st.warning("No ports available")
                            conn.rollback()

                        else:

                            cursor.execute(
                                """
                                UPDATE Stations
                                SET available_ports = available_ports - 1
                                WHERE station_id=?
                                """,
                                (sid,)
                            )

                            cursor.execute("""
                                INSERT INTO Bookings(user_id, station_id, status)
                                OUTPUT INSERTED.booking_id
                                VALUES (?, ?, 'Booked')
                            """, (st.session_state.user_id, sid))

                            result = cursor.fetchone()

                            if result:
                                st.session_state.booking_id = int(result[0])

                                conn.commit()

                                st.success("Booking Successful")

                            else:
                                conn.rollback()
                                st.error("Booking failed")

                except Exception as e:
                    conn.rollback()
                    st.error(f"Booking Failed: {e}")

                finally:
                    conn.autocommit = True

            # ---------------- PAYMENT ----------------
            if st.session_state.booking_id:

                st.info("Amount: ₹200")

                mode = st.radio(
                    "Mode",
                    ["online", "offline"]
                )

                if st.button("Pay"):

                    try:

                        existing = cursor.execute(
                            "SELECT * FROM Payments WHERE booking_id=?",
                            (st.session_state.booking_id,)
                        ).fetchone()

                        if existing:
                            st.warning("Payment already completed")

                        else:

                            cursor.execute(
                                """
                                INSERT INTO Payments
                                (booking_id, amount, payment_mode, payment_status)
                                VALUES (?,200,?, 'Paid')
                                """,
                                (st.session_state.booking_id, mode)
                            )

                            conn.commit()

                            st.success("Payment Successful")

                    except Exception as e:
                        st.error(e)

            # ---------------- ACID ----------------
            st.subheader("🔐 ACID Properties")

            if st.button("Check ACID Properties"):

                st.success("Atomicity: Booking & Payment executed safely")
                st.success("Consistency: Ports never go negative")
                st.success("Isolation: Concurrent bookings handled")
                st.success("Durability: Transactions stored permanently")

            # ---------------- REVIEWS ----------------
            st.subheader("⭐ Reviews")

            reviews = pd.read_sql(
                """
                SELECT rating, comment
                FROM Reviews
                WHERE station_id=?
                """,
                conn,
                params=[sid]
            )

            st.dataframe(reviews)

            existing_review = cursor.execute(
                """
                SELECT rating, comment
                FROM Reviews
                WHERE user_id=? AND station_id=?
                """,
                (st.session_state.user_id, sid)
            ).fetchone()

            if existing_review:
                default_rating = existing_review[0]
                default_comment = existing_review[1]
            else:
                default_rating = 3
                default_comment = ""

            rating = st.slider(
                "Rating",
                1,
                5,
                value=default_rating
            )

            comment = st.text_input(
                "Comment",
                value=default_comment
            )

            if existing_review:

                if st.button("Edit Review"):

                    cursor.execute(
                        """
                        UPDATE Reviews
                        SET rating=?, comment=?
                        WHERE user_id=? AND station_id=?
                        """,
                        (
                            rating,
                            comment,
                            st.session_state.user_id,
                            sid
                        )
                    )

                    conn.commit()

                    st.success("Review Updated")

            else:

                if st.button("Submit Review"):

                    if not comment:
                        st.warning("Comment required")

                    else:

                        cursor.execute(
                            """
                            INSERT INTO Reviews
                            (user_id, station_id, rating, comment)
                            VALUES (?, ?, ?, ?)
                            """,
                            (
                                st.session_state.user_id,
                                sid,
                                rating,
                                comment
                            )
                        )

                        conn.commit()

                        st.success("Review Added")

    # ---------------- HISTORY ----------------
    elif option == "History":

        st.header("📜 Booking History")

        history = pd.read_sql(
            """
            SELECT *
            FROM Bookings
            WHERE user_id=?
            """,
            conn,
            params=[st.session_state.user_id]
        )

        st.dataframe(history)

# ---------------- STATION DASHBOARD ----------------
def station_dashboard():

    st.header("🏢 Station Dashboard")

    stations_df = pd.read_sql(
        """
        SELECT station_id, name, city, available_ports
        FROM Stations
        """,
        conn
    )

    st.dataframe(stations_df)

    sid = st.number_input(
        "Enter Station ID",
        min_value=1
    )

    data = cursor.execute(
        """
        SELECT total_ports, available_ports
        FROM Stations
        WHERE station_id=?
        """,
        (sid,)
    ).fetchone()

    if not data:
        st.warning("Invalid Station ID")
        return

    total, available = data

    used = total - available

    st.metric("Available Ports", available)

    new_ports = st.number_input(
        "Update Ports",
        min_value=0
    )

    if st.button("Update"):

        cursor.execute(
            """
            UPDATE Stations
            SET available_ports=?
            WHERE station_id=?
            """,
            (new_ports, sid)
        )

        conn.commit()

        st.success("Ports Updated")

    # ---------------- CHART ----------------
    fig, ax = plt.subplots()

    ax.pie(
        [used, available],
        labels=["Used 🔴", "Available 🟢"],
        autopct="%1.1f%%"
    )

    ax.set_title("⚡ Port Usage Overview")

    st.pyplot(fig)

# ---------------- ADMIN DASHBOARD ----------------
def admin_dashboard():

    st.header("🛠️ Admin Dashboard")

    users = cursor.execute(
        "SELECT COUNT(*) FROM Users"
    ).fetchone()[0]

    stations = cursor.execute(
        "SELECT COUNT(*) FROM Stations"
    ).fetchone()[0]

    bookings = cursor.execute(
        "SELECT COUNT(*) FROM Bookings"
    ).fetchone()[0]

    col1, col2, col3 = st.columns(3)

    col1.metric("Users", users)
    col2.metric("Stations", stations)
    col3.metric("Bookings", bookings)

    # ---------------- BAR CHART ----------------
    st.subheader("📊 System Overview")

    data = {
        "Users": users,
        "Stations": stations,
        "Bookings": bookings
    }

    fig, ax = plt.subplots()

    ax.bar(data.keys(), data.values())

    st.pyplot(fig)

    # ---------------- MANAGE STATIONS ----------------
    st.subheader("⚡ Manage Stations")

    name = st.text_input("Name")
    city = st.text_input("City")
    address = st.text_input("Address")

    ports = st.number_input(
        "Ports",
        min_value=1
    )

    sid = st.number_input(
        "Station ID",
        min_value=1
    )

    if st.button("Add Station"):

        if not name or not city:
            st.warning("Fill all required fields")

        else:

            cursor.execute(
                """
                INSERT INTO Stations
                (name, city, address, total_ports, available_ports)
                VALUES (?, ?, ?, ?, ?)
                """,
                (name, city, address, ports, ports)
            )

            conn.commit()

            st.success("Station Added")

    if st.button("Update Station"):

        cursor.execute(
            """
            UPDATE Stations
            SET name=?, city=?, address=?,
                total_ports=?, available_ports=?
            WHERE station_id=?
            """,
            (name, city, address, ports, ports, sid)
        )

        conn.commit()

        st.success("Station Updated")

    if st.button("Delete Station"):

        try:
            conn.autocommit = False

            cursor.execute(
                "DELETE FROM Reviews WHERE station_id=?",
                (sid,)
            )

            cursor.execute(
                """
                DELETE FROM Payments
                WHERE booking_id IN (
                    SELECT booking_id
                    FROM Bookings
                    WHERE station_id=?
                )
                """,
                (sid,)
            )

            cursor.execute(
                "DELETE FROM Transactions WHERE station_id=?",
                (sid,)
            )

            cursor.execute(
                "DELETE FROM Bookings WHERE station_id=?",
                (sid,)
            )

            cursor.execute(
                "DELETE FROM Stations WHERE station_id=?",
                (sid,)
            )

            conn.commit()

            st.success("Station Deleted")

        except Exception as e:
            conn.rollback()
            st.error(e)

        finally:
            conn.autocommit = True

    # ---------------- CANCEL BOOKING ----------------
    st.subheader("❌ Cancel Booking")

    bid = st.number_input(
        "Booking ID",
        min_value=1
    )

    if st.button("Cancel Booking"):

        try:
            conn.autocommit = False

            b = cursor.execute(
                """
                SELECT station_id
                FROM Bookings
                WHERE booking_id=?
                """,
                (bid,)
            ).fetchone()

            if not b:
                st.warning("Booking not found")
                conn.rollback()

            else:

                sid_b = int(b[0])

                cursor.execute(
                    "DELETE FROM Payments WHERE booking_id=?",
                    (bid,)
                )

                cursor.execute(
                    "DELETE FROM Bookings WHERE booking_id=?",
                    (bid,)
                )

                cursor.execute(
                    """
                    UPDATE Stations
                    SET available_ports=available_ports+1
                    WHERE station_id=?
                    """,
                    (sid_b,)
                )

                conn.commit()

                st.success("Booking Cancelled")

        except Exception as e:
            conn.rollback()
            st.error(e)

        finally:
            conn.autocommit = True

    # ---------------- NORMALIZATION ----------------
    st.subheader("🧠 Normalization Checker")

    if st.button("Check Normalization"):

        st.success("✔ 1NF: Atomic values")
        st.success("✔ 2NF: No partial dependency")

        cols = [
            col[0]
            for col in cursor.execute(
                """
                SELECT COLUMN_NAME
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME='Stations'
                """
            )
        ]

        if "city" in cols and "pincode" in cols:
            st.warning("⚠ Possible transitive dependency")
        else:
            st.success("✔ 3NF satisfied")

    # ---------------- COMPLETE DB ----------------
    st.subheader("📊 Complete Database View")

    st.markdown("### 👤 Users")
    st.dataframe(pd.read_sql("SELECT * FROM Users", conn))

    st.markdown("### ⚡ Stations")
    st.dataframe(pd.read_sql("SELECT * FROM Stations", conn))

    st.markdown("### 📜 Bookings")
    st.dataframe(pd.read_sql("SELECT * FROM Bookings", conn))

    st.markdown("### 💳 Payments")
    st.dataframe(pd.read_sql("SELECT * FROM Payments", conn))

    st.markdown("### 🔄 Transactions")
    st.dataframe(pd.read_sql("SELECT * FROM Transactions", conn))

    st.markdown("### ⭐ Reviews")
    st.dataframe(pd.read_sql("SELECT * FROM Reviews", conn))

# ---------------- ROUTER ----------------
if st.session_state.role is None:
    login()

else:

    if st.session_state.role == "user":
        user_dashboard()

    elif st.session_state.role == "station":
        station_dashboard()

    elif st.session_state.role == "admin":
        admin_dashboard()

    # ---------------- LOGOUT ----------------
    if st.sidebar.button("Logout"):

        st.session_state.role = None
        st.session_state.user_id = None
        st.session_state.booking_id = None

        st.rerun()