import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind
from util import set_background, hist_visualize, pie_visualize


st.set_page_config(layout='centered', page_title='Dashboard by Lavrov Artem', page_icon="🤕")
st.set_option('deprecation.showPyplotGlobalUse', False)

set_background('imagesandvideo/img_1.png')

st.title("Статистическая проверка гипотез о количестве больничных дней")
st.info("Загрузите ваш файл или используйте данные по умолчанию (М.Тех_Данные_к_ТЗ_DS)")
st.markdown(
    """
    <style>
    textarea {
        font-size: 5rem !important;
    }
    input {
        font-size: 5rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

#Download data
@st.cache_data
def load_data(filename):
    return pd.read_csv(filename, sep = ",")

data_file = st.file_uploader("Загрузите CSV", type="csv")
st.write('Или')
if st.checkbox('Использовать данные по умолчанию'):
    use_default_data = True
else:
    use_default_data = False

if data_file or use_default_data:
    with st.sidebar:
        st.header("Ввод параметров")
        work_days = st.slider("Введите кол-во рабочих дней",0 , 9, 2 , 1)
        age = st.slider("Введите возраст", 18, 65, 35, 1)
        significance_level = st.radio(
            "Выберите уровень значимости",
            [0.01, 0.5],
            horizontal=True,
        )
        st.write('Рабочих дней:', work_days)
        st.write('Возраст:', age)

    work_days = int(work_days)
    age = int(age)

    st.subheader("Выбранные значения:")
    st.write("Количество рабочих дней:", work_days)
    st.write("Возраст:", age)
    if use_default_data:
        data = load_data('stats.csv')
    else:
        data = load_data('stats.csv')
    data.rename(columns={'Количество больничных дней': 'work_days', 'Возраст': 'age', 'Пол': 'gender'}, inplace=True)

    col1, col2 = st.columns(2)
    with col1:
        st.write("* Пример данных:")
        st.table(data.head())
    with col2:
        st.write("* Описание данных:")
        st.dataframe(data.describe())

    st.header(f"Проверка 1 гипотезы: Мужчины пропускают в течение года более {work_days} рабочих дней по болезни значимо чаще женщин.")

    N1, N2 = data.gender.value_counts()
    # Визуализируем pie plot c отношением мужчин к женщинам
    pie_visualize(['Мужчины', 'Жeнщины'], [N1, N2])
    st.write(f"* Количество мужчин: {N1}")
    st.write(f"* Количество женщин: {N2}")


    Man_date = data[(data.gender == 'М')].work_days
    Woman_date = data[(data.gender == 'Ж')].work_days
    Man_date.name = 'Мужчины'
    Woman_date.name = 'Женщны'

    st.subheader("Гистограммы:")
    col1, col2 = st.columns(2)
    with col1:
        marker_color1 = st.color_picker('Выберите цвет', '#FF9500')
        st.write('Текущий цвет', marker_color1)
    with col2:
        marker_color2 = st.color_picker('Выберите цвет', '#00f901')
        st.write('Текущий цвет', marker_color1)

    # Функция вывода гистограммы
    hist_visualize(Man_date, Woman_date, marker_color1, marker_color2, 'полу')

    t_statistic, p_value = ttest_ind(
        data[(data.gender == 'М') & (data.work_days > work_days)].work_days,
        data[(data.gender == 'Ж') & (data.work_days > work_days)].work_days,
        alternative='less'
    )

    st.subheader('Проведем t-тестирование')
    st.write(f'* Гипотеза Н0: ужчины пропускают в течение года более {work_days} рабочих дней по болезни не значимо чаще женщин.')
    st.write(f'* Гипотеза H1: Мужчины пропускают в течение года более {work_days} рабочих дней по болезни значимо чаще женщин.')
    st.write('p-value:', p_value if not np.isnan(p_value) else "недостаточно данных")
    st.write('  statistic:', t_statistic if not np.isnan(t_statistic) else "недостаточно данных")

    st.subheader("Вывод:")

    st.write(f"Принимаем гипотезу H1, так как p_value меньше уровня значимости {significance_level}" if p_value <= significance_level
        else f"Принимаем гипотезу H0, так как p_value больше уровня значимости {significance_level}")

    st.header(f"Проверка 2 гипотезы: Работники старше {age} лет пропускают в течение года более {work_days} \
    рабочих дней (work_days) по болезни значимо чаще своих более молодых коллег.")

    data["age_type"] = ['old' if x > age else 'young' for x in data['age']]

    N3, N4 = data.age_type.value_counts()
    # Визуализируем pie plot
    pie_visualize([f'Aged', 'Young'], [N3, N4])
    st.write(f"* Количество сотрудников старше {age} лет: {N3}")
    st.write(f"* количество сотрудников младше {age} лет: {N4}")


    sns.boxplot(x='age', y='work_days', data=data)
    plt.title('Распределение пропущенных дней по возрасту')
    st.pyplot()

    Aged = data[data.age_type == 'old'].work_days
    Young = data[data.age_type == 'young'].work_days
    Aged.name = 'В возрасте'
    Young.name = 'Молодые'

    st.subheader("Гистограммы:")
    col1, col2 = st.columns(2)
    with col1:
        marker_color1 = st.color_picker('Выберите цвет', '#6BE400')
        st.write('Текущий цвет', marker_color1)
    with col2:
        marker_color2 = st.color_picker('Выберите цвет', '#E20048')
        st.write('Текущий цвет', marker_color1)

    # Функция вывода гистограммы
    hist_visualize(Aged, Young, marker_color1, marker_color2, 'возрасту')
    st.subheader('Проведем t-тестирование')
    st.write(f'* Гипотеза H0: Работники старше {age} лет  пропускают в течение года более {work_days} \
        рабочих дней по болезни не значимо чаще своих более молодых коллег.')
    st.write(f'* Гипотеза H1: Работники старше {age} лет пропускают в течение года более {work_days} \
    рабочих дней по болезни значимо чаще своих более молодых коллег.')

    t_statistic, p_value = ttest_ind(
        Aged[Aged > 2],
        Young[Young > 2],
        alternative='less'
    )

    # Выводим значение статистики и p-значения
    st.write('p-value:', p_value if not np.isnan(p_value) else "недостаточно данных")
    st.write('statistic:', t_statistic if not np.isnan(t_statistic) else "недостаточно данных")

    st.subheader("Вывод:")

    st.write(f"Принимаем гипотезу H1, так как p_value меньше уровня значимости {significance_level}" if p_value <= significance_level
             else f"Принимаем гипотезу H0, так как p_value больше уровня значимости {significance_level}")

st.subheader("Контактная информация")
st.info(
    """
    Автор - [Лавров Артём](https://github.com/artemylavrov) \n\n
    Контактный номер: 8-958-805-14-41\n
    """
)

