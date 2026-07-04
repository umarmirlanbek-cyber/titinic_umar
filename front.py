import streamlit as st
import requests

api_url = 'http://127.0.0.1:9000/predict'

st.title('Titanic Survival Project')

Pclass = st.selectbox('Класс каюты', [1, 2, 3])
Sex = st.selectbox('Пол', ['male', 'female'])
Age = st.number_input('Возраст', min_value=0, max_value=100, value=30, step=1)
FamilySize = st.number_input('Размер семьи на борту', min_value=0, max_value=15, value=0, step=1)
Fare = st.number_input('Стоимость билета', min_value=0.0, max_value=600.0, value=30.0, step=1.0)
Embarked = st.selectbox('Порт посадки', ['S', 'C', 'Q'])

titanic_data = {
    "Pclass": Pclass,
    "Sex": Sex,
    "Age": Age,
    "FamilySize": FamilySize,
    "Fare": Fare,
    "Embarked": Embarked,
}

if st.button('Предсказать'):
    try:
        answer = requests.post(api_url, json=titanic_data, timeout=10)
        if answer.status_code == 200:
            result = answer.json()
            st.success(f"Результат: {result.get('Answer')}")
        else:
            st.error(f"Ошибка: {answer.status_code}")
    except requests.exceptions.RequestException:
        st.error("Не удалось соединиться к API")