import streamlit as st
import pytesseract
from PIL import Image
from gtts import gTTS
import img2pdf
from pypdf import PdfReader
import io
import cv2
import numpy as np
from pyzbar.pyzbar import decode

# --- 1. ARCHITECTURAL CONFIG & STYLING ---
st.set_page_config(page_title="Architect Hub", page_icon="📑", layout="wide")

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; background-color: #1E1E1E; color: white; border: 1px solid #333; }
    .stButton>button:hover { background-color: #333; border: 1px solid #007BFF; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("🛠️ Intelligence Hub")
    st.write("Role: **AI Solutions Architect**")
    st.divider()
    choice = st.radio("Select Tool", [
        "🖼️ Image to PDF", 
        "🔊 Text to Audio", 
        "👁️ Image Scanner (OCR)", 
        "📄 PDF Metadata",
        "📸 QR Code Tools"
    ])
    st.divider()
    st.caption("v1.2 | Be kind to your mind.")

# --- 3. TOOL LOGIC ---

# --- QR CODE TOOLS (NEW!) ---
if choice == "📸 QR Code Tools":
    st.header("QR Code Intelligence")
    tab1, tab2 = st.tabs(["Scan QR", "Generate QR"])
    
    with tab1:
        st.subheader("Upload QR to Scan")
        qr_file = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'], key="qr_scan")
        if qr_file:
            img = Image.open(qr_file)
            st.image(img, width=300)
            if st.button("Decode QR Code"):
                # Convert PIL image to OpenCV format
                img_array = np.array(img.convert('RGB'))
                decoded_objects = decode(img_array)
                
                if decoded_objects:
                    for obj in decoded_objects:
                        data = obj.data.decode("utf-8")
                        st.success(f"**Decoded Content:** {data}")
                        if data.startswith("http"):
                            st.link_button("🌐 Visit Link", data)
                    st.balloons()
                else:
                    st.error("No QR code detected. Try a clearer image.")

    with tab2:
        st.subheader("Create a QR Code")
        qr_text = st.text_input("Enter URL or Text:")
        if st.button("Generate QR"):
            if qr_text:
                import qrcode
                qr = qrcode.make(qr_text)
                buf = io.BytesIO()
                qr.save(buf, format="PNG")
                st.image(buf.getvalue(), width=300)
                st.download_button("📥 Download QR", buf.getvalue(), "my_qr.png", "image/png")
            else:
                st.warning("Please enter text first.")

# --- IMAGE TO PDF ---
elif choice == "🖼️ Image to PDF":
    st.header("Image to PDF Converter")
    uploaded_images = st.file_uploader("Upload Images", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
    if uploaded_images and st.button("Convert to PDF"):
        img_list = [img.read() for img in uploaded_images]
        pdf_bytes = img2pdf.convert(img_list)
        st.download_button("📥 Download PDF", data=pdf_bytes, file_name="converted.pdf")
        st.balloons()

# --- TEXT TO AUDIO ---
elif choice == "🔊 Text to Audio":
    st.header("Text to Audio Generator")
    text_input = st.text_area("Enter text:")
    if st.button("Generate Audio") and text_input:
        tts = gTTS(text=text_input, lang='en')
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        st.audio(audio_buffer)
        st.download_button("📥 Download MP3", audio_buffer.getvalue(), "speech.mp3")

# --- IMAGE SCANNER (OCR) ---
elif choice == "👁️ Image Scanner (OCR)":
    st.header("AI Visual Scanner")
    ocr_file = st.file_uploader("Scan Text from Image", type=['png', 'jpg', 'jpeg'])
    if ocr_file:
        img = Image.open(ocr_file)
        if st.button("Extract Text"):
            text = pytesseract.image_to_string(img)
            st.text_area("Result:", text, height=200)

# --- PDF METADATA ---
elif choice == "📄 PDF Metadata":
    st.header("PDF Metadata Viewer")
    pdf_file = st.file_uploader("Upload PDF", type=['pdf'])
    if pdf_file:
        reader = PdfReader(pdf_file)
        st.metric("Total Pages", len(reader.pages))
        st.write(reader.metadata)