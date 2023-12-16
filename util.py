import pandas as pd
import streamlit as st
import base64
import plotly.graph_objects as go


def set_background(image_file:str)->None:
    """
    Эта функция устанавливает фон приложения Streamlit на изображение, указанное в данном файле изображения.

    Arg:
        image_file (str): путь к файлу изображения, которое будет использоваться в качестве фона.
    Return:
        None
    """

    with open(image_file, "rb") as f:
        img_data = f.read()
    b64_encoded = base64.b64encode(img_data).decode()
    style = f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{b64_encoded});
            background-size: cover;
        }}
        </style>
    """
    st.markdown(style, unsafe_allow_html=True)

def hist_visualize(x:pd.DataFrame, y:pd.DataFrame, marker_color1:str, marker_color2:str, category_title:str):
    '''
    Функция визуализирует лве гистограммы на одной фигуре используя plotly, а также показывает средние значния
    :param x: Первая выборка данных
    :param y: Вторая выборка данных
    :param marker_color1: Значение цвета
    :param marker_color2: Второе значение цвета
    :param category_title: то что будет выведенно в титульнике
    :return: None
    '''
    x_mean = x.mean()
    y_mean = y.mean()
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=x, name=x.name, marker_color=marker_color1))
    fig.add_trace(go.Histogram(x=y, name=y.name, marker_color=marker_color2))
    fig.add_trace(go.Scatter(
        x=(x_mean, x_mean),
        y=((x.size+y.size) / (len(y.unique()) - 3), 0),
        mode='lines',
        name=f'Среднее {x.name}',
        yaxis='y1'
    ))
    fig.add_trace(go.Scatter(
        x=(y_mean, y_mean),
        y=((x.size + y.size) / (len(y.unique()) - 3), 0),
        mode='lines',
        name=f'Среднее {y.name}',
        yaxis='y1'
    ))
    fig.update_layout(
        autosize=False,
        width=800,
        height=800,
        barmode='overlay',

        title_text=f'Распределение пропущенных дней по {category_title}',  # title of plot
        xaxis_title_text='Количество больничных дней',  # xaxis label
        yaxis_title_text='Кол-во сотрудников'
    )
    # Reduce opacity to see both histograms
    fig.update_traces(opacity=0.75)
    st.plotly_chart(fig)

def pie_visualize(labels:list[str], values:list[int]):
    '''
    Функция выводит Pie plot
    :param labels: Названия классов
    :param values: Кол-во классов
    :return: None
    '''

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_layout(
        autosize=False,
        width=600,
        height=600,
        title_text='Отношение классов'
    )
    st.plotly_chart(fig)