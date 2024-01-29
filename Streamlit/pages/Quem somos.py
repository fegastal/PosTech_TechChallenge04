import streamlit as st
import requests
import pandas as pd

st.set_page_config(layout= 'wide')

st.title('QUEM SOMOS')

# Carregar a imagem a partir do caminho do arquivo
caminho_imagem = 'equipe.jpg'
imagem = st.image(caminho_imagem, caption='Fernanda Gastal | Rafael Marangoni | Roger Demori | projeto desenvolvido em https://github.com/fegastal/PosTech_TechChallenge04', use_column_width=True)
