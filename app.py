import streamlit as st
import requests
from PIL import Image
import io
import base64
import os
from pathlib import Path
from gtts import gTTS
from ultralytics import YOLO

BASE_DIR = Path(__file__).resolve().parent

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Kishan Mitra AI | Smart Agriculture Advisory",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Custom CSS Layout & Tight Spacing Adjustments
# ---------------------------------------------------------
st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 6rem !important;
    }

    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }

    .stApp {
        background: linear-gradient(rgba(15, 23, 42, 0.25), rgba(15, 23, 42, 0.3)), 
                    url('https://images.unsplash.com/photo-1500382017468-9049fed747ef?q=80&w=2000&auto=format&fit=crop');
        background-size: cover;
        background-position: center top;
        background-attachment: fixed;
        color: #ffffff;
        font-family: 'Inter', -apple-system, sans-serif;
    }

    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.90) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.2);
    }

    section[data-testid="stSidebar"] div[data-testid="stSidebarContent"] {
        padding-top: 0.1rem !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stSidebarUserContent"] {
        padding-top: 0 !important;
        margin-top: -3.25rem !important;
    }

    .ai-advisory-footer {
        position: fixed;
        left: 20rem;
        right: 1.25rem;
        bottom: 0.75rem;
        z-index: 999;
        padding: 0.75rem 1rem;
        border: 1px solid rgba(245, 158, 11, 0.75);
        border-radius: 12px;
        background: rgba(69, 65, 31, 0.96);
        color: #ffffff;
        font-size: 0.92rem;
        line-height: 1.35;
        text-align: center;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35);
    }

    @media (max-width: 768px) {
        .ai-advisory-footer {
            left: 0.75rem;
            right: 0.75rem;
            bottom: 0.5rem;
        }
    }
    
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

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] .stMarkdown {
        color: #ffffff !important;
        font-weight: 600 !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="select"] * {
        color: #0f172a !important;
        font-weight: 600 !important;
    }

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

    .section-label {
        color: #ffffff;
        font-size: 1.15rem;
        font-weight: 700;
        text-shadow: 0 2px 6px rgba(0, 0, 0, 0.9);
        margin-bottom: 0.5rem;
        height: 30px;
    }

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

    div[data-testid="stMetricValue"] {
        color: #4ade80 !important;
        font-weight: 800;
    }

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

    /* Keep the feedback form readable over the photographic background. */
    div[data-testid="stExpander"] details {
        overflow: hidden !important;
        background: rgba(15, 23, 42, 0.96) !important;
        border: 1px solid rgba(255, 255, 255, 0.24) !important;
        border-radius: 12px !important;
        box-shadow: 0 6px 22px rgba(0, 0, 0, 0.45) !important;
        backdrop-filter: blur(12px) !important;
    }

    div[data-testid="stExpander"] details > summary {
        background: rgba(15, 23, 42, 0.98) !important;
    }

    div[data-testid="stExpander"] details > summary,
    div[data-testid="stExpander"] details > summary * {
        color: #ffffff !important;
        fill: #ffffff !important;
        font-weight: 700 !important;
    }

    div[data-testid="stExpander"] div[data-testid="stForm"] {
        padding: 0.25rem 0.25rem 0.5rem !important;
    }

    div[data-testid="stExpander"] label,
    div[data-testid="stExpander"] label p,
    div[data-testid="stExpander"] div[role="radiogroup"] label,
    div[data-testid="stExpander"] div[role="radiogroup"] label * {
        color: #ffffff !important;
        opacity: 1 !important;
        font-weight: 600 !important;
    }

    div[data-testid="stExpander"] textarea {
        color: #0f172a !important;
        background: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        caret-color: #0f172a !important;
    }

    div[data-testid="stExpander"] textarea::placeholder {
        color: #64748b !important;
        opacity: 1 !important;
    }

    div[data-testid="stExpander"] div[data-testid="stFormSubmitButton"] button {
        min-width: 180px !important;
        height: 48px !important;
        padding: 0.5rem 1rem !important;
        color: #ffffff !important;
        background: linear-gradient(90deg, #22c55e 0%, #16a34a 100%) !important;
        border: none !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.45) !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
    }

    div[data-testid="stExpander"] div[data-testid="stFormSubmitButton"] button:hover {
        background: linear-gradient(90deg, #16a34a 0%, #15803d 100%) !important;
        transform: translateY(-1px);
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

CROP_STAGES = {
    "Wheat": ["Seedling", "Tillering", "Stem elongation", "Heading / Flowering", "Grain filling"],
    "Maize": ["Seedling", "Vegetative", "Tasseling / Silking", "Grain filling"],
}

INDIAN_STATES = [
    "Select state", "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar",
    "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand",
    "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya",
    "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
    "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
    "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu",
    "Delhi", "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry",
]

# ---------------------------------------------------------
# Fixed Inference Configuration
# ---------------------------------------------------------
model_version = "v2"
confidence_threshold = 0.15

# ---------------------------------------------------------
# Sidebar Section 1: Farm & Crop Details
# ---------------------------------------------------------
st.sidebar.markdown("### 🌾 Farm & Crop Details")

selected_crop = st.sidebar.selectbox("Crop", list(CROP_STAGES.keys()))
selected_growth_stage = st.sidebar.selectbox("Growth stage", CROP_STAGES[selected_crop])
selected_state = st.sidebar.selectbox("State / UT", INDIAN_STATES)
selected_district = st.sidebar.text_input("District", placeholder="Enter district")

st.sidebar.markdown("---")

# ---------------------------------------------------------
# Sidebar Section 2: Dynamic Sample Image Reader (Compact)
# ---------------------------------------------------------
st.sidebar.markdown("### 🖼️ Quick Demo Samples")

SAMPLES_DIR = BASE_DIR / "samples"
available_samples = {"None (Upload Custom File)": None}

if os.path.exists(SAMPLES_DIR):
    valid_extensions = (".jpg", ".jpeg", ".png", ".webp")
    files = sorted(os.listdir(SAMPLES_DIR))
    for fname in files:
        if fname.lower().endswith(valid_extensions):
            clean_name = os.path.splitext(fname)[0].replace("_", " ").replace("-", " ").title()
            label = f"🐛 {clean_name} ({fname})"
            available_samples[label] = SAMPLES_DIR / fname

selected_sample_label = st.sidebar.selectbox(
    "Choose Target Sample",
    options=list(available_samples.keys()),
    index=0
)

st.sidebar.markdown("---")

# ---------------------------------------------------------
# Sidebar Section 3: Preferred Language
# ---------------------------------------------------------
st.sidebar.markdown("### 🌐 Preferred Language")

language = st.sidebar.radio(
    "Select Language for Advisory",
    list(GTTS_LANG_CODES.keys()),
    index=list(GTTS_LANG_CODES.keys()).index("Hindi")
)

# n8n Webhook for Multilingual Treatment Advisory Text
N8N_WEBHOOK_URL = "https://surjyanp.app.n8n.cloud/webhook/pest-action"
FEEDBACK_WEBHOOK_URL = os.getenv(
    "N8N_FEEDBACK_WEBHOOK_URL",
    "https://surjyanp.app.n8n.cloud/webhook/agrishield-feedback",
)

# ---------------------------------------------------------
# Local YOLO Model Caching and Loading
# ---------------------------------------------------------
@st.cache_resource
def load_yolo_model(version):
    requested_file = BASE_DIR / ("best_v2.pt" if version == "v2" else "best_v1.pt")
    fallback_file = BASE_DIR / "best_v1.pt"
    weight_file = requested_file if requested_file.exists() else fallback_file
    if not weight_file.exists():
        raise FileNotFoundError(
            "YOLO model weights are missing. Expected best_v1.pt or best_v2.pt "
            f"in {BASE_DIR}."
        )
    return YOLO(str(weight_file))

try:
    model = load_yolo_model(model_version)
except Exception as e:
    st.error(f"Error loading model weights: {e}")
    model = None


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_advisory(pest, language_name, crop_name, crop_stage, state_name, district_name):
    response = requests.post(
        N8N_WEBHOOK_URL,
        json={
            "pest": pest,
            "language": language_name,
            "crop": crop_name,
            "growth_stage": crop_stage,
            "state": state_name,
            "district": district_name,
        },
        timeout=20,
    )
    response.raise_for_status()
    return response.json()


def submit_feedback(crop, growth_stage, state, district, image, diagnosis, helpful, note):
    response = requests.post(
        FEEDBACK_WEBHOOK_URL,
        json={
            "crop": crop,
            "growth_stage": growth_stage,
            "state": state,
            "district": district,
            "image": image,
            "diagnosis": diagnosis,
            "helpful": helpful,
            "note": note,
        },
        timeout=20,
    )
    response.raise_for_status()
    return response.json() if response.content else {"status": "success"}


@st.cache_data(ttl=3600, show_spinner=False)
def generate_advisory_audio(text, language_code):
    audio_buffer = io.BytesIO()
    gTTS(text=text, lang=language_code, slow=False).write_to_fp(audio_buffer)
    return audio_buffer.getvalue()

# ---------------------------------------------------------
# Main Header
# ---------------------------------------------------------
st.markdown('<div class="main-title">🌾 Kishan Mitra AI Platform</div>', unsafe_allow_html=True)
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
    elif sample_path and sample_path.exists():
        with sample_path.open("rb") as f:
            image_bytes = f.read()
        image_filename = sample_path.name
        image_to_display = Image.open(sample_path)

    input_signature = (
        image_filename,
        len(image_bytes) if image_bytes is not None else 0,
        model_version,
        confidence_threshold,
        selected_crop,
        selected_growth_stage,
        selected_state,
        selected_district.strip().lower(),
    )
    if st.session_state.get("input_signature") != input_signature:
        st.session_state["input_signature"] = input_signature
        st.session_state.pop("last_detection", None)

    if image_to_display:
        st.image(image_to_display, caption=f"Input Image: {image_filename}")

# --- PORTION 2: AI DIAGNOSTICS & THREAT ASSESSMENT (LOCAL YOLO) ---
with col2:
    st.markdown('<div class="section-label">🔬 2. AI Diagnostics</div>', unsafe_allow_html=True)
    
    if image_to_display is not None:
        scan_clicked = st.button("RUN DIAGNOSTIC SCAN 🚀")

        if scan_clicked or "last_detection" in st.session_state:
            if scan_clicked:
                if model is None:
                    st.error("YOLO model weights are not loaded.")
                else:
                    with st.spinner("Analyzing image locally..."):
                        try:
                            # Run local inference
                            results = model(image_to_display, conf=confidence_threshold)
                            res = results[0]
                            
                            detections_list = []
                            for box in res.boxes:
                                cls_id = int(box.cls[0])
                                conf_val = float(box.conf[0])
                                p_name = model.names.get(cls_id, "unknown")
                                detections_list.append({"pest_name": p_name, "confidence": conf_val})
                            
                            # Render annotated image
                            annotated_arr = res.plot()  # BGR numpy array
                            annotated_rgb = annotated_arr[..., ::-1] # Convert BGR to RGB
                            
                            pil_annotated = Image.fromarray(annotated_rgb)
                            buffered = io.BytesIO()
                            pil_annotated.save(buffered, format="JPEG")
                            encoded_img = base64.b64encode(buffered.getvalue()).decode()

                            st.session_state["last_detection"] = {
                                "detections": detections_list,
                                "annotated_image": encoded_img
                            }
                        except Exception as e:
                            st.error("Error during local model inference.")
                            st.caption(f"Details: {e}")
                            st.session_state["last_detection"] = None

            # Render Detection & Severity Gauge
            res_json = st.session_state.get("last_detection")
            if res_json:
                detections = res_json.get("detections", [])
                if len(detections) > 0:
                    detections = sorted(
                        detections,
                        key=lambda item: float(item.get("confidence", 0.0)),
                        reverse=True,
                    )
                    detected_pest = detections[0].get("pest_name", "unknown")
                    confidence = float(detections[0].get("confidence", 0.0))

                    st.markdown(
                        f'<div class="inline-status-badge"><strong>Detected Condition:</strong> {detected_pest} ({confidence * 100:.1f}%)</div>',
                        unsafe_allow_html=True
                    )

                    st.caption("AI confidence (not field infestation severity)")
                    st.progress(confidence)
                    st.info("✅ Detection passed the fixed 15% confidence threshold.")

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

# --- PORTION 3: TREATMENT ADVISORY, TTS AUDIO & DOWNLOADABLE REPORT ---
with col3:
    st.markdown('<div class="section-label">📋 3. Treatment Advisory</div>', unsafe_allow_html=True)
    
    if detected_pest and detected_pest != "unknown":
        with st.spinner(f"Retrieving advisory in {language}..."):
            try:
                n8n_data = fetch_advisory(
                    detected_pest,
                    language,
                    selected_crop,
                    selected_growth_stage,
                    selected_state,
                    selected_district.strip(),
                )

                chemical_solution = n8n_data.get("chemical", "N/A")
                st.metric(label="Chemical Solution", value=chemical_solution)

                instructions = n8n_data.get("translated_instructions", "No advisory available.")
                st.info(f"**Instructions ({language}):**\n\n{instructions}")

                # --- MULTILINGUAL AUDIO TTS ---
                st.markdown("🔊 **Listen to Local Advisory:**")
                try:
                    tts_lang = GTTS_LANG_CODES.get(language, "en")
                    tts_text = f"{detected_pest}. {chemical_solution}. {instructions}"
                    audio_bytes = generate_advisory_audio(tts_text, tts_lang)
                    st.audio(audio_bytes, format="audio/mp3")
                except Exception:
                    st.caption("🔊 *Audio player unavailable for selected language.*")

                st.markdown("---")
                    
                # --- DOWNLOADABLE FIELD REPORT ---
                report_content = f"""==================================================
KISHAN MITRA AI - FIELD ADVISORY REPORT
==================================================
Crop                       : {selected_crop}
Growth Stage               : {selected_growth_stage}
Location                   : {selected_district or 'Not provided'}, {selected_state}
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
                    file_name=f"Kishan_Mitra_Advisory_{detected_pest}.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error("Error communicating with n8n advisory agent.")
                st.caption(f"Details: {e}")

    elif detected_pest == "unknown":
        st.info("💡 **No detection above 15%:** Try a clearer close-up or select a different sample image.")

if st.session_state.get("last_detection"):
    with st.expander("💬 Farmer Feedback"):
        with st.form("farmer_feedback_form", clear_on_submit=True):
            feedback_choice = st.radio(
                "Was this diagnosis helpful?",
                ["Yes", "No", "Not sure"],
                horizontal=True,
                index=None,
            )
            feedback_note = st.text_area(
                "Optional note",
                placeholder="Tell us what looked right or wrong",
            )
            feedback_submitted = st.form_submit_button("Submit feedback")

        if feedback_submitted:
            if feedback_choice is None:
                st.warning("Please select Yes, No, or Not sure.")
            else:
                try:
                    with st.spinner("Submitting feedback..."):
                        result = submit_feedback(
                            selected_crop,
                            selected_growth_stage,
                            selected_state,
                            selected_district.strip(),
                            image_filename or "",
                            detected_pest or "",
                            feedback_choice,
                            feedback_note.strip(),
                        )
                    if result.get("status") == "success":
                        st.success("Thank you. Your feedback has been saved.")
                    else:
                        st.error("The feedback service returned an unexpected response.")
                except requests.RequestException as e:
                    st.error("Could not submit feedback. Please try again.")
                    st.caption(f"Details: {e}")

st.markdown(
    '<div class="ai-advisory-footer"><strong>AI-generated advisory.</strong> '
    'Confirm pesticide selection and dosage with a qualified agricultural expert or local '
    'agriculture officer before application.</div>',
    unsafe_allow_html=True,
)
