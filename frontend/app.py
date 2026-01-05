import streamlit as st
from PIL import Image
import time

st.set_page_config(
    page_title="Carbon Sustainability Analyzer",
    page_icon="🌱"
)

st.title("🌱 Carbon Sustainability Analyzer")

st.write("Drag & drop a supplement label image below.")

# Upload box
uploaded_file = st.file_uploader(
    "📤 Drag & drop or click to upload an image",
    type=["jpg", "jpeg", "png"]
)

# Placeholder for sustainability summary
summary_placeholder = st.empty()

if uploaded_file is None:
    # Before upload
    summary_placeholder.info("Carbon sustainability summary is here.")

else:
    # Upload progress bar
    progress_bar = st.progress(0, text="Uploading image...")

    for percent in range(100):
        time.sleep(0.01)  # simulate upload time
        progress_bar.progress(percent + 1)

    progress_bar.empty()

    # Load and show image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    st.success("Image uploaded successfully!")

    st.divider()

    # 🌱 Carbon Sustainability Summary (ONLY after upload)
    summary_placeholder.markdown(
        """
        ### 🌱 Carbon Sustainability Summary

        **Carbon Emission:**  
        ≈ **2.9 g CO₂e per tablet**

        **Carbon Score:**  
        **85 / 100** *(Grade B – Good)*

        **Explanation:**  
        This supplement has a low carbon footprint due to its low-dose
        riboflavin content and plant-based excipients. Emissions mainly
        originate from vitamin B-2 production, while tablet formulation
        and vegetarian composition keep the overall impact low.
        """
    )
