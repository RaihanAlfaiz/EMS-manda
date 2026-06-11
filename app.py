import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="EMS Enterprise Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for login
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user_role" not in st.session_state:
    st.session_state["user_role"] = "Admin"
if "user_name" not in st.session_state:
    st.session_state["user_name"] = "Jane Doe"

# Initialize system parameters configuration
if "tarif_pln" not in st.session_state:
    st.session_state["tarif_pln"] = 1726
if "tarif_ev_50" not in st.session_state:
    st.session_state["tarif_ev_50"] = 2500
if "tarif_ev_120" not in st.session_state:
    st.session_state["tarif_ev_120"] = 3500
if "tipe_rentang" not in st.session_state:
    st.session_state["tipe_rentang"] = "Harian (Per Hari)"
if "batas_angka" not in st.session_state:
    st.session_state["batas_angka"] = 1700
if "categories" not in st.session_state:
    st.session_state["categories"] = ["AC / HVAC", "Lampu (Lighting)", "EV Charging", "Stop Kontak"]

if not st.session_state["logged_in"]:
    st.markdown(
        """
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>
        <style>
            [data-testid="stAppViewContainer"] {
                background: radial-gradient(circle at top right, #102a45, #000d1a) !important;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            /* Dark Glassmorphic Login Form Wrapper */
            div[data-testid="stForm"] {
                max-width: 420px;
                margin: 60px auto 10px auto;
                padding: 40px !important;
                background: rgba(16, 32, 56, 0.65) !important;
                backdrop-filter: blur(20px) saturate(180%);
                -webkit-backdrop-filter: blur(20px) saturate(180%);
                border-radius: 16px !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.5) !important;
            }
            
            /* Form input labels style */
            div[data-testid="stTextInput"] label, div[data-testid="stSelectbox"] label {
                color: rgba(255, 255, 255, 0.85) !important;
                font-weight: 600 !important;
                font-size: 13px !important;
                margin-bottom: 6px !important;
            }
            
            /* Text inputs style */
            div[data-testid="stTextInput"] input {
                background-color: rgba(255, 255, 255, 0.04) !important;
                border: 1px solid rgba(255, 255, 255, 0.12) !important;
                color: #ffffff !important;
                border-radius: 8px !important;
                padding: 10px 14px !important;
                transition: all 0.2s ease-in-out !important;
            }
            
            div[data-testid="stTextInput"] input:focus {
                border-color: #0058be !important;
                box-shadow: 0 0 0 2px rgba(0, 88, 190, 0.35) !important;
                background-color: rgba(255, 255, 255, 0.08) !important;
            }
            
            /* Selectbox container styling */
            div[data-testid="stSelectbox"] > div {
                background-color: transparent !important;
            }
            
            div[data-testid="stSelectbox"] div[data-baseweb="select"] {
                background-color: rgba(255, 255, 255, 0.04) !important;
                border: 1px solid rgba(255, 255, 255, 0.12) !important;
                border-radius: 8px !important;
                color: #ffffff !important;
            }
            
            div[data-testid="stSelectbox"] div[data-baseweb="select"] div {
                color: #ffffff !important;
            }

            /* Dropdown list styling */
            ul[role="listbox"] {
                background-color: #0c1b30 !important;
                border: 1px solid rgba(255, 255, 255, 0.15) !important;
            }
            ul[role="listbox"] li {
                color: #ffffff !important;
                transition: background-color 0.2s !important;
            }
            ul[role="listbox"] li:hover {
                background-color: rgba(255, 255, 255, 0.1) !important;
            }
            
            /* Submit Button styling */
            button[data-testid="stFormSubmitButton"] {
                background: linear-gradient(135deg, #0058be 0%, #2170e4 100%) !important;
                color: #ffffff !important;
                border: none !important;
                border-radius: 8px !important;
                font-weight: 700 !important;
                padding: 12px 24px !important;
                width: 100% !important;
                box-shadow: 0 4px 15px rgba(0, 88, 190, 0.3) !important;
                transition: all 0.2s ease-in-out !important;
                margin-top: 10px !important;
            }
            
            button[data-testid="stFormSubmitButton"]:hover {
                transform: translateY(-1px) !important;
                box-shadow: 0 6px 20px rgba(0, 88, 190, 0.55) !important;
                background: linear-gradient(135deg, #2170e4 0%, #0058be 100%) !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        with st.form("login_form"):
            st.markdown(
                """
                <div class="login-header" style="text-align: center; margin-bottom: 28px;">
                    <span class="material-symbols-outlined" style="font-size: 54px; color: #3b82f6; margin-bottom: 8px;">bolt</span>
                    <h1 style="color: #ffffff; font-size: 26px; font-weight: 800; margin: 0; background: linear-gradient(135deg, #ffffff 0%, #adc6ff 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">EMS Enterprise</h1>
                    <p style="color: rgba(255, 255, 255, 0.6); font-size: 11px; margin: 4px 0 0 0; text-transform: uppercase; letter-spacing: 0.12em;">Sistem Pemantauan Energi</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            username = st.text_input("Username", placeholder="Masukkan username")
            password = st.text_input("Password", type="password", placeholder="Masukkan password")
            role = st.selectbox("Role Akses", ["Admin", "Super Admin"])
            
            submit = st.form_submit_button("Masuk ke Dashboard")
            if submit:
                if role == "Admin" and username == "admin" and password == "admin":
                    st.session_state["logged_in"] = True
                    st.session_state["user_role"] = "Admin"
                    st.session_state["user_name"] = "Jane Doe"
                    st.success("Login berhasil!")
                    st.rerun()
                elif role == "Super Admin" and username == "superadmin" and password == "superadmin":
                    st.session_state["logged_in"] = True
                    st.session_state["user_role"] = "Super Admin"
                    st.session_state["user_name"] = "John Doe"
                    st.success("Login berhasil!")
                    st.rerun()
                else:
                    st.error("Username atau Password salah!")
                    
        st.markdown(
            """
            <div style="background-color: rgba(255, 255, 255, 0.04); border-radius: 8px; padding: 12px; margin-top: 20px; font-size: 11px; color: rgba(255, 255, 255, 0.7); text-align: center; border: 1px solid rgba(255, 255, 255, 0.08);">
                <p style="margin: 0; font-weight: 600; color: #ffffff;">Petunjuk Login:</p>
                <p style="margin: 4px 0 0 0;">Admin: <code>admin</code> / <code>admin</code><br>
                Super Admin: <code>superadmin</code> / <code>superadmin</code></p>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.stop()

# Custom Global Styles (Material Icons, Inter Font, and specific overrides)
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>
    <style>
        /* Global Reset & Typography */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
            font-family: 'Inter', sans-serif !important;
            background-color: #f8f9ff !important;
            color: #0b1c30 !important;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #000000 !important;
            border-right: 1px solid #c6c6cd !important;
            min-width: 260px !important;
            max-width: 260px !important;
        }
        
        [data-testid="stSidebar"] * {
            color: #ffffff !important;
        }

        /* Navigation Radio custom style inside Sidebar */
        [data-testid="stSidebar"] div[role="radiogroup"] {
            gap: 4px;
        }

        [data-testid="stSidebar"] div[role="radiogroup"] label {
            background-color: transparent !important;
            border: none !important;
            border-radius: 4px !important;
            padding: 8px 12px !important;
            color: rgba(255, 255, 255, 0.7) !important;
            font-weight: 500 !important;
            transition: all 0.2s ease-in-out !important;
            cursor: pointer !important;
            margin-bottom: 2px !important;
        }

        [data-testid="stSidebar"] div[role="radiogroup"] label:hover {
            background-color: rgba(255, 255, 255, 0.1) !important;
            color: #ffffff !important;
        }

        [data-testid="stSidebar"] div[role="radiogroup"] label[data-selected="true"] {
            background-color: #0058be !important;
            color: #ffffff !important;
            font-weight: 700 !important;
        }

        /* Top Header Styling */
        header[data-testid="stHeader"] {
            background-color: rgba(248, 249, 255, 0.8) !important;
            backdrop-filter: blur(8px);
            border-bottom: 1px solid #c6c6cd !important;
            z-index: 99;
        }

        /* Premium Cards */
        .data-card {
            border: 1px solid #e2e8f0;
            background-color: #ffffff;
            padding: 24px;
            border-radius: 4px;
            box-shadow: 0px 4px 6px -1px rgba(15, 23, 42, 0.05);
            transition: all 0.2s ease-in-out;
            margin-bottom: 20px;
        }

        .data-card:hover {
            box-shadow: 0px 10px 15px -3px rgba(15, 23, 42, 0.08);
            transform: translateY(-2px);
        }

        /* Native bordered container override to look like premium card */
        section[data-testid="stMain"] div[data-testid="stVerticalBlockBorderWrapper"] {
            border: 1px solid #e2e8f0 !important;
            background-color: #ffffff !important;
            border-radius: 8px !important;
            box-shadow: 0px 4px 6px -1px rgba(15, 23, 42, 0.05) !important;
            padding: 20px !important;
            transition: all 0.2s ease-in-out !important;
        }

        section[data-testid="stMain"] div[data-testid="stVerticalBlockBorderWrapper"]:hover {
            box-shadow: 0px 10px 15px -3px rgba(15, 23, 42, 0.08) !important;
            transform: translateY(-2px) !important;
        }

        /* Prevent sidebar vertical blocks from acquiring white card styling */
        [data-testid="stSidebar"] div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0px !important;
        }

        /* Sidebar Button styling */
        [data-testid="stSidebar"] button {
            background-color: rgba(255, 255, 255, 0.08) !important;
            color: #ffb4ab !important;
            border: 1px solid rgba(255, 180, 171, 0.2) !important;
            border-radius: 6px !important;
            font-weight: 600 !important;
            font-size: 13px !important;
            transition: all 0.2s ease-in-out !important;
            height: 38px !important;
        }
        [data-testid="stSidebar"] button:hover {
            background-color: #ba1a1a !important;
            color: #ffffff !important;
            border-color: #ba1a1a !important;
            box-shadow: 0 0 10px rgba(186, 26, 26, 0.4) !important;
        }

        .material-symbols-outlined {
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
            vertical-align: middle;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar Branding & Navigation
with st.sidebar:
    st.markdown(
        """
        <div style="padding: 10px 10px 24px 10px; border-bottom: 1px solid rgba(255,255,255,0.1); margin-bottom: 20px;">
            <h1 style="color: white; font-size: 20px; font-weight: 700; margin: 0; line-height: 1.2;">EMS Enterprise</h1>
            <p style="color: rgba(255,255,255,0.6); font-size: 9px; text-transform: uppercase; letter-spacing: 0.15em; margin: 4px 0 0 0;">RELIABLE MONITORING</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Selection radio formatted nicely
    page = st.radio(
        "Navigation",
        options=[
            "Dashboard",
            "Energy Profile",
            "Real-time EV Monitoring",
            "Reports & Audit",
            "Admin Settings"
        ],
        label_visibility="collapsed"
    )

    st.markdown("<hr style='margin: 15px 0; border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 11px; font-weight: 700; color: rgba(255,255,255,0.5); text-transform: uppercase; margin: 0 0 10px 0;'>⚡ Batas Baseline</p>", unsafe_allow_html=True)
    baseline_limit = st.slider(
        "Batas Baseline (kWh)",
        min_value=50,
        max_value=200,
        value=120,
        step=5,
        label_visibility="collapsed"
    )
    st.markdown(f"<p style='font-size: 12px; color: #adc6ff; margin-top: -5px;'>Batas: <b>{baseline_limit} kWh</b></p>", unsafe_allow_html=True)

    st.markdown(
        """
        <div style="margin-top: 40px; padding: 10px; border-radius: 8px; background-color: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);">
            <p style="font-size: 9px; color: rgba(255,255,255,0.5); text-transform: uppercase; font-weight: 700; margin: 0 0 8px 0; letter-spacing: 0.1em;">System Status</p>
            <div style="display: flex; align-items: center; gap: 8px;">
                <div style="width: 8px; height: 8px; border-radius: 9999px; background-color: #4edea3; box-shadow: 0 0 8px #4edea3;"></div>
                <span style="font-size: 11px; color: rgba(255,255,255,0.8);">All Systems Nominal</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Footer/Profile in Sidebar
    u_name = st.session_state.get("user_name", "Jane Doe")
    u_role = st.session_state.get("user_role", "Admin")
    u_initials = "".join([part[0] for part in u_name.split()[:2]]).upper()

    st.markdown(
        f"""
        <div style="margin-top: auto; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.1); display: flex; align-items: center; gap: 12px;">
            <div style="width: 36px; height: 36px; border-radius: 9999px; background-color: #2170e4; display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; font-size: 14px;">
                {u_initials}
            </div>
            <div>
                <p style="font-size: 13px; font-weight: 600; color: #ffffff; margin: 0; line-height: 1.2;">{u_name}</p>
                <p style="font-size: 10px; color: rgba(255,255,255,0.6); margin: 0;">{u_role}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Custom styled logout button in sidebar
    if st.button("Keluar (Logout)", use_container_width=True):
        st.session_state["logged_in"] = False
        st.session_state["user_role"] = "Admin"
        st.session_state["user_name"] = "Jane Doe"
        st.rerun()

# Header Section Builder
def build_header(title, subtitle_badge=None, temp_str="31°C", user_role=None, user_name=None):
    if user_role is None:
        user_role = st.session_state.get("user_role", "Admin")
    if user_name is None:
        user_name = st.session_state.get("user_name", "Jane Doe")
    badge_html = f'<div style="height: 20px; width: 1px; bg-color: #c6c6cd; background-color: #c6c6cd; margin: 0 12px;"></div><span style="font-size: 11px; font-weight: 600; color: #45464d; background-color: #e5eeff; padding: 4px 8px; border-radius: 4px; text-transform: uppercase;">{subtitle_badge}</span>' if subtitle_badge else ''
    
    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; border-bottom: 1px solid #e2e8f0; padding-bottom: 16px;">
          <div style="display: flex; align-items: center;">
            <h2 style="font-size: 24px; font-weight: 700; color: #0b1c30; margin: 0; line-height: 1.2;">{title}</h2>
            {badge_html}
          </div>
          <div style="display: flex; align-items: center; gap: 20px;">
            <!-- Weather -->
            <div style="display: flex; align-items: center; gap: 8px; padding: 6px 12px; background-color: #eff4ff; border-radius: 9999px; border: 1px solid #c6c6cd;">
              <span class="material-symbols-outlined" style="color: #0058be;">partly_cloudy_day</span>
              <div style="display: flex; flex-direction: column;">
                <span style="font-size: 9px; font-weight: 700; color: #76777d; text-transform: uppercase; line-height: 1;">Cikarang, ID</span>
                <span style="font-size: 13px; font-weight: 700; color: #0b1c30;">{temp_str}</span>
              </div>
            </div>
            <!-- Notifications -->
            <div style="position: relative; cursor: pointer; padding: 8px; border-radius: 9999px; transition: background-color 0.2s;">
              <span class="material-symbols-outlined" style="color: #45464d;">notifications</span>
              <span style="position: absolute; top: 8px; right: 8px; width: 8px; height: 8px; background-color: #ba1a1a; border-radius: 9999px; border: 1.5px solid white;"></span>
            </div>
            <!-- Profile -->
            <div style="display: flex; align-items: center; gap: 12px; padding-left: 16px; border-left: 1px solid #c6c6cd;">
              <div style="text-align: right;">
                <p style="font-size: 13px; font-weight: 700; color: #0b1c30; margin: 0;">{user_name}</p>
                <p style="font-size: 9px; font-weight: 700; color: #76777d; text-transform: uppercase; margin: 0;">{user_role}</p>
              </div>
              <div style="width: 36px; height: 36px; border-radius: 9999px; background-color: #2170e4; display: flex; align-items: center; justify-content: center; color: white;">
                <span class="material-symbols-outlined">person</span>
              </div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------- PAGE 1: DASHBOARD EMS ----------------
if page == "Dashboard":
    build_header("Dashboard EMS", temp_str="31°C")
    
    # Dashboard calculations based on baseline_limit
    hours = ['08:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00']
    consumption = [48, 66, 102, 145, 72, 54, 36]
    
    # Check if baseline is exceeded
    excess_sum = sum(max(0, val - baseline_limit) for val in consumption)
    efficiency = max(0, 100 - int(excess_sum / sum(consumption) * 100))
    is_exceeded = any(val >= baseline_limit for val in consumption)
    
    if is_exceeded:
        status_badge = '<span style="font-size: 12px; font-weight: 700; color: #ba1a1a; background-color: rgba(186, 26, 26, 0.1); border: 1px solid rgba(186, 26, 26, 0.2); padding: 4px 8px; border-radius: 4px; text-transform: uppercase;">Warning</span>'
        status_desc = f"{efficiency}% Efficiency"
        card_border = "border-left: 4px solid #ba1a1a;"
    else:
        status_badge = '<span style="font-size: 12px; font-weight: 700; color: #0058be; background-color: rgba(0, 88, 190, 0.1); border: 1px solid rgba(0, 88, 190, 0.2); padding: 4px 8px; border-radius: 4px; text-transform: uppercase;">Normal</span>'
        status_desc = "100% Efficiency"
        card_border = "border-left: 4px solid #0058be;"
    
    # Metric cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            """
            <div class="data-card">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 16px;">
                    <p style="font-size: 11px; font-weight: 600; color: #76777d; text-transform: uppercase; letter-spacing: 0.05em; margin: 0;">Total kWh Hari Ini</p>
                    <span class="material-symbols-outlined" style="color: #0058be;">bolt</span>
                </div>
                <h3 style="font-size: 28px; font-weight: 700; color: #0b1c30; margin: 0; line-height: 1;">1,248.50</h3>
                <div style="margin-top: 16px; display: inline-flex; align-items: center; gap: 4px; color: #005236; background-color: rgba(111, 251, 190, 0.2); padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 700;">
                    <span class="material-symbols-outlined" style="font-size: 14px;">trending_up</span>
                    12% vs Kemarin
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="data-card">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 16px;">
                    <p style="font-size: 11px; font-weight: 600; color: #76777d; text-transform: uppercase; letter-spacing: 0.05em; margin: 0;">Estimasi Biaya (Rp)</p>
                    <span class="material-symbols-outlined" style="color: #0058be;">payments</span>
                </div>
                <h3 style="font-size: 28px; font-weight: 700; color: #0b1c30; margin: 0; line-height: 1;">Rp 1.872.750</h3>
                <p style="font-size: 11px; color: #76777d; font-weight: 700; text-transform: uppercase; margin: 16px 0 0 0;">Billing Cycle: Day 12 of 30</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="data-card" style="{card_border}">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 16px;">
                    <p style="font-size: 11px; font-weight: 600; color: #76777d; text-transform: uppercase; letter-spacing: 0.05em; margin: 0;">Status Baseline</p>
                    <span class="material-symbols-outlined" style="color: #0058be;">equalizer</span>
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    {status_badge}
                    <p style="font-size: 14px; color: #0b1c30; margin: 0; font-weight: 500;">{status_desc}</p>
                </div>
                <p style="font-size: 11px; color: #76777d; font-style: italic; margin: 16px 0 0 0;">Updated 2 mins ago</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Charts Grid
    chart_col1, chart_col2 = st.columns([2, 1])
    
    with chart_col1:
        with st.container(border=True):
            # Bar Chart - Energy Consumption
            colors = ['#ba1a1a' if val >= baseline_limit else '#adc6ff' for val in consumption]

            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(
                x=hours,
                y=consumption,
                marker_color=colors,
                hovertemplate='%{x}: %{y} kWh<extra></extra>',
                showlegend=False
            ))

            # Add target baseline line
            fig_bar.add_shape(
                type="line",
                x0=-0.5, y0=baseline_limit, x1=6.5, y1=baseline_limit,
                line=dict(color="#ba1a1a", width=2, dash="dash")
            )

            fig_bar.add_annotation(
                x=5.0, y=baseline_limit + 6 if baseline_limit < 190 else baseline_limit - 10,
                text=f"TARGET BASELINE ({baseline_limit} kWh/h)",
                showarrow=False,
                font=dict(color="#ba1a1a", size=9, family="Inter", weight="bold"),
                bgcolor="#ffffff",
                opacity=0.9
            )

            fig_bar.add_annotation(
                x='14:00', y=145,
                text="PEAK: 145kWh",
                showarrow=True,
                arrowhead=1,
                ax=0, ay=-30,
                font=dict(color="#ffffff", size=9, family="Inter", weight="bold"),
                bgcolor="#ba1a1a",
                bordercolor="#ba1a1a",
                borderwidth=1,
                borderpad=4
            )

            fig_bar.update_layout(
                title=dict(
                    text="Konsumsi Energi<br><span style='font-size: 11px; color: #76777d; font-weight: normal;'>Real-time data compared to target baseline</span>",
                    font=dict(size=16, family="Inter", color="#0b1c30", weight="bold")
                ),
                xaxis=dict(showgrid=False, linecolor='#c6c6cd'),
                yaxis=dict(showgrid=True, gridcolor='#eff4ff', linecolor='#c6c6cd'),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=20, r=20, t=60, b=20),
                height=340
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
    with chart_col2:
        with st.container(border=True):
            # Donut Chart - Tool distribution
            labels = ['Air Conditioning (AC)', 'Lighting (Lampu)', 'EV Charging']
            values = [45, 30, 25]
            colors_pie = ['#0058be', '#4edea3', '#d8e2ff']

            fig_pie = go.Figure(data=[go.Pie(
                labels=labels,
                values=values,
                hole=.6,
                marker=dict(colors=colors_pie),
                hovertemplate='%{label}: %{percent}<extra></extra>',
                textinfo='percent',
                textposition='inside',
                showlegend=True
            )])

            fig_pie.add_annotation(
                x=0.5, y=0.5,
                text="TOTAL<br><b>100%</b>",
                showarrow=False,
                font=dict(size=14, family="Inter", color="#0b1c30"),
                align="center"
            )

            fig_pie.update_layout(
                title=dict(
                    text="Distribusi Alat<br><span style='font-size: 11px; color: #76777d; font-weight: normal;'>Load consumption per category</span>",
                    font=dict(size=16, family="Inter", color="#0b1c30", weight="bold")
                ),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.3,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=10)
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=60, b=50),
                height=340
            )
            st.plotly_chart(fig_pie, use_container_width=True)

    # Baseline Exceedance warning and chart
    if is_exceeded:
        st.markdown(
            f"""
            <div style="background-color: #ffdad9; border: 1px solid #ba1a1a; padding: 16px; border-radius: 4px; margin-bottom: 20px; display: flex; align-items: center; gap: 12px; color: #410002;">
                <span class="material-symbols-outlined" style="color: #ba1a1a; font-size: 24px;">warning</span>
                <div>
                    <h4 style="margin: 0; font-weight: 700; font-size: 14px;">Peringatan Kelebihan Beban Baseline!</h4>
                    <p style="margin: 2px 0 0 0; font-size: 12px;">Konsumsi energi puncak hari ini mencapai <b>145 kWh</b> pada pukul <b>14:00</b>, melebihi batas baseline Anda sebesar <b>{145 - baseline_limit} kWh</b>.</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.container(border=True):
            # Plotly chart for excess over baseline
            excess = [max(0, val - baseline_limit) for val in consumption]
            
            fig_excess = go.Figure()
            fig_excess.add_trace(go.Scatter(
                x=hours,
                y=excess,
                mode='lines+markers',
                fill='tozeroy',
                line=dict(color='#ba1a1a', width=3),
                fillcolor='rgba(186, 26, 26, 0.2)',
                hovertemplate='%{x}: %{y} kWh (Overshoot)<extra></extra>',
                name='Kelebihan Beban'
            ))

            fig_excess.update_layout(
                title=dict(
                    text="Grafik Deviasi Over-Baseline (Sisa Konsumsi Berlebih)<br><span style='font-size: 11px; color: #76777d; font-weight: normal;'>Detail kelebihan penggunaan daya di atas batas target baseline</span>",
                    font=dict(size=16, family="Inter", color="#0b1c30", weight="bold")
                ),
                xaxis=dict(showgrid=False, linecolor='#c6c6cd'),
                yaxis=dict(showgrid=True, gridcolor='#eff4ff', linecolor='#c6c6cd'),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=20, r=20, t=60, b=20),
                height=280
            )
            st.plotly_chart(fig_excess, use_container_width=True)

    # Detailed Transactions Table Section
    st.markdown("### Detail Transaksi EV Charging")
    st.markdown("<p style='font-size: 13px; color: #76777d; margin-top: -10px; margin-bottom: 15px;'>Real-time usage logs for electric vehicle stations</p>", unsafe_allow_html=True)
    
    # Filter/Search Row
    search_col, space_col = st.columns([1, 2])
    with search_col:
        search_query = st.text_input("Search ID User...", placeholder="Cari ID User / Tipe...", label_visibility="collapsed")
        
    transactions_data = [
        {"ID User": "#EV-09234", "Tipe Charger": "DC Fast Charger", "Waktu Mulai": "Today, 14:23", "Daya (kWh)": "42.5 kWh", "Total Rp": "Rp 63.750", "badge_class": "dc-fast"},
        {"ID User": "#EV-09231", "Tipe Charger": "AC Type 2", "Waktu Mulai": "Today, 12:45", "Daya (kWh)": "18.2 kWh", "Total Rp": "Rp 27.300", "badge_class": "ac-type"},
        {"ID User": "#EV-09228", "Tipe Charger": "DC Fast Charger", "Waktu Mulai": "Today, 10:15", "Daya (kWh)": "35.0 kWh", "Total Rp": "Rp 52.500", "badge_class": "dc-fast"},
        {"ID User": "#EV-09225", "Tipe Charger": "DC Fast Charger", "Waktu Mulai": "Active Session", "Daya (kWh)": "-- kWh", "Total Rp": "--", "badge_class": "dc-fast-active"},
    ]

    filtered_tx = [
        tx for tx in transactions_data 
        if search_query.lower() in tx["ID User"].lower() or search_query.lower() in tx["Tipe Charger"].lower()
    ]

    table_rows = ""
    for tx in filtered_tx:
        badge = ""
        if tx["badge_class"] == "dc-fast":
            badge = '<span style="background-color: rgba(216, 226, 255, 0.6); color: #0058be; font-weight: 700; font-size: 10px; padding: 4px 8px; border-radius: 4px; text-transform: uppercase;">DC Fast Charger</span>'
        elif tx["badge_class"] == "ac-type":
            badge = '<span style="background-color: rgba(198, 198, 205, 0.3); color: #76777d; font-weight: 700; font-size: 10px; padding: 4px 8px; border-radius: 4px; text-transform: uppercase;">AC Type 2</span>'
        elif tx["badge_class"] == "dc-fast-active":
            badge = '<span style="background-color: rgba(216, 226, 255, 0.6); color: #0058be; font-weight: 700; font-size: 10px; padding: 4px 8px; border-radius: 4px; text-transform: uppercase;">DC Fast Charger</span>'
        
        row_style = ""
        waktu_style = "color: #45464d;"
        if tx["Waktu Mulai"] == "Active Session":
            row_style = 'style="border-left: 4px solid #2170e4;"'
            waktu_style = "color: #2170e4; font-weight: 700; font-style: italic;"
            
        table_rows += f"""
        <tr {row_style}>
            <td style="padding: 16px 24px; font-weight: 700; color: #0b1c30; font-size: 14px;">{tx["ID User"]}</td>
            <td style="padding: 16px 24px;">{badge}</td>
            <td style="padding: 16px 24px; font-size: 14px; {waktu_style}">{tx["Waktu Mulai"]}</td>
            <td style="padding: 16px 24px; font-weight: 700; font-size: 14px; color: #0b1c30;">{tx["Daya (kWh)"]}</td>
            <td style="padding: 16px 24px; text-align: right; font-weight: 700; font-size: 14px; color: #0b1c30;">{tx["Total Rp"]}</td>
        </tr>
        """

    if not filtered_tx:
        table_rows = """
        <tr>
            <td colspan="5" style="padding: 32px; text-align: center; color: #76777d; font-style: italic;">Tidak ada transaksi yang ditemukan</td>
        </tr>
        """

    table_html = f"""
    <div class="data-card" style="padding: 0px; overflow: hidden; border-radius: 4px; border: 1px solid #e2e8f0; background-color: #ffffff;">
        <div style="overflow-x: auto;">
            <table style="width: 100%; border-collapse: collapse; text-align: left;">
                <thead>
                    <tr style="background-color: #e5eeff; border-bottom: 1px solid #c6c6cd;">
                        <th style="padding: 16px 24px; font-size: 12px; font-weight: 600; color: #45464d; text-transform: uppercase; letter-spacing: 0.05em;">ID User</th>
                        <th style="padding: 16px 24px; font-size: 12px; font-weight: 600; color: #45464d; text-transform: uppercase; letter-spacing: 0.05em;">Tipe Charger</th>
                        <th style="padding: 16px 24px; font-size: 12px; font-weight: 600; color: #45464d; text-transform: uppercase; letter-spacing: 0.05em;">Waktu Mulai</th>
                        <th style="padding: 16px 24px; font-size: 12px; font-weight: 600; color: #45464d; text-transform: uppercase; letter-spacing: 0.05em;">Daya (kWh)</th>
                        <th style="padding: 16px 24px; text-align: right; font-size: 12px; font-weight: 600; color: #45464d; text-transform: uppercase; letter-spacing: 0.05em;">Total Rp</th>
                    </tr>
                </thead>
                <tbody style="background-color: #ffffff;">
                    {table_rows}
                </tbody>
            </table>
        </div>
        <div style="padding: 16px 24px; background-color: #ffffff; border-top: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 12px; color: #76777d; font-weight: 700;">Showing {len(filtered_tx)} of {len(transactions_data)} records</span>
            <div style="display: flex; gap: 8px;">
                <button style="border: 1px solid #c6c6cd; background-color: #ffffff; padding: 6px 12px; border-radius: 4px; cursor: pointer; color: #45464d; font-weight: bold;"><span class="material-symbols-outlined" style="font-size: 16px;">chevron_left</span></button>
                <button style="border: 1px solid #c6c6cd; background-color: #ffffff; padding: 6px 12px; border-radius: 4px; cursor: pointer; color: #45464d; font-weight: bold;"><span class="material-symbols-outlined" style="font-size: 16px;">chevron_right</span></button>
            </div>
        </div>
    </div>
    """
    st.markdown(table_html.replace('\n', ' '), unsafe_allow_html=True)


# ---------------- PAGE 2: ENERGY PROFILE ANALYSIS ----------------
elif page == "Energy Profile":
    build_header("Analisa Profil Energi", temp_str="24°C")
    
    # Filter Bar Section
    with st.container(border=True):
        st.markdown("<h4 style='font-size: 12px; font-weight: 700; color: #76777d; text-transform: uppercase; margin: 0 0 16px 0;'>Filter Analisa:</h4>", unsafe_allow_html=True)
        
        fcol1, fcol2, fcol3, fcol4 = st.columns([1, 1, 1, 0.8])
        with fcol1:
            periode_sel = st.selectbox("Pilih Periode..", ["7 Hari Terakhir", "30 Hari Terakhir", "Bulan Ini", "Kustom..."])
        with fcol2:
            kategori_sel = st.selectbox("Kategori:", ["Semua Beban", "Penerangan", "HVAC", "Produksi"])
        with fcol3:
            bandingkan_sel = st.selectbox("Bandingkan:", ["Minggu Lalu", "Tahun Lalu", "Target Baseline"])
        with fcol4:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            apply_btn = st.button("Terapkan", use_container_width=True, type="primary")

    # Dynamic Data Generator
    def generate_analisa_data(periode, kategori, bandingkan):
        if periode == "7 Hari Terakhir":
            days = 7
        elif periode == "30 Hari Terakhir":
            days = 30
        elif periode == "Bulan Ini":
            days = 15  # Let's say mid-month
        else:
            days = 7
            
        # Base multiplier based on category
        cat_mult = 1.0
        if kategori == "Penerangan":
            cat_mult = 0.3
        elif kategori == "HVAC":
            cat_mult = 0.45
        elif kategori == "Produksi":
            cat_mult = 0.25
            
        np.random.seed(10)
        base_date = datetime(2023, 10, 27)
        dates = [(base_date - timedelta(days=i)).strftime("%d %b") for i in range(days)]
        dates.reverse()
        
        baseline_val = 1750 * cat_mult
        
        current_y = [int(1800 * cat_mult + np.random.normal(0, 80 * cat_mult)) for _ in range(days)]
        prev_y = [int(1650 * cat_mult + np.random.normal(0, 60 * cat_mult)) for _ in range(days)]
        
        sum_curr = sum(current_y)
        sum_prev = sum(prev_y)
        diff_pct = round(((sum_curr - sum_prev) / sum_prev) * 100, 1)
        
        return dates, current_y, prev_y, baseline_val, sum_curr, sum_prev, diff_pct

    dates, current_y, prev_y, baseline_val, sum_curr, sum_prev, diff_pct = generate_analisa_data(periode_sel, kategori_sel, bandingkan_sel)

    # KPI Cards Section
    kcol1, kcol2, kcol3 = st.columns(3)
    
    with kcol1:
        st.markdown(
            f"""
            <div class="data-card">
                <p style="font-size: 11px; font-weight: 600; color: #76777d; text-transform: uppercase; letter-spacing: 0.05em; margin: 0 0 8px 0;">Total kWh Periode Ini</p>
                <div style="display: flex; align-items: baseline; gap: 8px;">
                    <h3 style="font-size: 28px; font-weight: 700; color: #0b1c30; margin: 0;">{sum_curr:,}</h3>
                    <span style="font-size: 14px; color: #76777d; font-weight: 600;">kWh</span>
                </div>
                <div style="margin-top: 16px; color: #3f465c; font-size: 11px; font-weight: 700; text-transform: uppercase; border-bottom: 1px dotted #76777d; width: fit-content;">Value Saat Ini</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with kcol2:
        st.markdown(
            f"""
            <div class="data-card">
                <p style="font-size: 11px; font-weight: 600; color: #76777d; text-transform: uppercase; letter-spacing: 0.05em; margin: 0 0 8px 0;">Total kWh Periode Lalu</p>
                <div style="display: flex; align-items: baseline; gap: 8px;">
                    <h3 style="font-size: 28px; font-weight: 700; color: #76777d; margin: 0;">{sum_prev:,}</h3>
                    <span style="font-size: 14px; color: #76777d; font-weight: 600;">kWh</span>
                </div>
                <div style="margin-top: 16px; color: #76777d; font-size: 11px; font-weight: 700; text-transform: uppercase; border-bottom: 1px dotted #76777d; width: fit-content;">Value Lalu</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with kcol3:
        status_color = "#ba1a1a" if diff_pct >= 0 else "#009668"
        plus_sign = "+" if diff_pct >= 0 else ""
        st.markdown(
            f"""
            <div class="data-card">
                <p style="font-size: 11px; font-weight: 600; color: #76777d; text-transform: uppercase; letter-spacing: 0.05em; margin: 0 0 8px 0;">Status Efisiensi (+ / -)</p>
                <div style="display: flex; align-items: baseline; gap: 8px; color: {status_color};">
                    <h3 style="font-size: 28px; font-weight: 700; margin: 0;">{plus_sign}{diff_pct}</h3>
                    <span style="font-size: 14px; font-weight: 600;">%</span>
                </div>
                <div style="margin-top: 16px; color: {status_color}; font-size: 11px; font-weight: 700; text-transform: uppercase; border-bottom: 1px dotted {status_color}; width: fit-content;">Naik/Turun %</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Line Chart
    with st.container(border=True):
        fig_line = go.Figure()
        
        # Current period (Solid black)
        fig_line.add_trace(go.Scatter(
            x=dates, y=current_y,
            mode='lines+markers',
            name='Periode Saat Ini',
            line=dict(color='#000000', width=3),
            hovertemplate='%{x}: %{y} kWh<extra></extra>'
        ))
        
        # Previous period (Dotted grey)
        fig_line.add_trace(go.Scatter(
            x=dates, y=prev_y,
            mode='lines+markers',
            name='Periode Lalu',
            line=dict(color='#c6c6cd', width=2, dash='dot'),
            hovertemplate='%{x}: %{y} kWh<extra></extra>'
        ))
        
        # Baseline
        fig_line.add_trace(go.Scatter(
            x=dates, y=[baseline_val]*len(dates),
            mode='lines',
            name='Batas Baseline',
            line=dict(color='#76777d', width=2, dash='dash'),
            hoverinfo='skip'
        ))
        
        fig_line.update_layout(
            title=dict(
                text="[Grafik Garis: Perbandingan Periode Ini vs Periode Lalu]",
                font=dict(size=16, family="Inter", color="#0b1c30", weight="bold")
            ),
            xaxis=dict(showgrid=False, linecolor='#c6c6cd'),
            yaxis=dict(showgrid=True, gridcolor='#eff4ff', linecolor='#c6c6cd'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.25,
                xanchor="center",
                x=0.5
            ),
            margin=dict(l=20, r=20, t=60, b=20),
            height=320
        )
        st.plotly_chart(fig_line, use_container_width=True)

    # Detailed Table Breakdown
    st.markdown("### [Tabel Rincian Breakdown Waktu]")
    
    table_rows = ""
    for d, curr, prev in zip(reversed(dates), reversed(current_y), reversed(prev_y)):
        diff = curr - prev
        diff_str = f"+{diff:,} kWh" if diff >= 0 else f"{diff:,} kWh"
        diff_color = "#ba1a1a" if diff >= 0 else "#009668"
        
        table_rows += f"""
        <tr style="border-bottom: 1px solid #eff4ff;">
            <td style="padding: 16px 24px; font-weight: 700; color: #0b1c30; font-size: 14px;">{d} Okt 2023</td>
            <td style="padding: 16px 24px; font-size: 14px; color: #0b1c30;">{curr:,} kWh</td>
            <td style="padding: 16px 24px; font-size: 14px; color: #76777d;">{prev:,} kWh</td>
            <td style="padding: 16px 24px; font-size: 14px; color: {diff_color}; font-weight: 700;">{diff_str}</td>
        </tr>
        """
        
    table_html = f"""
    <div class="data-card" style="padding: 0px; overflow: hidden; border-radius: 8px; border: 1px solid #e2e8f0; background-color: #ffffff;">
        <div style="overflow-x: auto;">
            <table style="width: 100%; border-collapse: collapse; text-align: left;">
                <thead>
                    <tr style="background-color: #eff4ff; border-bottom: 1px solid #c6c6cd;">
                        <th style="padding: 16px 24px; font-size: 12px; font-weight: 600; color: #45464d; text-transform: uppercase; letter-spacing: 0.05em;">Waktu / Tanggal</th>
                        <th style="padding: 16px 24px; font-size: 12px; font-weight: 600; color: #45464d; text-transform: uppercase; letter-spacing: 0.05em;">Penggunaan Saat Ini</th>
                        <th style="padding: 16px 24px; font-size: 12px; font-weight: 600; color: #45464d; text-transform: uppercase; letter-spacing: 0.05em;">Penggunaan Lalu</th>
                        <th style="padding: 16px 24px; font-size: 12px; font-weight: 600; color: #45464d; text-transform: uppercase; letter-spacing: 0.05em;">Selisih KWh</th>
                    </tr>
                </thead>
                <tbody style="background-color: #ffffff;">
                    {table_rows}
                </tbody>
            </table>
        </div>
        <div style="padding: 16px 24px; background-color: #ffffff; border-top: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center;">
            <button style="border: 1px solid #c6c6cd; background-color: #ffffff; padding: 8px 12px; border-radius: 4px; cursor: pointer; font-size: 12px; font-weight: 600; display: flex; align-items: center; gap: 4px; color: #45464d;">
                <span class="material-symbols-outlined" style="font-size: 16px;">download</span> Ekspor Data (CSV)
            </button>
            <div style="display: flex; gap: 8px;">
                <button style="border: 1px solid #c6c6cd; background-color: #ffffff; padding: 4px 8px; border-radius: 4px; cursor: pointer; color: #45464d; font-weight: bold;"><span class="material-symbols-outlined" style="font-size: 16px;">chevron_left</span></button>
                <button style="border: 1px solid #c6c6cd; background-color: #ffffff; padding: 4px 8px; border-radius: 4px; cursor: pointer; color: #45464d; font-weight: bold;"><span class="material-symbols-outlined" style="font-size: 16px;">chevron_right</span></button>
            </div>
        </div>
    </div>
    """
    st.markdown(table_html.replace('\n', ' '), unsafe_allow_html=True)

    # Contextual Insight Overlay at the bottom
    st.markdown(
        """
        <div style="background-color: #213145; color: #ffffff; padding: 20px; border-radius: 8px; margin-top: 24px; border: 1px solid rgba(255,255,255,0.1); position: relative;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 15px; font-weight: 700; color: white;">Wawasan Efisiensi</span>
                <span class="material-symbols-outlined" style="cursor: pointer; color: #d3e4fe; font-size: 20px;">info</span>
            </div>
            <p style="font-size: 13px; opacity: 0.9; margin: 0; line-height: 1.5; color: #eaf1ff;">
                Penggunaan energi Anda melonjak <b>11.4%</b> dibandingkan minggu lalu. Mayoritas kenaikan terdeteksi pada klaster <b>Produksi Lantai 2</b> selama jam sibuk (10:00 - 14:00).
            </p>
            <div style="margin-top: 16px; display: flex; justify-content: flex-end;">
                <button style="padding: 8px 16px; background-color: #2170e4; color: #ffffff; border: none; border-radius: 4px; font-weight: 600; font-size: 11px; cursor: pointer; text-transform: uppercase; letter-spacing: 0.05em; transition: opacity 0.2s;">
                    Investigasi Detail
                </button>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------- PAGE 3: LIVE MONITORING EV CHARGING ----------------
elif page == "Real-time EV Monitoring":
    build_header("Live Monitoring EV Charging", subtitle_badge="DC FAST STATIONS - SITE 04", temp_str="31°C")
    
    # Hero Metrics Row
    mcol1, mcol2, mcol3 = st.columns(3)
    
    with mcol1:
        st.markdown(
            """
            <div class="data-card">
                <p style="font-size: 11px; font-weight: 600; color: #76777d; text-transform: uppercase; letter-spacing: 0.05em; margin: 0 0 8px 0;">Charger Aktif / Total</p>
                <div style="display: flex; align-items: baseline; gap: 8px;">
                    <span style="font-size: 28px; font-weight: 700; color: #0058be;">12</span>
                    <span style="font-size: 16px; color: #76777d; font-weight: 600;">/ 16 Units</span>
                </div>
                <div style="margin-top: 16px; width: 100%; bg-color: #e5eeff; height: 8px; border-radius: 9999px; overflow: hidden; background-color: #e5eeff;">
                    <div style="background-color: #0058be; height: 100%; width: 75%; border-radius: 9999px;"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with mcol2:
        st.markdown(
            """
            <div class="data-card">
                <p style="font-size: 11px; font-weight: 600; color: #76777d; text-transform: uppercase; letter-spacing: 0.05em; margin: 0 0 8px 0;">Total Beban EV Saat Ini</p>
                <div style="display: flex; align-items: baseline; gap: 8px;">
                    <span style="font-size: 28px; font-weight: 700; color: #0b1c30;">428.5</span>
                    <span style="font-size: 16px; color: #76777d; font-weight: 600;">kW</span>
                </div>
                <div style="margin-top: 12px; display: inline-flex; align-items: center; gap: 4px; color: #005236; font-size: 12px; font-weight: 600;">
                    <span class="material-symbols-outlined" style="font-size: 14px;">trending_up</span>
                    +12% from previous hour
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with mcol3:
        st.markdown(
            """
            <div class="data-card">
                <p style="font-size: 11px; font-weight: 600; color: #76777d; text-transform: uppercase; letter-spacing: 0.05em; margin: 0 0 8px 0;">Pendapatan Hari Ini</p>
                <div style="display: flex; align-items: baseline; gap: 4px;">
                    <span style="font-size: 16px; color: #76777d; font-weight: 600;">Rp.</span>
                    <span style="font-size: 28px; font-weight: 700; color: #0b1c30;">8.420.000</span>
                </div>
                <p style="font-size: 11px; color: #76777d; margin: 12px 0 0 0; font-weight: 600;">Projected: Rp. 10.5M by EOD</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Charger status grid
    st.markdown(
        """
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
            <h3 style="font-size: 18px; font-weight: 700; color: #0b1c30; margin: 0; display: flex; align-items: center; gap: 8px;">
                <span class="material-symbols-outlined" style="color: #0058be;">grid_view</span> Status Unit Charger - Real-time
            </h3>
            <div style="display: flex; align-items: center; gap: 16px;">
                <div style="display: flex; align-items: center; gap: 6px;">
                    <div style="width: 10px; height: 10px; border-radius: 9999px; background-color: #009668;"></div>
                    <span style="font-size: 11px; font-weight: 600; color: #45464d;">Tersedia</span>
                </div>
                <div style="display: flex; align-items: center; gap: 6px;">
                    <div style="width: 10px; height: 10px; border-radius: 9999px; background-color: #0058be;"></div>
                    <span style="font-size: 11px; font-weight: 600; color: #45464d;">Terisi / Charging</span>
                </div>
                <div style="display: flex; align-items: center; gap: 6px;">
                    <div style="width: 10px; height: 10px; border-radius: 9999px; background-color: #ba1a1a;"></div>
                    <span style="font-size: 11px; font-weight: 600; color: #45464d;">Maintenance / Error</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # 4 Units in Grid
    gcol1, gcol2, gcol3, gcol4 = st.columns(4)
    
    with gcol1:
        st.markdown(
            """
            <div class="data-card" style="border: 2px solid #0058be; position: relative;">
              <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px;">
                <div>
                  <p style="font-size: 11px; font-weight: 600; color: #76777d; margin: 0;">Unit 01 (120kW)</p>
                  <h4 style="font-size: 20px; font-weight: 600; color: #0058be; margin: 4px 0 0 0;">Charging...</h4>
                </div>
                <span class="material-symbols-outlined" style="color: #0058be; font-variation-settings: 'FILL' 1;">bolt</span>
              </div>
              <div style="margin-bottom: 24px;">
                <p style="font-family: monospace; font-size: 11px; color: #76777d; margin: 0 0 8px 0;">ID: USR-105</p>
                <div style="display: flex; justify-content: space-between; font-size: 12px; font-weight: 600; margin-bottom: 4px;">
                  <span>SOC: 68%</span>
                  <span>Est: 14 min</span>
                </div>
                <div style="width: 100%; bg-color: #e5eeff; height: 8px; border-radius: 9999px; overflow: hidden; background-color: #e5eeff;">
                  <div style="background-color: #0058be; height: 100%; width: 68%; border-radius: 9999px;"></div>
                </div>
              </div>
              <div style="display: flex; justify-content: space-between; border-top: 1px solid #c6c6cd; padding-top: 12px;">
                <div style="text-align: center;">
                  <p style="font-size: 8px; color: #76777d; text-transform: uppercase; margin: 0;">Voltage</p>
                  <p style="font-size: 12px; font-weight: 700; margin: 0; color: #0b1c30;">402V</p>
                </div>
                <div style="text-align: center;">
                  <p style="font-size: 8px; color: #76777d; text-transform: uppercase; margin: 0;">Current</p>
                  <p style="font-size: 12px; font-weight: 700; margin: 0; color: #0b1c30;">156A</p>
                </div>
                <div style="text-align: center;">
                  <p style="font-size: 8px; color: #76777d; text-transform: uppercase; margin: 0;">Power</p>
                  <p style="font-size: 12px; font-weight: 700; margin: 0; color: #0b1c30;">62.7kW</p>
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with gcol2:
        st.markdown(
            """
            <div class="data-card" style="display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 205px;">
              <div style="width: 54px; height: 54px; border-radius: 9999px; background-color: rgba(111, 251, 190, 0.2); display: flex; align-items: center; justify-content: center; color: #009668; margin-bottom: 12px;">
                <span class="material-symbols-outlined" style="font-size: 30px;">check_circle</span>
              </div>
              <p style="font-size: 11px; font-weight: 600; color: #76777d; margin: 0 0 4px 0;">Unit 02 (50kW)</p>
              <h4 style="font-size: 18px; font-weight: 700; color: #009668; letter-spacing: 0.05em; text-transform: uppercase; margin: 0;">Tersedia</h4>
            </div>
            """,
            unsafe_allow_html=True
        )

    with gcol3:
        st.markdown(
            """
            <div class="data-card" style="border: 2px dashed #ba1a1a; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 205px; background-color: rgba(255, 218, 214, 0.1);">
              <div style="width: 54px; height: 54px; border-radius: 9999px; background-color: rgba(255, 218, 214, 0.3); display: flex; align-items: center; justify-content: center; color: #ba1a1a; margin-bottom: 12px;">
                <span class="material-symbols-outlined" style="font-size: 30px;">warning</span>
              </div>
              <p style="font-size: 11px; font-weight: 600; color: #76777d; margin: 0 0 4px 0;">Unit 03 (50kW)</p>
              <h4 style="font-size: 18px; font-weight: 700; color: #ba1a1a; letter-spacing: 0.05em; text-transform: uppercase; margin: 0;">Error!</h4>
              <p style="font-size: 10px; color: #ba1a1a; margin: 4px 0 0 0;">Check Network Connectivity</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with gcol4:
        st.markdown(
            """
            <div class="data-card" style="border: 2px solid #0058be; position: relative;">
              <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px;">
                <div>
                  <p style="font-size: 11px; font-weight: 600; color: #76777d; margin: 0;">Unit 04 (120kW)</p>
                  <h4 style="font-size: 20px; font-weight: 600; color: #0058be; margin: 4px 0 0 0;">Charging...</h4>
                </div>
                <span class="material-symbols-outlined" style="color: #0058be; font-variation-settings: 'FILL' 1;">bolt</span>
              </div>
              <div style="margin-bottom: 24px;">
                <p style="font-family: monospace; font-size: 11px; color: #76777d; margin: 0 0 8px 0;">ID: USR-YYY</p>
                <div style="display: flex; justify-content: space-between; font-size: 12px; font-weight: 600; margin-bottom: 4px;">
                  <span>SOC: 22%</span>
                  <span>Est: 48 min</span>
                </div>
                <div style="width: 100%; bg-color: #e5eeff; height: 8px; border-radius: 9999px; overflow: hidden; background-color: #e5eeff;">
                  <div style="background-color: #0058be; height: 100%; width: 22%; border-radius: 9999px;"></div>
                </div>
              </div>
              <div style="display: flex; justify-content: space-between; border-top: 1px solid #c6c6cd; padding-top: 12px;">
                <div style="text-align: center;">
                  <p style="font-size: 8px; color: #76777d; text-transform: uppercase; margin: 0;">Voltage</p>
                  <p style="font-size: 12px; font-weight: 700; margin: 0; color: #0b1c30;">440V</p>
                </div>
                <div style="text-align: center;">
                  <p style="font-size: 8px; color: #76777d; text-transform: uppercase; margin: 0;">Current</p>
                  <p style="font-size: 12px; font-weight: 700; margin: 0; color: #0b1c30;">250A</p>
                </div>
                <div style="text-align: center;">
                  <p style="font-size: 8px; color: #76777d; text-transform: uppercase; margin: 0;">Power</p>
                  <p style="font-size: 12px; font-weight: 700; margin: 0; color: #0b1c30;">110kW</p>
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Search bar & Transactions table for EV Charging
    st.markdown("### [Daftar Transaksi EV Charging - Berjalan & Selesai]")
    
    tsearch_col, tspace_col = st.columns([1, 2])
    with tsearch_col:
        trans_search = st.text_input("Cari ID Kendaraan...", placeholder="Cari ID Kendaraan (cth: B 1234 EV)...", label_visibility="collapsed")
        
    charging_tx_list = [
        {"ID": "B 1234 EV", "Tipe": "CCS2 - Fast Charge", "Mulai": "14:22:10", "kWh": "42.5 kWh", "Durasi": "00:42:15", "Biaya": "Rp. 114.750", "Status": "Ongoing"},
        {"ID": "D 5678 ZEV", "Tipe": "Type 2 - AC", "Mulai": "13:45:00", "kWh": "12.2 kWh", "Durasi": "01:15:30", "Biaya": "Rp. 32.940", "Status": "Completed"},
        {"ID": "B 9012 E", "Tipe": "CCS2 - Fast Charge", "Mulai": "14:05:22", "kWh": "28.9 kWh", "Durasi": "00:25:10", "Biaya": "Rp. 78.030", "Status": "Ongoing"},
        {"ID": "F 3456 AC", "Tipe": "CHAdeMO", "Mulai": "12:10:00", "kWh": "55.0 kWh", "Durasi": "00:55:00", "Biaya": "Rp. 148.500", "Status": "Completed"},
    ]

    filtered_ch_tx = [
        t for t in charging_tx_list 
        if trans_search.lower() in t["ID"].lower() or trans_search.lower() in t["Tipe"].lower()
    ]

    table_rows_ch = ""
    for t in filtered_ch_tx:
        status_badge = ""
        if t["Status"] == "Ongoing":
            status_badge = '<span style="background-color: rgba(216, 226, 255, 0.5); color: #0058be; font-weight: 700; font-size: 11px; padding: 4px 10px; border-radius: 9999px; border: 1px solid rgba(0, 88, 190, 0.2);">Ongoing</span>'
        else:
            status_badge = '<span style="background-color: rgba(111, 251, 190, 0.2); color: #009668; font-weight: 700; font-size: 11px; padding: 4px 10px; border-radius: 9999px; border: 1px solid rgba(0, 150, 104, 0.2);">Completed</span>'
            
        table_rows_ch += f"""
        <tr style="border-bottom: 1px solid #eff4ff;">
            <td style="padding: 16px 24px; font-weight: 700; color: #0b1c30; font-size: 14px;">{t["ID"]}</td>
            <td style="padding: 16px 24px; font-size: 14px; color: #0b1c30;">{t["Tipe"]}</td>
            <td style="padding: 16px 24px; font-size: 14px; color: #76777d;">{t["Mulai"]}</td>
            <td style="padding: 16px 24px; font-size: 14px; color: #0b1c30; font-weight: 600;">{t["kWh"]}</td>
            <td style="padding: 16px 24px; font-size: 14px; color: #0b1c30;">{t["Durasi"]}</td>
            <td style="padding: 16px 24px; font-size: 14px; color: #0b1c30; font-weight: 700;">{t["Biaya"]}</td>
            <td style="padding: 16px 24px; text-align: right;">{status_badge}</td>
        </tr>
        """

    if not filtered_ch_tx:
        table_rows_ch = """
        <tr>
            <td colspan="7" style="padding: 32px; text-align: center; color: #76777d; font-style: italic;">Tidak ada transaksi yang ditemukan</td>
        </tr>
        """

    table_ch_html = f"""
    <div class="data-card" style="padding: 0px; overflow: hidden; border-radius: 4px; border: 1px solid #e2e8f0; background-color: #ffffff;">
        <div style="overflow-x: auto;">
            <table style="width: 100%; border-collapse: collapse; text-align: left;">
                <thead>
                    <tr style="background-color: #eff4ff; border-bottom: 1px solid #c6c6cd;">
                        <th style="padding: 16px 24px; font-size: 12px; font-weight: 600; color: #45464d; text-transform: uppercase; letter-spacing: 0.05em;">ID Kendaraan</th>
                        <th style="padding: 16px 24px; font-size: 12px; font-weight: 600; color: #45464d; text-transform: uppercase; letter-spacing: 0.05em;">Tipe Charger</th>
                        <th style="padding: 16px 24px; font-size: 12px; font-weight: 600; color: #45464d; text-transform: uppercase; letter-spacing: 0.05em;">Waktu Mulai</th>
                        <th style="padding: 16px 24px; font-size: 12px; font-weight: 600; color: #45464d; text-transform: uppercase; letter-spacing: 0.05em;">kWh Terpakai</th>
                        <th style="padding: 16px 24px; font-size: 12px; font-weight: 600; color: #45464d; text-transform: uppercase; letter-spacing: 0.05em;">Durasi</th>
                        <th style="padding: 16px 24px; font-size: 12px; font-weight: 600; color: #45464d; text-transform: uppercase; letter-spacing: 0.05em;">Biaya (Estimasi)</th>
                        <th style="padding: 16px 24px; text-align: right; font-size: 12px; font-weight: 600; color: #45464d; text-transform: uppercase; letter-spacing: 0.05em;">Status</th>
                    </tr>
                </thead>
                <tbody style="background-color: #ffffff;">
                    {table_rows_ch}
                </tbody>
            </table>
        </div>
        <div style="padding: 16px 24px; background-color: #ffffff; border-top: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center;">
            <p style="font-size: 12px; color: #76777d; font-weight: 600; margin: 0;">Showing {len(filtered_ch_tx)} of {len(charging_tx_list)} active/recent sessions</p>
            <a href="#" style="color: #0058be; text-decoration: none; font-size: 12px; font-weight: 700; display: inline-flex; align-items: center; gap: 4px;">
                View Audit Log <span class="material-symbols-outlined" style="font-size: 14px;">arrow_forward</span>
            </a>
        </div>
    </div>
    """
    st.markdown(table_ch_html.replace('\n', ' '), unsafe_allow_html=True)


# ---------------- PAGE 4: REPORTS & AUDIT ----------------
elif page == "Reports & Audit":
    build_header("Report & Audit Keuangan / Energi", temp_str="28°C")
    
    # Filter Bar Section
    with st.container(border=True):
        st.markdown("<h4 style='font-size: 12px; font-weight: 700; color: #76777d; text-transform: uppercase; margin: 0 0 16px 0;'>Pilih Jenis Laporan:</h4>", unsafe_allow_html=True)
        
        fcol1, fcol2, fcol3, fcol4 = st.columns([1.2, 1.2, 0.8, 1])
        with fcol1:
            report_type = st.selectbox("Pilih Jenis Laporan", ["Audit Keuangan (BPK)", "Efisiensi Energi Bulanan", "Rekapitulasi Transaksi EV"])
        with fcol2:
            date_range = st.date_input("Rentang Waktu", value=(datetime(2024, 5, 1), datetime(2024, 5, 31)))
        with fcol3:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            show_btn = st.button("Tampilkan", use_container_width=True, type="primary")
        with fcol4:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            if report_type == "Audit Keuangan (BPK)":
                mock_data = [
                    {"Tanggal": "2024-05-01", "Kategori": "Operasional AC", "Daya (kWh)": 12050, "Biaya (Rp)": 20800000},
                    {"Tanggal": "2024-05-15", "Kategori": "Operasional Lampu", "Daya (kWh)": 4200, "Biaya (Rp)": 7250000},
                    {"Tanggal": "2024-05-30", "Kategori": "Stop Kontak / Server", "Daya (kWh)": 8900, "Biaya (Rp)": 15360000}
                ]
            elif report_type == "Efisiensi Energi Bulanan":
                mock_data = [
                    {"Bulan": "Mei 2024", "Target Efisiensi (kWh)": 25000, "Realisasi (kWh)": 24150, "Status": "Target Tercapai"}
                ]
            else:
                mock_data = [
                    {"Tanggal": "2024-05-28", "User ID": "USR-105", "Daya (kWh)": 22.5, "Pemasukan (Rp)": 55000},
                    {"Tanggal": "2024-05-27", "User ID": "USR-098", "Daya (kWh)": 35.0, "Pemasukan (Rp)": 87500},
                    {"Tanggal": "2024-05-27", "User ID": "USR-211", "Daya (kWh)": 18.4, "Pemasukan (Rp)": 46000}
                ]
            df_report = pd.DataFrame(mock_data)
            csv_report = df_report.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                label="Export PDF / CSV / Excel",
                data=csv_report,
                file_name=f"report_{report_type.lower().replace(' ', '_')}.csv",
                mime="text/csv",
                use_container_width=True
            )
            
    # KPI Cards Section
    kcol1, kcol2, kcol3 = st.columns(3)
    
    with kcol1:
        st.markdown(
            """
            <div class="data-card">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;">
                    <p style="font-size: 11px; font-weight: 600; color: #76777d; text-transform: uppercase; letter-spacing: 0.05em; margin: 0;">Total kWh (Periode Terpilih)</p>
                    <span class="material-symbols-outlined" style="color: #0058be;">electric_bolt</span>
                </div>
                <div style="display: flex; align-items: baseline; gap: 8px;">
                    <h3 style="font-size: 28px; font-weight: 700; color: #0b1c30; margin: 0;">12,450.82</h3>
                    <span style="font-size: 14px; color: #76777d; font-weight: 600;">kWh</span>
                </div>
                <div style="margin-top: 16px; display: inline-flex; align-items: center; gap: 4px; color: #005236; background-color: rgba(111, 251, 190, 0.2); padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 700;">
                    <span class="material-symbols-outlined" style="font-size: 14px;">arrow_upward</span>
                    4.2% dibanding bulan lalu
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with kcol2:
        st.markdown(
            """
            <div class="data-card">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;">
                    <p style="font-size: 11px; font-weight: 600; color: #76777d; text-transform: uppercase; letter-spacing: 0.05em; margin: 0;">Estimasi Tagihan PLN (Pengeluaran)</p>
                    <span class="material-symbols-outlined" style="color: #ba1a1a;">payments</span>
                </div>
                <h3 style="font-size: 28px; font-weight: 700; color: #0b1c30; margin: 0; line-height: 1;">Rp 18.245.000</h3>
                <p style="font-size: 11px; color: #76777d; font-weight: 700; text-transform: uppercase; margin: 16px 0 0 0;">Berdasarkan Tarif Golongan B3/TM</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with kcol3:
        st.markdown(
            """
            <div class="data-card">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;">
                    <p style="font-size: 11px; font-weight: 600; color: #76777d; text-transform: uppercase; letter-spacing: 0.05em; margin: 0;">Total Pemasukan EV Charging</p>
                    <span class="material-symbols-outlined" style="color: #009668;">account_balance_wallet</span>
                </div>
                <h3 style="font-size: 28px; font-weight: 700; color: #0b1c30; margin: 0; line-height: 1;">Rp 24.120.500</h3>
                <div style="margin-top: 16px; display: inline-flex; align-items: center; gap: 4px; color: #005236; background-color: rgba(111, 251, 190, 0.2); padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 700;">
                    <span class="material-symbols-outlined" style="font-size: 14px;">arrow_upward</span>
                    12.8% target tercapai
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    # Audit Trail Section
    with st.container(border=True):
        tcol1, tcol2, tcol3 = st.columns([2, 1.2, 0.8])
        with tcol1:
            st.markdown("### Audit Trail - Rekam Jejak Transaksi & Konsumsi")
        with tcol2:
            search_audit = st.text_input("Cari ID Bukti / Tanggal...", label_visibility="collapsed", placeholder="Cari ID Bukti / Tanggal...")
            
        audit_logs = [
            {"tanggal": "28 Mei 2024, 08:30", "tipe": "Konsumsi Harian", "badge_class": "bg-surface-variant text-on-surface-variant", "deskripsi": "Gedung Utama - AC Central L1", "daya": "450.2", "rupiah": "(Pengeluaran)", "rupiah_class": "text-error", "status": "Tercatat", "dot_class": "bg-on-tertiary-container"},
            {"tanggal": "28 Mei 2024, 09:15", "tipe": "Payment Masuk", "badge_class": "bg-secondary-fixed text-on-secondary-fixed-variant", "deskripsi": "ID: USR-105 (EV Charge)", "daya": "22.5", "rupiah": "+ Rp. 55.000", "rupiah_class": "text-on-tertiary-container", "status": "Sukses", "dot_class": "bg-secondary"},
            {"tanggal": "27 Mei 2024, 14:20", "tipe": "Payment Masuk", "badge_class": "bg-secondary-fixed text-on-secondary-fixed-variant", "deskripsi": "ID: USR-098 (EV Charge)", "daya": "35.0", "rupiah": "+ Rp. 87.500", "rupiah_class": "text-on-tertiary-container", "status": "Sukses", "dot_class": "bg-secondary"},
            {"tanggal": "27 Mei 2024, 18:00", "tipe": "Konsumsi Harian", "badge_class": "bg-surface-variant text-on-surface-variant", "deskripsi": "Panel Lampu Parkir B1", "daya": "120.8", "rupiah": "(Pengeluaran)", "rupiah_class": "text-error", "status": "Tercatat", "dot_class": "bg-on-tertiary-container"},
            {"tanggal": "27 Mei 2024, 20:10", "tipe": "Payment Masuk", "badge_class": "bg-secondary-fixed text-on-secondary-fixed-variant", "deskripsi": "ID: USR-211 (EV Charge)", "daya": "18.4", "rupiah": "+ Rp. 46.000", "rupiah_class": "text-on-tertiary-container", "status": "Sukses", "dot_class": "bg-secondary"}
        ]
        
        filtered_logs = [log for log in audit_logs if search_audit.lower() in log["deskripsi"].lower() or search_audit.lower() in log["tanggal"].lower() or search_audit.lower() in log["tipe"].lower()]
        
        # Prepare CSV data for export
        df_export = pd.DataFrame(filtered_logs)
        if not df_export.empty:
            df_export = df_export[["tanggal", "tipe", "deskripsi", "daya", "rupiah", "status"]]
            df_export.columns = ["Tanggal", "Tipe Log", "Deskripsi / ID User", "Daya (kWh)", "Nominal (Rp)", "Status"]
            csv_data = df_export.to_csv(index=False).encode('utf-8')
        else:
            csv_data = b""
            
        with tcol3:
            st.download_button(
                label="Export CSV",
                data=csv_data,
                file_name="audit_trail_report.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        table_rows = ""
        for log in filtered_logs:
            color_style = "color: #ba1a1a;" if log["rupiah"] == "(Pengeluaran)" else "color: #009668;"
            bg_style = "background-color: #d3e4fe; color: #004395;" if log["tipe"] == "Konsumsi Harian" else "background-color: #d8e2ff; color: #001a42;"
            
            table_rows += f"""
            <tr style="border-bottom: 1px solid #eff4ff; font-size: 13px;">
                <td style="padding: 12px 16px; color: #45464d;">{log['tanggal']}</td>
                <td style="padding: 12px 16px;"><span class="px-2 py-0.5 rounded-full text-[10px] font-bold uppercase" style="{bg_style}">{log['tipe']}</span></td>
                <td style="padding: 12px 16px; font-weight: 600; color: #0b1c30;">{log['deskripsi']}</td>
                <td style="padding: 12px 16px; color: #45464d;">{log['daya']}</td>
                <td style="padding: 12px 16px; font-weight: 700; {color_style}">{log['rupiah']}</td>
                <td style="padding: 12px 16px;">
                    <div style="display: flex; align-items: center; gap: 6px; font-weight: 700; color: {'#009668' if log['status'] == 'Tercatat' else '#2170e4'}">
                        <div style="width: 6px; height: 6px; border-radius: 9999px; background-color: {'#009668' if log['status'] == 'Tercatat' else '#2170e4'}"></div>
                        {log['status']}
                    </div>
                </td>
            </tr>
            """
            
        table_html = f"""
        <div class="data-card" style="padding: 0px; overflow: hidden; border-radius: 8px; border: 1px solid #e2e8f0; background-color: #ffffff;">
            <table style="width: 100%; text-align: left; border-collapse: collapse;">
                <thead style="background-color: #eff4ff; color: #45464d; font-size: 11px; text-transform: uppercase; font-weight: 700;">
                    <tr>
                        <th style="padding: 12px 16px; border-bottom: 1px solid #c6c6cd;">Tanggal</th>
                        <th style="padding: 12px 16px; border-bottom: 1px solid #c6c6cd;">Tipe Log</th>
                        <th style="padding: 12px 16px; border-bottom: 1px solid #c6c6cd;">Deskripsi / ID User</th>
                        <th style="padding: 12px 16px; border-bottom: 1px solid #c6c6cd;">Nominal Daya (kWh)</th>
                        <th style="padding: 12px 16px; border-bottom: 1px solid #c6c6cd;">Nominal Rupiah (Rp)</th>
                        <th style="padding: 12px 16px; border-bottom: 1px solid #c6c6cd;">Status</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows if table_rows else '<tr><td colspan="6" style="text-align: center; padding: 20px; color: #76777d;">Data tidak ditemukan</td></tr>'}
                </tbody>
            </table>
        </div>
        """
        st.markdown(table_html.replace('\n', ' '), unsafe_allow_html=True)
        st.markdown("<p style='font-size: 11px; color: #76777d; margin-top: 5px;'>Menampilkan 5 dari 1,240 baris data</p>", unsafe_allow_html=True)


# ---------------- PAGE 5: ADMIN SETTINGS ----------------
elif page == "Admin Settings":
    build_header("Pengaturan Parameter Sistem (Admin)", temp_str="28°C")
    
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.markdown("### 1. Tarif Dasar Listrik (PLN)")
            st.markdown("<p style='font-size: 13px; color: #76777d;'>Digunakan untuk estimasi pengeluaran tagihan gedung.</p>", unsafe_allow_html=True)
            
            tarif_input = st.number_input("Harga per kWh (Rp)", min_value=1, value=st.session_state["tarif_pln"])
            if st.button("Simpan Perubahan Tarif PLN", type="primary"):
                st.session_state["tarif_pln"] = tarif_input
                st.success("Tarif PLN berhasil diperbarui!")
                
    with col2:
        with st.container(border=True):
            st.markdown("### 2. Tarif Layanan EV Charging")
            st.markdown("<p style='font-size: 13px; color: #76777d;'>Tarif jual ke user berdasarkan kecepatan charger.</p>", unsafe_allow_html=True)
            
            ev_50 = st.number_input("Tipe 50kW (Rp/kWh)", min_value=1, value=st.session_state["tarif_ev_50"])
            ev_120 = st.number_input("Tipe 120kW (Rp/kWh)", min_value=1, value=st.session_state["tarif_ev_120"])
            if st.button("Simpan Perubahan Tarif EV", type="primary"):
                st.session_state["tarif_ev_50"] = ev_50
                st.session_state["tarif_ev_120"] = ev_120
                st.success("Tarif EV Charging berhasil diperbarui!")
                
    with st.container(border=True):
        st.markdown("### 3. Target Baseline Energi")
        st.markdown("<p style='font-size: 13px; color: #76777d;'>Tentukan batas maksimal konsumsi untuk grafik & notifikasi peringatan.</p>", unsafe_allow_html=True)
        
        base_col1, base_col2, base_col3 = st.columns([1.2, 1.2, 0.8])
        with base_col1:
            tipe_rentang_input = st.selectbox("Tipe Rentang", ["Harian (Per Hari)", "Mingguan (Per Minggu)", "Bulanan (Per Bulan)"], index=["Harian (Per Hari)", "Mingguan (Per Minggu)", "Bulanan (Per Bulan)"].index(st.session_state["tipe_rentang"]))
        with base_col2:
            batas_angka_input = st.number_input("Batas Angka (kWh)", min_value=1, value=st.session_state["batas_angka"])
        with base_col3:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            if st.button("Simpan Target", use_container_width=True, type="primary"):
                st.session_state["tipe_rentang"] = tipe_rentang_input
                st.session_state["batas_angka"] = batas_angka_input
                st.success("Target Baseline berhasil diperbarui!")
                
    with st.container(border=True):
        st.markdown("### 4. Manajemen Kategori Beban (Pie Chart)")
        st.markdown("<p style='font-size: 13px; color: #76777d;'>Daftar kategori alat yang dimonitor konsumsinya.</p>", unsafe_allow_html=True)
        
        cat_cols = st.columns(4)
        for idx, cat in enumerate(st.session_state["categories"]):
            col_idx = idx % 4
            with cat_cols[col_idx]:
                st.markdown(
                    f"""
                    <div style="padding: 10px 14px; background-color: #f8f9ff; border: 1px solid #c6c6cd; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <span style="font-weight: 600; color: #0b1c30; font-size: 13px;">{cat}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                if st.button(f"Hapus {cat}", key=f"del_{cat}_{idx}", use_container_width=True):
                    st.session_state["categories"].remove(cat)
                    st.rerun()
                    
        st.markdown("<hr style='margin: 15px 0; border-color: #eff4ff;'>", unsafe_allow_html=True)
        add_col1, add_col2 = st.columns([3, 1])
        with add_col1:
            new_cat_name = st.text_input("Nama Kategori Baru:", placeholder="Masukkan nama kategori...", label_visibility="collapsed")
        with add_col2:
            if st.button("Tambah Kategori", type="primary", use_container_width=True):
                if new_cat_name and new_cat_name not in st.session_state["categories"]:
                    st.session_state["categories"].append(new_cat_name)
                    st.success(f"Kategori '{new_cat_name}' ditambahkan!")
                    st.rerun()
