import streamlit as st
from backend import RooftopInput, analyze_rooftop

st.set_page_config(page_title="Solar AI Assistant", layout="centered")
st.title("🔆 Solar Rooftop AI Assistant")
st.markdown("Analyze your rooftop for solar installation using AI.")

# inputs
image_option = st.radio("Choose image input method:", ["Upload Image", "Enter Image URL"])
uploaded_file = None
image_url = None

if image_option == "Upload Image":
  uploaded_file = st.file_uploader("Upload rooftop image", type=["jpg", "jpeg", "png"])
else:
  image_url = st.text_input("Image URL", placeholder="https://example.com/roof.jpg")


with st.form("user_inputs"):
  location = st.text_input("Location", "Pune, India")
  roof_material = st.selectbox("Roof Material", ["Concrete", "Asphalt", "Metal", "Slate", "Tile"])
  slope = st.selectbox("Slope", ["Flat", "Moderate", "Steep"])
  orientation = st.selectbox("Orientation", ["South-facing", "North-facing", "East-facing", "West-facing"])
  shade = st.text_input("Shading Description", "Partial shading from trees")
  square_feet = st.number_input("Approx Roof Area (sq ft)", min_value=50.0, max_value=10000.0, value=500.0)

  submitted = st.form_submit_button("Analyze")

if submitted:
  st.info("Processing... Please wait.")

  input_data = {
    'location':location,
    'roof_material':roof_material,
    'slope':slope,
    'orientation':orientation,
    'shade':shade,
    'square_feet':square_feet,
    'image_url':image_url if image_option == "Enter Image URL" else None
  }

  pydantic_data = RooftopInput(**input_data)

  print(f'\n Input data: {pydantic_data}')
  print(f'\n Type: {type(pydantic_data)}')
  uploaded_image_bytes = uploaded_file.read() if uploaded_file else None

  result = analyze_rooftop(pydantic_data, uploaded_image_bytes)


  if "error" in result:
    st.error("Error: " + result['error'])
  else:
    st.success("Analysis Complete ✅")

    st.subheader("📊 Solar Estimate")
    st.markdown(f"Total Kilowatt: {result['solar_estimate']['total_kw']}\n Estimated cost: {result['solar_estimate']['estimated_cost_inr']} \n Annual generation (kwh): {result['solar_estimate']['annual_generation_kwh']} \n Annual savings: {result['solar_estimate']['annual_generation_kwh']}")
    st.json(result["solar_estimate"])

    st.subheader("📋 Recommendation")
    st.markdown(result["recommendation"].content)