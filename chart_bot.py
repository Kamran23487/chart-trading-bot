import streamlit as st
import numpy as np
import cv2
from PIL import Image

st.title("📊 Crypto Chart Screenshot Analyzer")
st.write("Upload a TradingView screenshot to get a basic trading signal.")

uploaded_file = st.file_uploader("Upload chart screenshot", type=["jpg", "jpeg", "png"])

def detect_candle_patterns(image, slices=30):
    img = np.array(image)
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    height, width, _ = img.shape

    slice_width = width // slices
    pattern = []

    for i in range(slices):
        x_start = i * slice_width
        x_end = x_start + slice_width
        crop = hsv[:, x_start:x_end]

        green_mask = cv2.inRange(crop, np.array([35, 60, 60]), np.array([85, 255, 255]))
        red_mask1 = cv2.inRange(crop, np.array([0, 70, 50]), np.array([10, 255, 255]))
        red_mask2 = cv2.inRange(crop, np.array([160, 70, 50]), np.array([180, 255, 255]))
        red_mask = red_mask1 | red_mask2

        green_pixels = cv2.countNonZero(green_mask)
        red_pixels = cv2.countNonZero(red_mask)

        if green_pixels > red_pixels * 1.5:
            pattern.append("G")
        elif red_pixels > green_pixels * 1.5:
            pattern.append("R")
        else:
            pattern.append("N")

    return pattern

def analyze_pattern(pattern):
    joined = "".join(pattern)
    if "GGG" in joined:
        return "📈 Strong Bullish Pattern Detected (3 Green Candles)"
    elif "RRR" in joined:
        return "📉 Strong Bearish Pattern Detected (3 Red Candles)"
    else:
        return "⚖️ No Clear Pattern Detected"

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="📈 Uploaded Chart", use_column_width=True)

    pattern = detect_candle_patterns(image)
    pattern_result = analyze_pattern(pattern)

    st.markdown("### 🧠 Pattern Analysis")
    st.write("Detected Candle Sequence:", "".join(pattern))
    st.markdown(f"**{pattern_result}**")
