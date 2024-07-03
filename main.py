import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Название
st.title('Data analysis application')
# Описание
st.write('Загрузи свой датафрейм для заполнения пропусков')
# Шаг 1. Загрузка CSV файла
uploaded_file = st.sidebar.file_uploader('Загрузи CSV файл', type='csv')
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write(df.head(5))
else:
    st.stop()
# Шаг 2. Проверка наличия пропусков в файле
missed_values = df.isna().sum()
missed_values = missed_values[missed_values > 0]

if len(missed_values) > 0:
    fig, ax = plt.subplots()
    sns.barplot(x=missed_values.index, y=missed_values.values)
    ax.set_title('Пропуски в столбцах')
    st.pyplot(fig)

# Шаг 3. Заполнить пропуски
    button = st.button('Заполнить пропуски')
    if button:
        df_filled = df[missed_values.index].copy()

        for col in df_filled.columns:
            if df_filled[col].dtype == 'object':
                df_filled[col] = df_filled[col].fillna(df_filled[col].mode()[0])
            else:
                df_filled[col] = df_filled[col].fillna(df_filled[col].mean())

        st.write(df_filled.head(5))

        # Шаг 4. Выгрузить заполненный данными CSV файл
        download_button = st.download_button(
            label='Скачать заполненный датасет в .csv',
            data=df_filled.to_csv(),
            file_name='filled.csv')
else:
    st.write('Нет пропусков в данных!!!')
    st.stop()


