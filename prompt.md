Markdown
# Comprehensive Project Specification: SunLoop

You are an expert full-stack developer building a complete hackathon web prototype for "SunLoop: Where Wasted Watts Find Worth" (Dexathon 2026, Team: Nexus Navigators, Team ID: DEX26299).

Build the entire project from scratch, generate every single file without placeholders, configure Docker, seed mock datasets, and launch the application on port 8501.

---

## 1. TECH STACK SPECIFICATIONS
- Frontend & UI: Streamlit (Python 3.10+)
- Backend Logic: Pure Python & pandas
- Geospatial Map: Folium with `streamlit-folium` (OpenStreetMap layer centered around Sathyabama / Chennai OMR coordinates: 12.8731° N, 80.2209° E)
- Database: Local CSV flat files (`data/*.csv`)
- Containerization: Docker & Docker Compose

---

## 2. VISUAL THEME & 3D POP DESIGN SPECIFICATIONS
Inject custom CSS using `st.markdown(..., unsafe_allow_html=True)` into `app.py`:
- Background Palette: Warm mild yellow / cream background (`#FFFDF0` or `#FEF9E7`).
- Text & Headings: High-contrast rich charcoal black (`#111827`) for extreme readability.
- Solar Accents: Bright vibrant solar orange (`#FF6B00` / `#FF8800`) for buttons, active state highlights, borders, and metric tags.
- 3D Floating Effect & Cards:
  - Cards must use a crisp white background (`#FFFFFF`), rounded borders (`18px`), and deep elevated dropshadows:
    `box-shadow: 0 10px 25px -5px rgba(255, 107, 0, 0.18), 0 8px 10px -6px rgba(0, 0, 0, 0.08);`
  - Micro-interactions: Cards and buttons must pop forward on hover:
    `transition: all 0.25s cubic-bezier(0.175, 0.885, 0.32, 1.275);`
    `transform: translateY(-4px) scale(1.02);`
    `box-shadow: 0 18px 30px -5px rgba(255, 107, 0, 0.30), 0 12px 16px -6px rgba(0, 0, 0, 0.12);`
- Playful Elements:
  - Add interactive badges, live status pills, and celebratory animations (`st.balloons()`) upon successful slot bookings.
  - Interactive 3D modal/pop-up dialog (`@st.dialog`) for the final slot reservation voucher with simulated QR code verification.

---

## 3. PROJECT DIRECTORY & FILES TO CREATE

Create the following file tree:
SunLoop/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .gitignore
├── README.md
├── app.py
└── data/
├── solar_data.csv
├── stations.csv
└── bookings.csv


### File 1: `requirements.txt`
streamlit>=1.35.0
pandas>=2.0.0
numpy>=1.24.0
folium>=0.16.0
streamlit-folium>=0.20.0


