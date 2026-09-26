import streamlit as st
import requests
from PIL import Image
import io
import base64
import os
from gtts import gTTS

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="AgriShield AI | Smart Agriculture Advisory",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Custom CSS Layout & Tight Spacing Adjustments
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* Reduce top and bottom padding of main page */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }

    /* Transparent Top Header Bar */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* Background Setup */
    .stApp {
        background: linear-gradient(rgba(15, 23, 42, 0.25), rgba(15, 23, 42, 0.3)), 
                    url('https://images.unsplash.com/photo-1500382017468-9049fed747ef?q=80&w=2000&auto=format&fit=crop');
        background-size: cover;
        background-position: center top;
        background-attachment: fixed;
        color: #ffffff;
        font-family: 'Inter', -apple-system, sans-serif;
    }

    /* Dark Glass Sidebar Container */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.90) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* TIGHT SIDEBAR SPACING FIXES */
    section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] > div {
        gap: 0.35rem !important;
    }

    section[data-testid="stSidebar"] hr {
        margin-top: 0.4rem !important;
        margin-bottom: 0.4rem !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
    }

    section[data-testid="stSidebar"] h3 {
        padding-top: 0.1rem !important;
        padding-bottom: 0.1rem !important;
        margin-bottom: 0.2rem !important;
        font-size: 1.05rem !important;
    }

    /* Sidebar Headers, Labels & Text */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] .stMarkdown {
        color: #ffffff !important;
        font-weight: 600 !important;
    }

    /* FIX SELECTBOX VISIBILITY IN SIDEBAR */
    section[data-testid="stSidebar"] div[data-baseweb="select"] * {
        color: #0f172a !important;
        font-weight: 600 !important;
    }

    /* Main Page Titles */
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #22c55e;
        margin-top: -0.5rem;
        margin-bottom: 0rem;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.9);
    }
    
    .sub-title {
        color: #ffffff;
        font-size: 1rem;
        font-weight: 500;
        margin-bottom: 1rem;
        text-shadow: 0 2px 6px rgba(0, 0, 0, 0.9);
    }

    /* Column Section Labels */
    .section-label {
        color: #ffffff;
        font-size: 1.15rem;
        font-weight: 700;
        text-shadow: 0 2px 6px rgba(0, 0, 0, 0.9);
        margin-bottom: 0.5rem;
        height: 30px;
    }

    /* COMPACT & WIDE FILE UPLOADER FIX */
    div[data-testid="stFileUploader"] {
        width: 100% !important;
    }

    div[data-testid="stFileUploaderDropzone"],
    div[data-baseweb="file-uploader"] {
        height: 48px !important;
        min-height: 48px !important;
        background-color: rgba(255, 255, 255, 0.95) !important;
        border: 2px dashed #16a34a !important;
        border-radius: 10px !important;
        padding: 4px 12px !important;
        backdrop-filter: blur(8px) !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4) !important;
    }

    div[data-testid="stFileUploaderDropzone"] * {
        color: #0f172a !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
    }

    /* IMAGE SIZE CONSTRAINTS */
    div[data-testid="stImage"] img {
        max-height: 240px !important;
        object-fit: contain !important;
        width: auto !important;
        margin: 0 auto !important;
        display: block !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5) !important;
    }

    .custom-diagnostic-card {
        background-color: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        padding: 20px;
        backdrop-filter: blur(8px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
        color: #ffffff;
        font-size: 0.95rem;
        font-weight: 500;
        text-align: center;
    }

    /* Action Button */
    .stButton>button {
        background: linear-gradient(90deg, #22c55e 0%, #16a34a 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        border: none !important;
        height: 48px !important;
        padding: 0.5rem 1rem !important;
        width: 100%;
        font-size: 0.95rem !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.5);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(34, 197, 94, 0.6);
    }

    /* Inline Status Badge */
    .inline-status-badge {
        background-color: rgba(15, 23, 42, 0.92);
        border: 1px solid rgba(34, 197, 94, 0.5);
        border-radius: 10px;
        padding: 8px 12px;
        margin-bottom: 10px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
        color: #ffffff;
        font-size: 0.9rem;
        font-weight: 500;
        text-align: center;
    }

    .inline-status-badge strong {
        color: #4ade80;
        margin-right: 5px;
    }

    /* Metric Display */
    div[data-testid="stMetricValue"] {
        color: #4ade80 !important;
        font-weight: 800;
    }

    /* Recommendation Box High Contrast */
    div[data-testid="stAlert"] {
        background-color: rgba(15, 23, 42, 0.92) !important;
        border: 1px solid rgba(34, 197, 94, 0.5) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.6) !important;
        padding: 16px !important;
    }

    div[data-testid="stAlert"] * {
        color: #ffffff !important;
        font-size: 0.95rem !important;
        line-height: 1.5 !important;
        font-weight: 500 !important;
    }

    div[data-testid="stAlert"] strong {
        color: #4ade80 !important;
        font-weight: 700 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Language to gTTS Language Code Mapping
GTTS_LANG_CODES = {
    "Bengali": "bn",
    "English": "en",
    "Hindi": "hi",
    "Kannada": "kn",
    "Marathi": "mr",
    "Odia (Oriya)": "or",
    "Tamil": "ta",
    "Telugu": "te"
}

# ---------------------------------------------------------
# Sidebar Section 1: Parameters
# ---------------------------------------------------------
st.sidebar.markdown("### 🛠️ Inference Parameters")

model_version = st.sidebar.radio(
    "YOLO Model Engine",
    ["v2", "v1"],
    index=0,
    help="Select v2 for higher accuracy on field pest datasets."
)

confidence_threshold = st.sidebar.slider(
    "Confidence Threshold",
    min_value=0.10,
    max_value=0.95,
    value=0.35,
    step=0.05,
    help="Increase this value if you encounter false detections."
)

st.sidebar.markdown("---")

# ---------------------------------------------------------
# Sidebar Section 2: Preferred Language
# ---------------------------------------------------------
st.sidebar.markdown("### 🌐 Preferred Language")

language = st.sidebar.radio(
    "Select Language for Advisory",
    list(GTTS_LANG_CODES.keys()),
    index=5
)

st.sidebar.markdown("---")

# ---------------------------------------------------------
# Sidebar Section 3: Dynamic Sample Image Reader (Compact)
# ---------------------------------------------------------
st.sidebar.markdown("### 🖼️ Quick Demo Samples")

SAMPLES_DIR = "samples"
available_samples = {"None (Upload Custom File)": None}

if os.path.exists(SAMPLES_DIR):
    valid_extensions = (".jpg", ".jpeg", ".png", ".webp")
    files = sorted(os.listdir(SAMPLES_DIR))
    for fname in files:
        if fname.lower().endswith(valid_extensions):
            clean_name = os.path.splitext(fname)[0].replace("_", " ").replace("-", " ").title()
            label = f"🐛 {clean_name} ({fname})"
            available_samples[label] = os.path.join(SAMPLES_DIR, fname)

selected_sample_label = st.sidebar.selectbox(
    "Choose Target Sample",
    options=list(available_samples.keys()),
    index=0
)

# Endpoints (LOCAL MODE DEFAULT)
FASTAPI_ENDPOINT = "http://localhost:8000/predict"
N8N_WEBHOOK_URL = "https://surjyanp.app.n8n.cloud/webhook/pest-action"

# ---------------------------------------------------------
# Main Header
# ---------------------------------------------------------
st.markdown('<div class="main-title">🌾 AgriShield AI Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Real-time pest detection & localized multilingual treatment recommendations</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# 3-COLUMN SCREEN LAYOUT (Horizontally Aligned Tops)
# ---------------------------------------------------------
col1, col2, col3 = st.columns([1, 1, 1.1], gap="medium")

# State variables
image_bytes = None
image_filename = None
image_to_display = None
detected_pest = None
confidence = 0.0

# --- PORTION 1: IMAGE UPLOAD ---
with col1:
    st.markdown('<div class="section-label">📸 1. Image Upload</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Choose plant image", 
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )

    sample_path = available_samples.get(selected_sample_label)

    if uploaded_file is not None:
        image_bytes = uploaded_file.getvalue()
        image_filename = uploaded_file.name
        image_to_display = Image.open(uploaded_file)
    elif sample_path and os.path.exists(sample_path):
        with open(sample_path, "rb") as f:
            image_bytes = f.read()
        image_filename = os.path.basename(sample_path)
        image_to_display = Image.open(sample_path)

    if image_to_display:
        st.image(image_to_display, caption=f"Input Image: {image_filename}")

# --- PORTION 2: AI DIAGNOSTICS & THREAT ASSESSMENT ---
with col2:
    st.markdown('<div class="section-label">🔬 2. AI Diagnostics</div>', unsafe_allow_html=True)
    
    if image_bytes is not None:
        scan_clicked = st.button("RUN DIAGNOSTIC SCAN 🚀")

        if scan_clicked or "last_detection" in st.session_state:
            if scan_clicked:
                with st.spinner("Analyzing image..."):
                    try:
                        files = {"file": (image_filename, image_bytes, "image/jpeg")}
                        data_payload = {
                            "model_version": model_version,
                            "conf": confidence_threshold
                        }
                        
                        fastapi_res = requests.post(
                            FASTAPI_ENDPOINT, 
                            files=files, 
                            data=data_payload, 
                            timeout=15
                        )
                        
                        if fastapi_res.status_code == 200:
                            st.session_state["last_detection"] = fastapi_res.json()
                        else:
                            st.error(f"FastAPI Backend Error ({fastapi_res.status_code})")
                            st.session_state["last_detection"] = None

                    except Exception as e:
                        st.error("Failed to connect to backend server.")
                        st.caption(f"Details: {e}")
                        st.session_state["last_detection"] = None

            # Render Detection & Severity Gauge
            res_json = st.session_state.get("last_detection")
            if res_json:
                detections = res_json.get("detections", [])
                if len(detections) > 0:
                    detected_pest = detections[0].get("pest_name", "unknown")
                    confidence = float(detections[0].get("confidence", 0.0))
                    
                    st.markdown(
                        f'<div class="inline-status-badge"><strong>Detected Condition:</strong> {detected_pest} ({confidence * 100:.1f}%)</div>', 
                        unsafe_allow_html=True
                    )
                    
                    # Threat Severity Gauge
                    st.progress(confidence)
                    if confidence > 0.75:
                        st.error("🚨 **High Severity:** Immediate intervention required within 24–48 hrs.")
                    elif confidence > 0.40:
                        st.warning("⚠️ **Moderate Severity:** Monitor crop density and isolate affected area.")
                    else:
                        st.info("ℹ️ **Low Severity:** Early indication. Apply preventive bio-pesticides.")

                else:
                    detected_pest = "unknown"
                    st.markdown(
                        '<div class="inline-status-badge"><span style="color:#f59e0b;">⚠️ No pest detected above threshold</span></div>', 
                        unsafe_allow_html=True
                    )

                if "annotated_image" in res_json:
                    img_bytes = base64.b64decode(res_json["annotated_image"])
                    annotated_img = Image.open(io.BytesIO(img_bytes))
                    st.image(annotated_img, caption="YOLO Bounding Box Visualization")
    else:
        st.markdown(
            '<div class="custom-diagnostic-card">Select a sample image on the sidebar or upload an image to start.</div>', 
            unsafe_allow_html=True
        )

# --- PORTION 3: TREATMENT ADVISORY, TTS AUDIO & DOWNLOADABLE REPORT ---
with col3:
    st.markdown('<div class="section-label">📋 3. Treatment Advisory</div>', unsafe_allow_html=True)
    
    if detected_pest and detected_pest != "unknown":
        with st.spinner(f"Retrieving advisory in {language}..."):
            try:
                payload = {
                    "pest": detected_pest,
                    "language": language
                }
                
                n8n_res = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=20)
                
                if n8n_res.status_code == 200:
                    n8n_data = n8n_res.json()
                    
                    chemical_solution = n8n_data.get("chemical", "N/A")
                    st.metric(label="Chemical Solution", value=chemical_solution)
                    
                    instructions = n8n_data.get("translated_instructions", "No advisory available.")
                    st.info(f"**Instructions ({language}):**\n\n{instructions}")
                    
                    # --- FEATURE 1: MULTILINGUAL AUDIO TTS ---
                    st.markdown("🔊 **Listen to Local Advisory:**")
                    try:
                        tts_lang = GTTS_LANG_CODES.get(language, "en")
                        tts_text = f"{detected_pest}. {chemical_solution}. {instructions}"
                        
                        tts = gTTS(text=tts_text, lang=tts_lang, slow=False)
                        fp = io.BytesIO()
                        tts.write_to_fp(fp)
                        fp.seek(0)
                        
                        st.audio(fp, format="audio/mp3")
                    except Exception as audio_err:
                        st.caption("🔊 *Audio player unavailable for selected language.*")

                    st.markdown("---")
                    
                    # --- FEATURE 3: DOWNLOADABLE FIELD REPORT ---
                    report_content = f"""==================================================
AGRISHIELD AI - FIELD ADVISORY REPORT
==================================================
Detected Pest / Condition : {detected_pest}
Model Confidence          : {confidence * 100:.1f}%
Selected Advisory Language: {language}
Chemical Solution         : {chemical_solution}

RECOMMENDED TREATMENT ACTION PLAN:
--------------------------------------------------
{instructions}

COMMUNITY SUPPORT & HELPLINE:
Kisan Call Center Hotline: 1800-180-1551
==================================================
"""
                    st.download_button(
                        label="📥 Download Advisory Report (TXT)",
                        data=report_content,
                        file_name=f"AgriShield_Advisory_{detected_pest}.txt",
                        mime="text/plain"
                    )

                else:
                    st.error(f"n8n Workflow Error: {n8n_res.status_code}")

            except Exception as e:
                st.error("Error communicating with n8n advisory agent.")
                st.caption(f"Details: {e}")

    elif detected_pest == "unknown":
        st.info("💡 **Tip:** Try lowering the **Confidence Threshold** slider in the sidebar or select a different sample image.")
    else:
        st.markdown(
            '<div class="custom-diagnostic-card">Scan results and localized treatment manuals will appear here after diagnostic processing.</div>', 
            unsafe_allow_html=True
        )