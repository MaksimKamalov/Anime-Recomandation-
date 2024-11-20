import requests
from st_on_hover_tabs import on_hover_tabs
import streamlit as st
import pandas as pd


def getFilms(films: list):
    for i in range(0, len(films)):
        st.write(str(i + 1) + " " + films[i])


def main():
    try:
        st.set_page_config(layout="wide")

        st.header("Рекомендации Аниме фильмов")
        st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)

        with st.sidebar:
            tabs = on_hover_tabs(tabName=['Топ 10 Аниме', 'Похожие по жанрам', 'Похожие аниме'],
                                 iconName=['dashboard', 'money', 'economy'], default_choice=0)

        if tabs == 'Топ 10 Аниме':
            st.title("Топ 10 Аниме")
            type_options = ['All', 'Movie', 'TV', 'OVA', 'Special', 'Music', 'ONA']
            selected_type = st.selectbox("Выберите тип аниме для фильтрации", type_options)
            API_URL = "http://127.0.0.1:5050/anime/"
            params = {"type": selected_type} if selected_type != "All" else {}
            response = requests.get(API_URL, params=params)

            if response.status_code == 200:
                anime_data = response.json()
                if anime_data:
                    df_anime = pd.DataFrame(anime_data)
                    st.dataframe(df_anime)
                else:
                    st.write("Нет данных для выбранного типа.")
            else:
                st.write("Ошибка при получении данных от API.")


        elif tabs == 'Похожие по жанрам':
            st.title("Похожие по жанрам")
            input_text = st.text_input("Введите жанр")

            if st.button("Искать", key="white"):
                if input_text.strip() != "":
                    response = requests.post("http://127.0.0.1:5050/genre", json={
                        "genre": input_text
                    })
                    result = response.json()
                    df_anime = pd.DataFrame(result)
                    if df_anime.empty:
                        st.write("Нет данных для выбранного жанра.")
                    else: 
                        st.dataframe(df_anime)
                else: 
                    st.write("Введите жанр!")
                    
            
        elif tabs == 'Похожие аниме':
            st.title("Похожие аниме")
            input_text = st.text_input("Введите название фильма")

            if st.button("Искать"):
                if input_text.strip() != "":
                    response = requests.post("http://127.0.0.1:5050/content", json={
                        "name": input_text
                    })
                    result = response.json()
                    df_anime = pd.DataFrame(result)
                    if df_anime.empty:
                        st.write("Нет данных для выбранного аниме.")
                    else: 
                        st.dataframe(df_anime)
                else: 
                    st.write("Введите название аниме!")    
    except Exception as e:
        print("Не правильный ввод!:", e)


if __name__ == "__main__":
    main()