### File 2: `Dockerfile`
```dockerfile
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
File 3: docker-compose.yml
YAML
version: '3.8'

services:
  sunloop-app:
    build: .
    container_name: sunloop_prototype
    ports:
      - "8501:8501"
    volumes:
      - .:/app
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
File 4: .gitignore
__pycache__/
*.py[cod]
*$py.class
.env
.venv
env/
venv/
.streamlit/
File 5: data/solar_data.csv
Generate hourly solar generation and household load data from 06:00 to 18:00:

Columns: Hour,Generation_kW,Consumption_kW,Surplus_kW

Populate realistic daylight curves (peaking around 12:00-14:00 at ~7.8 kW generation vs ~2.3 kW home load, producing ~5.5 kW peak surplus).

File 6: data/stations.csv
Generate 5 local consumer hubs around Sathyabama / OMR Chennai (~12.8731° N, 80.2209° E):

Columns: ID,Name,Type,Latitude,Longitude,Demand_kW,Dynamic_Rate_INR,Status

Seeded Data:

Hub 1: "OMR EV FastCharge Hub" | EV Station | 12.8750 | 80.2240 | 15.0 | 5.20 | Available

Hub 2: "Sathyabama Campus e-Shuttle" | EV Fleet | 12.8715 | 80.2190 | 10.0 | 4.80 | Available

Hub 3: "SunRise Commercial Bakery" | Small Business | 12.8790 | 80.2260 | 6.5 | 5.50 | Available

Hub 4: "SpeedClean Laundromat" | Small Business | 12.8680 | 80.2150 | 4.0 | 5.00 | Available

Hub 5: "GreenWheels 2-Wheeler Swap" | EV Station | 12.8820 | 80.2280 | 8.0 | 4.50 | Available

File 7: data/bookings.csv
Initialize with header:Booking_ID,Timestamp,Customer_Name,Station_Name,Units_kWh,Rate_Per_kWh,Total_Amount_INR,Status
Pre-seed 2 mock records so the table is never blank on start.

4. APPLICATION LAYOUT & FEATURES IN app.py
Header & Navigation:

Title: "☀️ SunLoop — Where Wasted Watts Find Worth"

Subtitle: "Hyperlocal Solar Energy Sharing | Dexathon 2026 | Team: Nexus Navigators (DEX26299)"

Live simulated status pill: "🟢 Solar Inverter Connected | Net Export: ACTIVE"

4 responsive tabs:

⚡ Real-Time Solar Monitor

📍 Hyperlocal Energy Map

🤝 Smart Match & Booking

💰 Savings & Impact Calculator

Tab 1: Real-Time Solar Monitor:

4 elevated 3D cards displaying:

Current Solar Generation: 7.2 kW

Home Consumption: 2.1 kW

Available Surplus Watts: 5.1 kW (highlighted in solar orange)

Real-time Solar Discount Rate: ₹4.80/kWh (vs Grid ₹8.50/kWh)

Chart: Visualizing Generation vs. Consumption over time, highlighting the peak surplus window (11:00 AM - 03:00 PM).

Tab 2: Hyperlocal Energy Map:

Folium map with OpenStreetMap tiles centered on the host solar rooftop (Gold/Orange Marker).

Marker points for the 5 nearby stations/buyers from stations.csv.

Clicking on a marker shows a 3D-styled popup with station name, type, live power demand (kW), current offered price, and booking availability.

Tab 3: Smart Match & Booking (with 3D Modal Voucher):

"Smart Match Algorithm" box: Automatically detects the best consumer hub based on highest demand matching the host's current 5.1 kW surplus.

Interactive booking form:

Buyer Name input.

Select Target Hub (dropdown from stations.csv).

Energy Units Requested (slider: 1 kWh to 30 kWh).

Preferred Daylight Slot.

Dynamic real-time calculation box:

Standard Grid Cost: Units * ₹8.50

SunLoop Cost: Units * Selected_Dynamic_Rate

Direct User Savings: Standard Grid Cost - SunLoop Cost

"Confirm & Book Slot" Button:

Uses @st.dialog("⚡ Solar Booking Confirmed!") to trigger an elevated 3D pop-up modal showing a clean booking receipt, total price, dynamic QR-verification placeholder, and an eco-impact tag.

Triggers st.balloons() celebration.

Appends the record into data/bookings.csv and reruns to refresh the table.

Display a stylish table of all booked transactions.

Tab 4: Savings & Impact Calculator:

Interactive Sliders:

Average Daily Surplus Traded (kWh/day) [Default: 25 kWh]

Standard Grid Tariff (₹/kWh) [Default: ₹8.50]

SunLoop Shared Tariff (₹/kWh) [Default: ₹5.00]

3D Metrics Grid:

Rooftop Owner Monthly Revenue: (Daily_kWh * SunLoop_Tariff * 30) ₹

EV Buyer Monthly Savings: (Daily_kWh * (Grid_Tariff - SunLoop_Tariff) * 30) ₹

Annual CO₂ Emissions Prevented: (Daily_kWh * 365 * 0.82) kg CO₂

Playful "Solar Tier Badge" card unlocked based on annual carbon offset:

< 2,000 kg: "🌱 Sprout Saver"

2,000 - 6,000 kg: "⚡ Watt Wizard"

6,000+ kg: "🌍 Solar Champion (Elite Clean Energy Contributor)"

5. EXECUTION INSTRUCTIONS
Create all directories and files listed above.

Ensure all CSV reads/writes create files if they do not exist.

Start the Docker container using docker compose up --build -d.

Make sure the application is live and accessible at http://localhost:8501.