# ☀️ SunLoop — Where Wasted Watts Find Worth

**Hyperlocal Solar Energy Sharing Platform**

---

## 🌟 Overview
**SunLoop** is an intuitive peer-to-peer (P2P) solar energy sharing web application that connects rooftop solar owners with nearby electric vehicle (EV) charging stations and local businesses.

During peak sunny hours, residential solar arrays often produce more electricity than the home consumes. SunLoop enables solar owners to monetize this surplus clean energy by sharing it directly with local consumers at a fair rate below standard grid prices.

---

## 🌐 Live Production Application

You can access the live web application from any browser on any device:

👉 **[https://sunloop-nexus.streamlit.app](https://sunloop-nexus.streamlit.app)**

---

## 🚀 3-Step Navigation

### 1. ☀️ Solar Energy Status
- **3 Simple Metric Cards:**
  - **Total Solar Generated (kW):** Real-time rooftop generation (`7.5 kW`).
  - **Household Usage (kW):** Active home appliances and base load (`2.5 kW`).
  - **Extra Power Available (kW):** Net surplus power ready to share (`5.0 kW`, highlighted in solar orange).
- **Daylight Curve Chart:** Clean hourly line chart visualizing generation vs. household consumption across daylight hours (06:00 to 18:00).

### 2. 📍 Energy Map & Booking
- **Interactive Map:** Centered on the local neighborhood showing the host rooftop and 5 nearby consumer stations:
  1. *Central EV Station* (15.0 kW demand @ ₹5.20/kWh)
  2. *City Hub FastCharge* (10.0 kW demand @ ₹4.80/kWh)
  3. *Local Artisan Bakery* (6.5 kW demand @ ₹5.50/kWh)
  4. *Community Laundromat* (4.0 kW demand @ ₹5.00/kWh)
  5. *GreenRide 2-Wheeler Hub* (8.0 kW demand @ ₹4.50/kWh)
- **Direct Booking Card:**
  - Dropdown: Select consumer or charging hub.
  - Slider: Select energy units to book (`1 to 30 kWh`).
  - Real-time comparison showing total cost vs. standard grid reference rate.
  - **"Book Solar Slot"** button launches a 3D confirmation voucher modal with an SVG QR verification badge, transaction code, and celebratory balloons (`st.balloons()`).
  - Automatically appends bookings into the persistent CSV flat file ([`data/bookings.csv`](data/bookings.csv)).

### 3. 💰 Cost & Savings Calculator
- **Two Sliders:**
  - *Daily Energy Shared (kWh)*
  - *Standard Electricity Rate (₹/kWh)*
- **Two Financial Summary Cards:**
  - 💵 **Monthly Earnings for Solar Owner (₹):** Predictable recurring income from shared surplus.
  - 🚗 **Monthly Savings for EV Driver (₹):** Direct pocket savings compared to utility grid retail tariffs.

---

## 🎨 Visual Design
- **Theme Palette:** Warm mild yellow/cream background (`#FEF9E7`), rich black typography (`#111827`), and vibrant solar-orange accents (`#FF6B00`).
- **3D Pop Cards:** Rounded borders (`18px`) with elevated shadows and hover transitions.
- **Distraction-Free UI:** Top Streamlit navigation bar, hamburger menu, deploy button, and footer are completely hidden via custom CSS.

---

## 🛠️ Local Development & Setup

### 1. Clone & install dependencies
```bash
git clone https://github.com/bvkrishmika-cit/SunLoop.git
cd SunLoop
pip install -r requirements.txt
```

### 2. Run the application
```bash
streamlit run app.py
```
Open your browser and navigate to `http://localhost:8501`.
