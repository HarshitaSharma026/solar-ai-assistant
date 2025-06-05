from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import ImageCaptionLoader
from pydantic import BaseModel, Field, HttpUrl
from dotenv import load_dotenv
from typing import Annotated, Optional
import requests, os
import tempfile
from utils import estimate_power_and_roi
load_dotenv()

model = ChatGoogleGenerativeAI(model='gemini-1.5-flash')

# get image caption
def get_image_caption(image_path):
  loader = ImageCaptionLoader(images=image_path)
  docs = loader.load()
  return docs[0].page_content


def fetch_image_bytes(image_url):
  headers = {"User-Agent": "Mozilla/5.0"}
  response = requests.get(image_url, headers=headers, timeout=10)
    # check HTTP status and content type
  if response.status_code == 200 and response.headers.get('Content-Type', '').startswith('image/'):
    return response.content
  else:
    raise ValueError(
      f"Could not get image data for {image_url} "
      f"(status: {response.status_code}, content-type: {response.headers.get('Content-Type')})"
    )

template = """
You're an expert in solar panel installation. A image captioning for a rooftop image of a potential customer is provided to you along with other information about the roof. 
Image Description: "{caption}"
Other roof information:
- Roof Material: {roof_material}
- Slope: {slope}
- Orientation: {orientation}
- Shading: {shade}
- Approx Area: {square_feet} sq ft
Extra info:
- Calculation of estimate power and roi: {solar_stats}
Based on this location '{location}', provide:
1. Installation feasibility
2. Recommended panel type and size (kW)
3. Cost, ROI, and panel count
4. Note on material or slope issues
Provide direct to the point answers in a easy to read format because the customer is going to read it. Do not write unecessary.
"""
prompt = PromptTemplate(
  template=template,
  input_variables=['caption', 'location', 'roof_material', 'slope','orientation', 'shade', 'square_feet']
)

chain = prompt | model 

# ---------- input schema with Pydantic
class RooftopInput(BaseModel):
  location: Annotated[str, Field(..., examples=['Pune, India'])]
  roof_material: Annotated[str, Field(..., examples=['Concrete'])]
  slope: Annotated[str, Field(..., examples=['Moderate'])]
  orientation: Annotated[str, Field(..., examples=['South-facing'])]
  shade: str = Field(..., example="Partial shading from trees")
  square_feet: float = Field(..., gt=0, example=500)
  image_url: Optional[HttpUrl] = None
  

# core function calling streamlit
def analyze_rooftop(data: RooftopInput, upload_image_bytes: Optional[bytes] = None):
  try:
    # print('------ INSIDE ')
    # get caption
    if data.image_url:
      image_data = fetch_image_bytes(data.image_url)
    elif upload_image_bytes:
      # print('----- INSIDE')
      image_data = upload_image_bytes
    else:
      raise ValueError("Either image_url or uploaded_image must be provided.")

    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
      tmp.write(image_data)
      tmp_path = tmp.name

    # print('----- INSIDE')
    print(f'temp file: {tmp_path}')
    caption = ImageCaptionLoader(images=[tmp_path]).load()[0].page_content
    os.remove(tmp_path)

    # --- Estimate Panel Info ---
    solar_stats = estimate_power_and_roi(data.square_feet)
    # print(f'SOLAR STATS: {solar_stats}')
    # print(f'caption: {caption}')

    response = chain.invoke({
      'caption': caption,
      'location': data.location,
      'roof_material': data.roof_material,
      'slope': data.slope,
      'orientation': data.orientation,
      'shade': data.shade,
      'square_feet': data.square_feet,
      'solar_stats': str(solar_stats)
    })
    # print(f'response: {response}')

    return {
      'caption': caption,
      'solar_estimate': solar_stats,
      'recommendation': response
    }
  except Exception as e:
    return {'error': str(e)}
