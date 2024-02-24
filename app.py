import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_prompt, image[0]])
    return response.text

def scale_image(uploaded_file, max_size=(800, 800)):
    if uploaded_file is not None:
        # Abre la imagen y redimensiona
        image = Image.open(uploaded_file)
        image.thumbnail(max_size)

        # Convierte la imagen redimensionada a bytes
        with BytesIO() as output_buffer:
            image.save(output_buffer, format="JPEG")  # Puedes ajustar el formato según tus necesidades
            bytes_data = output_buffer.getvalue()

        return bytes_data
    else:
        raise FileNotFoundError("No se ha cargado un archivo")

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = scale_image(uploaded_file)
        
        image_parts = [{
            "mime_type": "image/jpeg",  # Puedes ajustar el tipo MIME según tu necesidad
            "data": bytes_data
        }]
        return image_parts
    else:
        raise FileNotFoundError("No se ha cargado un archivo")

st.set_page_config(page_title="Identificador de plantas", page_icon=":potted_plant:")
st.header("Identificador de plantas")
uploaded_file = st.file_uploader("Selecciona una imagen...", type=["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagen cargada", use_column_width=True)

submit = st.button("Dame información acerca de la planta")

input_prompt = """
                Eres un experto en agricultura y botanica, de las imagenes de las plantas eres capaz de 
                determinar que tipo de planta es, indicando su nombre cientifico y el comun,
                brindas informacion de interes sobre la planta, de manera concisa en no mas de 100 caracteres.

                Ademas eres capaz de establecer si la planta tiene frutos o flores, y de indicar si la planta 
                se encuentra bien de salud o no, indicando si se encuentra enferma y la causa de su enfermedad,
                como por ejemplo si tiene hongos, que tipo de hongos o si se encuentra deshidratada. 
                No debes inventar informacion que no se puede establecer a traves de la imagen de la planta.
                Debes dar consejos de cuidado de la planta basado en su salud.

                Este es el formato que usas para entregar la informacion:

                Nombre cientifico:

                Nombre comun:

                Datos de interes:

                Estado de la planta:

                Consejos:

                """

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data)
    st.header("Esta es la información de tu planta:")
    st.write(response)
