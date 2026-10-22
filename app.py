import os
import random
from datetime import datetime
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium

# ---------------------------------------------------------
# 1. PAGE SETUP
# ---------------------------------------------------------
st.set_page_config(
    page_title="SunLoop — Solar Energy Sharing",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------
# 2. LOCAL CSV FLAT DATA MANAGEMENT
# ---------------------------------------------------------
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
SOLAR_CSV = os.path.join(DATA_DIR, "solar_data.csv")
STATIONS_CSV = os.path.join(DATA_DIR, "stations.csv")
BOOKINGS_CSV = os.path.join(DATA_DIR, "bookings.csv")

# Generic neighborhood coordinates
HOST_LAT = 12.8731
HOST_LON = 80.2209

def ensure_data_files():
    """Ensure data directory and required CSV flat files exist."""
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(SOLAR_CSV):
        solar_data = [
            {"Hour": "06:00", "Generation_kW": 0.5, "Consumption_kW": 1.2, "Surplus_kW": 0.0},
            {"Hour": "08:00", "Generation_kW": 2.8, "Consumption_kW": 1.6, "Surplus_kW": 1.2},
            {"Hour": "10:00", "Generation_kW": 6.1, "Consumption_kW": 2.0, "Surplus_kW": 4.1},
            {"Hour": "12:00", "Generation_kW": 7.8, "Consumption_kW": 2.3, "Surplus_kW": 5.5},
            {"Hour": "14:00", "Generation_kW": 7.1, "Consumption_kW": 2.2, "Surplus_kW": 4.9},
            {"Hour": "16:00", "Generation_kW": 3.9, "Consumption_kW": 1.9, "Surplus_kW": 2.0},
            {"Hour": "18:00", "Generation_kW": 0.4, "Consumption_kW": 2.0, "Surplus_kW": 0.0},
        ]
        pd.DataFrame(solar_data).to_csv(SOLAR_CSV, index=False)

    if not os.path.exists(STATIONS_CSV):
        stations_data = [
            {"ID": "HUB-01", "Name": "Central EV Station", "Type": "EV Station", "Latitude": 12.8750, "Longitude": 80.2240, "Demand_kW": 15.0, "Dynamic_Rate_INR": 5.20, "Status": "Available"},
            {"ID": "HUB-02", "Name": "City Hub FastCharge", "Type": "EV Station", "Latitude": 12.8715, "Longitude": 80.2190, "Demand_kW": 10.0, "Dynamic_Rate_INR": 4.80, "Status": "Available"},
            {"ID": "HUB-03", "Name": "Local Artisan Bakery", "Type": "Small Business", "Latitude": 12.8790, "Longitude": 80.2260, "Demand_kW": 6.5, "Dynamic_Rate_INR": 5.50, "Status": "Available"},
            {"ID": "HUB-04", "Name": "Community Laundromat", "Type": "Small Business", "Latitude": 12.8680, "Longitude": 80.2150, "Demand_kW": 4.0, "Dynamic_Rate_INR": 5.00, "Status": "Available"},
            {"ID": "HUB-05", "Name": "GreenRide 2-Wheeler Hub", "Type": "EV Station", "Latitude": 12.8820, "Longitude": 80.2280, "Demand_kW": 8.0, "Dynamic_Rate_INR": 4.50, "Status": "Available"},
        ]
        pd.DataFrame(stations_data).to_csv(STATIONS_CSV, index=False)

    if not os.path.exists(BOOKINGS_CSV):
        bookings_data = [
            {"Booking_ID": "SL-101", "Timestamp": "2026-10-22 10:30", "Customer_Name": "Local EV Driver", "Station_Name": "Central EV Station", "Units_kWh": 12.5, "Rate_Per_kWh": 5.20, "Total_Amount_INR": 65.00, "Status": "Confirmed"},
            {"Booking_ID": "SL-102", "Timestamp": "2026-10-22 11:45", "Customer_Name": "Delivery Van", "Station_Name": "City Hub FastCharge", "Units_kWh": 18.0, "Rate_Per_kWh": 4.80, "Total_Amount_INR": 86.40, "Status": "Confirmed"},
        ]
        pd.DataFrame(bookings_data).to_csv(BOOKINGS_CSV, index=False)

ensure_data_files()

def get_solar_data():
    ensure_data_files()
    return pd.read_csv(SOLAR_CSV)

def get_stations():
    ensure_data_files()
    return pd.read_csv(STATIONS_CSV)

def get_bookings():
    ensure_data_files()
    return pd.read_csv(BOOKINGS_CSV)

def save_new_booking(record):
    ensure_data_files()
    df = get_bookings()
    df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
    df.to_csv(BOOKINGS_CSV, index=False)

# ---------------------------------------------------------
# 3. CSS: HIDE DEVELOPER BAR & 3D POP THEME
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

    /* 1. Hide Streamlit top header, deploy button, hamburger menu, and footer */
    #MainMenu {visibility: hidden !important;}
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    [data-testid="stHeader"] {display: none !important;}
    [data-testid="stToolbar"] {display: none !important;}
    .stDeployButton {display: none !important;}
    #stDecoration {display: none !important;}

    /* 2. Warm mild yellow/cream background & rich black typography */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #FEF9E7 !important;
        color: #111827 !important;
        font-family: 'Inter', sans-serif !important;
    }

    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 3rem !important;
        max-width: 1140px !important;
    }

    h1, h2, h3, h4 {
        font-family: 'Outfit', sans-serif !important;
        color: #111827 !important;
        font-weight: 700 !important;
    }

    /* 3. Clean neutral hero header */
    .hero-box {
        background: #FFFFFF;
        border: 2px solid rgba(255, 107, 0, 0.2);
        border-radius: 20px;
        padding: 1.5rem 1.8rem;
        margin-bottom: 1.3rem;
        box-shadow: 0 10px 25px -5px rgba(255, 107, 0, 0.15), 0 8px 10px -6px rgba(0, 0, 0, 0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 1rem;
    }

    .hero-title {
        font-family: 'Outfit', sans-serif;
        font-size: 2.2rem;
        font-weight: 800;
        color: #111827;
        margin: 0;
        line-height: 1.15;
    }

    .hero-subtitle {
        color: #4B5563;
        font-size: 0.95rem;
        margin-top: 0.25rem;
        font-weight: 500;
    }

    .status-pill {
        background: #ECFDF5;
        color: #065F46;
        border: 1.5px solid #A7F3D0;
        padding: 0.45rem 1.1rem;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.88rem;
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        box-shadow: 0 4px 10px rgba(16, 185, 129, 0.15);
    }

    /* 4. 3D Pop Elevated Cards */
    .pop-card {
        background: #FFFFFF;
        border: 1.5px solid rgba(255, 107, 0, 0.16);
        border-radius: 18px;
        padding: 1.4rem 1.5rem;
        box-shadow: 0 10px 25px -5px rgba(255, 107, 0, 0.18), 0 8px 10px -6px rgba(0, 0, 0, 0.08);
        transition: all 0.25s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        margin-bottom: 1.1rem;
    }

    .pop-card:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 18px 30px -5px rgba(255, 107, 0, 0.30), 0 12px 16px -6px rgba(0, 0, 0, 0.12);
        border-color: #FF6B00;
    }

    .pop-card-orange {
        background: linear-gradient(135deg, #FFFFFF 0%, #FFF7ED 100%);
        border: 2px solid #FF6B00;
    }

    .metric-caption {
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        color: #6B7280;
        letter-spacing: 0.04em;
    }

    .metric-number {
        font-family: 'Outfit', sans-serif;
        font-size: 2.3rem;
        font-weight: 800;
        color: #111827;
        margin: 0.25rem 0;
    }

    .metric-number.orange {
        color: #FF6B00;
    }

    .metric-subtext {
        font-size: 0.85rem;
        color: #6B7280;
    }

    /* 5. Clean Navigation Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.6rem;
        background-color: transparent;
        border-bottom: 2px solid rgba(255, 107, 0, 0.18);
        margin-bottom: 1.2rem;
    }

    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        background-color: #FFFFFF;
        border: 1.5px solid rgba(255, 107, 0, 0.16);
        border-radius: 12px 12px 0 0;
        color: #4B5563;
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        font-size: 1rem;
        padding: 0 1.5rem;
        transition: all 0.2s ease;
    }

    .stTabs [aria-selected="true"] {
        background: #FFF5EB !important;
        border-color: #FF6B00 !important;
        border-bottom: 3.5px solid #FF6B00 !important;
        color: #FF6B00 !important;
    }

    /* 6. Vibrant Solar-Orange Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #FF8800 0%, #FF6B00 100%) !important;
        color: #FFFFFF !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.75rem 2rem !important;
        box-shadow: 0 8px 20px rgba(255, 107, 0, 0.35) !important;
        transition: all 0.25s ease !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 12px 25px rgba(255, 107, 0, 0.45) !important;
        color: #FFFFFF !important;
    }

    /* 7. 3D Voucher Confirmation Modal */
    .voucher-card {
        background: #FFFFFF;
        border: 2px dashed #FF6B00;
        border-radius: 18px;
        padding: 1.6rem;
        text-align: center;
        box-shadow: 0 14px 32px rgba(255, 107, 0, 0.25);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# 4. CONFIRMATION VOUCHER POPUP DIALOG
# ---------------------------------------------------------
dialog_decorator = getattr(st, "dialog", getattr(st, "experimental_dialog", None))

def render_qr_badge():
    """Generates a clean SVG QR authorization badge."""
    return """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="130" height="130" style="margin: 0.8rem auto; display: block;">
        <rect width="100" height="100" fill="#FEF9E7" rx="8" stroke="#FF6B00" stroke-width="2"/>
        <rect x="12" y="12" width="22" height="22" fill="#FF6B00" rx="2"/>
        <rect x="66" y="12" width="22" height="22" fill="#FF6B00" rx="2"/>
        <rect x="12" y="66" width="22" height="22" fill="#FF6B00" rx="2"/>
        <rect x="17" y="17" width="12" height="12" fill="#FEF9E7"/>
        <rect x="71" y="17" width="12" height="12" fill="#FEF9E7"/>
        <rect x="17" y="71" width="12" height="12" fill="#FEF9E7"/>
        <circle cx="50" cy="50" r="10" fill="#FF6B00"/>
        <circle cx="50" cy="50" r="5" fill="#FEF9E7"/>
        <rect x="42" y="20" width="8" height="8" fill="#111827"/>
        <rect x="70" y="44" width="8" height="8" fill="#111827"/>
        <rect x="44" y="70" width="8" height="8" fill="#111827"/>
    </svg>
    """

if dialog_decorator:
    @dialog_decorator("⚡ Solar Booking Confirmed!")
    def show_voucher_modal(booking):
        st.markdown(
            f"""
            <div class="voucher-card">
                <div style="font-size: 2.2rem;">🎉</div>
                <h3 style="margin: 0.2rem 0; color: #FF6B00; font-family: 'Outfit';">Solar Energy Reservation Voucher</h3>
                <p style="color: #6B7280; font-size: 0.88rem; margin-bottom: 1rem;">
                    Booking Code: <strong>{booking['Booking_ID']}</strong> &bull; {booking['Timestamp']}
                </p>
                <div style="background: #FFF9F2; border-radius: 12px; padding: 1rem; text-align: left; font-size: 0.95rem; margin-bottom: 1rem; border: 1px solid rgba(255,107,0,0.18);">
                    <p style="margin: 0.3rem 0;">🏢 <strong>Consumer Station:</strong> {booking['Station_Name']}</p>
                    <p style="margin: 0.3rem 0;">⚡ <strong>Energy Units Booked:</strong> <span style="color:#FF6B00; font-weight:700;">{booking['Units_kWh']} kWh</span></p>
                    <p style="margin: 0.3rem 0;">💵 <strong>Total Paid:</strong> <strong style="color:#059669; font-size: 1.15rem;">₹{booking['Total_Amount_INR']:.2f}</strong> (@ ₹{booking['Rate_Per_kWh']:.2f}/kWh)</p>
                    <p style="margin: 0.3rem 0;">🏷️ <strong>Status:</strong> <span style="color:#059669; font-weight:700;">● Confirmed & Dispatched</span></p>
                </div>
                {render_qr_badge()}
                <p style="font-size: 0.8rem; color: #6B7280; margin-top: 0.2rem;">
                    Present this verification badge at the station to initiate energy transfer.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Done", use_container_width=True):
            st.rerun()
else:
    def show_voucher_modal(booking):
        st.success(f"Booking {booking['Booking_ID']} Confirmed! Total: ₹{booking['Total_Amount_INR']:.2f}")

# ---------------------------------------------------------
# 5. NEUTRAL HEADER
# ---------------------------------------------------------
st.markdown(
    """
    <div class="hero-box">
        <div>
            <div class="hero-title">☀️ SunLoop</div>
            <div class="hero-subtitle">
                <strong>Where Wasted Watts Find Worth</strong> &bull; Hyperlocal Peer-to-Peer Solar Energy Sharing
            </div>
        </div>
        <div>
            <span class="status-pill">
                🟢 Solar Inverter Connected & Ready
            </span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# 6. SIMPLIFIED 3-STEP NAVIGATION
# ---------------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "☀️ Solar Energy Status",
    "📍 Energy Map & Booking",
    "💰 Cost & Savings Calculator"
])

# =========================================================
# TAB 1: SOLAR ENERGY STATUS
# =========================================================
with tab1:
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            """
            <div class="pop-card">
                <div class="metric-caption">Total Solar Generated (kW)</div>
                <div class="metric-number">7.5 <span style="font-size: 1.2rem; font-weight: 600;">kW</span></div>
                <div class="metric-subtext">Current real-time rooftop solar generation</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="pop-card">
                <div class="metric-caption">Household Usage (kW)</div>
                <div class="metric-number">2.5 <span style="font-size: 1.2rem; font-weight: 600;">kW</span></div>
                <div class="metric-subtext">Active home appliance and base consumption</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            """
            <div class="pop-card pop-card-orange">
                <div class="metric-caption" style="color: #FF6B00;">Extra Power Available (kW)</div>
                <div class="metric-number orange">5.0 <span style="font-size: 1.2rem; font-weight: 600;">kW</span></div>
                <div class="metric-subtext" style="color: #FF6B00; font-weight: 600;">Surplus energy available for local sharing</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Clean Hourly Line Chart
    st.markdown(
        """
        <div class="pop-card" style="margin-top: 0.5rem;">
            <h4 style="margin: 0 0 0.4rem 0;">📊 Hourly Generation vs. Household Consumption</h4>
            <p style="color: #6B7280; font-size: 0.88rem; margin: 0 0 1rem 0;">
                Excess solar energy peaks during sunny afternoon hours (11:00 AM – 3:00 PM), creating surplus clean power for nearby consumers.
            </p>
        """,
        unsafe_allow_html=True,
    )

    solar_df = get_solar_data()
    chart_view = solar_df.rename(columns={
        "Generation_kW": "Solar Generation (kW)",
        "Consumption_kW": "Household Usage (kW)",
        "Surplus_kW": "Extra Power Available (kW)"
    }).set_index("Hour")

    st.line_chart(
        chart_view[["Solar Generation (kW)", "Household Usage (kW)", "Extra Power Available (kW)"]],
        color=["#FF8800", "#6B7280", "#10B981"],
        height=320,
    )
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# TAB 2: ENERGY MAP & BOOKING
# =========================================================
with tab2:
    stations_df = get_stations()

    st.markdown(
        """
        <div class="pop-card" style="margin-bottom: 0.8rem;">
            <h3 style="margin: 0 0 0.2rem 0;">📍 Local Energy Map</h3>
            <p style="margin: 0; color: #6B7280; font-size: 0.9rem;">
                Nearby consumer stations and charging points ready to receive shared rooftop solar power.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Interactive Folium Map
    m = folium.Map(location=[HOST_LAT, HOST_LON], zoom_start=15, tiles="OpenStreetMap")

    # Host rooftop marker
    folium.Marker(
        location=[HOST_LAT, HOST_LON],
        tooltip="☀️ Host Rooftop (5.0 kW Extra Available)",
        popup="<strong>Host Rooftop Array</strong><br>5.0 kW Extra Energy Available",
        icon=folium.Icon(color="orange", icon="sun", prefix="fa"),
    ).add_to(m)

    # 5 Nearby Consumer Hub Markers
    for _, row in stations_df.iterrows():
        popup_html = f"<strong>{row['Name']}</strong><br>Category: {row['Type']}<br>Demand: {row['Demand_kW']} kW<br>Rate: ₹{row['Dynamic_Rate_INR']:.2f}/kWh"
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            tooltip=f"{row['Name']} ({row['Demand_kW']} kW Demand)",
            popup=popup_html,
            icon=folium.Icon(color="green" if "EV" in row["Type"] else "blue", icon="bolt", prefix="fa"),
        ).add_to(m)

    st_folium(m, width="100%", height=380)

    # Simple Booking Card Below Map
    st.markdown(
        """
        <div class="pop-card pop-card-orange" style="margin-top: 1rem;">
            <h3 style="margin: 0 0 0.5rem 0; color: #FF6B00;">⚡ Book Energy Transfer</h3>
            <p style="margin: 0 0 1rem 0; color: #4B5563; font-size: 0.92rem;">
                Select a local station, set the energy units to transfer, and confirm your booking.
            </p>
        """,
        unsafe_allow_html=True,
    )

    b_col1, b_col2 = st.columns([3, 2])

    with b_col1:
        station_labels = [
            f"{row['Name']} — ₹{row['Dynamic_Rate_INR']:.2f}/kWh ({row['Type']})"
            for _, row in stations_df.iterrows()
        ]
        chosen_label = st.selectbox("Select Consumer / Station", options=station_labels, index=0)
        chosen_idx = station_labels.index(chosen_label)
        selected_station = stations_df.iloc[chosen_idx]

        units_to_book = st.slider(
            "Energy Units to Book (kWh)",
            min_value=1.0,
            max_value=30.0,
            value=12.0,
            step=1.0,
            help="1 unit = 1 kilowatt-hour (kWh) of clean solar power."
        )

    with b_col2:
        unit_rate = float(selected_station["Dynamic_Rate_INR"])
        total_price = units_to_book * unit_rate
        grid_reference_cost = units_to_book * 8.50  # standard grid tariff comparison
        direct_savings = grid_reference_cost - total_price

        st.markdown(
            f"""
            <div style="background: #FFFFFF; border-radius: 14px; padding: 1.1rem; border: 1.5px solid rgba(255,107,0,0.25);">
                <div style="font-size: 0.85rem; color: #6B7280; font-weight: 700; text-transform: uppercase;">Transaction Preview</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: #111827; margin: 0.3rem 0;">₹{total_price:.2f}</div>
                <div style="font-size: 0.85rem; color: #059669; font-weight: 700;">
                    🎉 Money Saved by EV Buyer: ₹{direct_savings:.2f} vs Grid
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        if st.button("Book Solar Slot", use_container_width=True):
            new_id = f"SL-{random.randint(100, 999)}"
            booking_record = {
                "Booking_ID": new_id,
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Customer_Name": "Local Consumer",
                "Station_Name": selected_station["Name"],
                "Units_kWh": float(units_to_book),
                "Rate_Per_kWh": float(unit_rate),
                "Total_Amount_INR": round(float(total_price), 2),
                "Status": "Confirmed",
            }
            save_new_booking(booking_record)
            st.balloons()
            show_voucher_modal(booking_record)

    st.markdown("</div>", unsafe_allow_html=True)

    # Recent Transactions Ledger
    with st.expander("📋 View Bookings Ledger"):
        ledger_df = get_bookings()
        st.dataframe(
            ledger_df[["Booking_ID", "Timestamp", "Station_Name", "Units_kWh", "Rate_Per_kWh", "Total_Amount_INR", "Status"]],
            use_container_width=True,
        )

# =========================================================
# TAB 3: COST & SAVINGS CALCULATOR
# =========================================================
with tab3:
    st.markdown(
        """
        <div class="pop-card">
            <h3 style="margin: 0 0 0.3rem 0;">💰 Cost & Savings Calculator</h3>
            <p style="margin: 0 0 1.2rem 0; color: #6B7280; font-size: 0.92rem;">
                Estimate monthly income for solar owners and direct savings for EV drivers based on daily traded units.
            </p>
        """,
        unsafe_allow_html=True,
    )

    s1, s2 = st.columns(2)
    with s1:
        daily_kwh = st.slider(
            "Daily Energy Shared (kWh)",
            min_value=5.0,
            max_value=60.0,
            value=25.0,
            step=1.0,
            help="Average units of excess solar power shared each day."
        )
    with s2:
        standard_rate = st.slider(
            "Standard Electricity Rate (₹/kWh)",
            min_value=6.00,
            max_value=12.00,
            value=8.50,
            step=0.25,
            help="Standard retail utility electricity tariff."
        )

    st.markdown("</div>", unsafe_allow_html=True)

    shared_solar_tariff = 5.00  # Fair shared solar rate
    monthly_owner_earnings = daily_kwh * shared_solar_tariff * 30
    monthly_ev_savings = daily_kwh * (standard_rate - shared_solar_tariff) * 30

    # 2 Clean Financial Summary Cards (No emissions metrics)
    sc1, sc2 = st.columns(2)

    with sc1:
        st.markdown(
            f"""
            <div class="pop-card pop-card-orange">
                <div class="metric-caption" style="color: #FF6B00;">Monthly Earnings for Solar Owner (₹)</div>
                <div class="metric-number orange">₹{monthly_owner_earnings:,.0f} <span style="font-size: 1rem; color: #6B7280;">/ month</span></div>
                <div class="metric-subtext">Annual Projected Income: <strong>₹{monthly_owner_earnings * 12:,.0f}</strong></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with sc2:
        st.markdown(
            f"""
            <div class="pop-card">
                <div class="metric-caption" style="color: #059669;">Monthly Savings for EV Driver (₹)</div>
                <div class="metric-number" style="color: #059669;">₹{monthly_ev_savings:,.0f} <span style="font-size: 1rem; color: #6B7280;">/ month</span></div>
                <div class="metric-subtext">Annual Money Saved: <strong>₹{monthly_ev_savings * 12:,.0f}</strong> vs standard grid</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ---------------------------------------------------------
# 7. FOOTER
# ---------------------------------------------------------
st.markdown(
    """
    <div style="text-align: center; margin-top: 2.5rem; color: #9CA3AF; font-size: 0.85rem;">
        ☀️ <strong>SunLoop</strong> &bull; Hyperlocal Solar Energy Sharing Platform
    </div>
    """,
    unsafe_allow_html=True,
)
