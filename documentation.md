# 🔆 Solar Rooftop AI Assistant

## Problem Statement
The goal of this project is to create an AI-powered rooftop analysis tool that uses imagery and contextual information to assess the suitability of a roof for solar panel installation. The tool should assist both homeowners and solar professionals by providing:
- Installation feasibility
- Recommended panel size and type
- Estimated cost and ROI
- Observations based on roof characteristics (slope, orientation, shading)

This project is part of an AI internship assessment focused on integrating multiple AI capabilities with practical backend and frontend development.

## Objectives
- Accept rooftop input via image upload or image URL
- Extract meaningful descriptions from images using Vision AI
- Combine image-based analysis with manual inputs (material, area, shading, etc.)
- Generate structured, reliable recommendations using LLMs
- Perform backend calculations for power output, cost, and payback period
- Validate user input using industry-grade standards (Pydantic)
- Present everything via an intuitive Streamlit UI
- Make the system modular, extensible, and deployable to the cloud

## Technical Approach

### 1. Vision AI via Image Captioning
- Used ```ImageCaptionLoader``` from LangChain Community to generate natural language descriptions of rooftop images.
- These captions are treated as structured knowledge passed to the LLM along with other essential information for analysis.
- Supported both file uploads and remote image URLs by saving image bytes to a temporary file. 

### 2. Rooftop and Solar Calculation
Implemented a utility function to estimate:
- Total panel capacity (kW) based on usable area
- Number of panels 
- Total installation cost 
- Annual energy savings
- ROI in years
This gave the assistant a way to produce grounded, calculable outputs before involving the LLM.

### 3. LLM Integration via LangChain
- Integrated Google Gemini via LangChain.
- Prompt included:
  - Image caption
  - All rooftop details from user
  - System instructions
- LLM returns structured suggestions on:
  - Feasibility
  - Panel type & orientation
  - Cost + ROI summary
  - Additional notes on material/shade/slope concerns

### 4. Backend Input Validation with Pydantic
- Defined a RooftopInput model in backend.py using Pydantic.
- Ensured inputs are:
  - Correctly typed
  - Constrained (e.g. slope must be "Flat", "Moderate", "Steep")
  - Secure (validated URL inputs)
- Supports programmatic usage and improves reliability.

### 5. Streamlit Frontend
- Clean interface built using Streamlit.
- Form includes all rooftop fields + image upload or URL.
- Results:
  - Caption (from image)
  - Solar estimation (ROI, cost, panel count)
  - LLM-generated recommendation


## Workflow Summary
1. User uploads a rooftop image or provides a URL
2. Streamlit reads the image as bytes
3. ```backend.py``` creates a temp file and generates a caption
4. Rooftop details are validated using RooftopInput
5. ```utils.py``` computes power, cost, and ROI
6. LLM prompt combines all data to generate a recommendation
7. Final result is rendered on the Streamlit UI