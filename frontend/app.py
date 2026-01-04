import streamlit as st
from PIL import Image

st.title("Image Upload Portal")
st.write("Upload an image to see it displayed below.")

# Create the file uploader widget
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Convert the file to an image Streamlit can handle
    image = Image.open(uploaded_file)
    
    # Display the image
    st.image(image, caption='Uploaded Image', use_container_width=True)
    st.success("Image uploaded successfully!")