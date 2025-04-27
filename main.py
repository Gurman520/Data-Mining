import pandas as pd
from sys import path
path.append('C:\\Program Files\\Microsoft.NET\\ADOMD.NET\\150')
path.append('C:\\Program Files\\Microsoft.NET\\ADOMD.NET\\160')
from pyadomd import Pyadomd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose


conn_str = "Provider=MSOLAP;Data Source=DESKTOP-FQQHIFA\\MSSQLSERVER_2;Initial Catalog=MultidimensionalProject2;Integrated Security=SSPI;"

# MDX запрос для получения данных
mdx_query = """
SELECT 
  [Measures].[Число Fact AMB Visits] as count_visit ON COLUMNS,
  [AMB TIME].[Month].[Month].ALLMEMBERS as month * [AMB TIME].[Year].[Year].ALLMEMBERS as year ON ROWS
  FROM (
    select [AMB TIME].[Year].&[2022] : [AMB TIME].[Year].&[2024] on COLUMNS
    from [Med Data]
    )
  where (
    [AMB VISIT].[DEPART].&[Детская поликлиника]
  )
"""

# Выполнение запроса
with Pyadomd(conn_str) as conn:
    with conn.cursor().execute(mdx_query) as cursor:
        df = pd.DataFrame(cursor.fetchall(), columns=[col.name for col in cursor.description])

df = df.rename(columns={
    "[Measures].[Число Fact AMB Visits]": "Посещения",
    "[AMB TIME].[Month].[Month].[MEMBER_CAPTION]": "month",
    "[AMB TIME].[Year].[Year].[MEMBER_CAPTION]": "year"
})
print(df)
print(list(df.columns))


# Создаем столбец с датой (первое число каждого месяца)
df['Дата'] = pd.to_datetime(
    df['year'].astype(str) + '-' + df['month'].astype(str) + '-01',  # Добавляем '-01' для дня
    format='%Y-%m-%d'  # Явно указываем формат даты
)

# Сортируем данные по дате (на случай, если они не упорядочены)
df = df.sort_values('Дата')

# Строим график
plt.figure(figsize=(12, 6))
plt.plot(df['Дата'], df['Посещения'], marker='o', linestyle='-', label='Посещения')
plt.title('Динамика посещений по месяцам', fontsize=14)
plt.xlabel('Дата', fontsize=12)
plt.ylabel('Количество посещений', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(rotation=45)  # Поворачиваем подписи дат для удобства

# Добавляем подписи точек (опционально)
for i, (date, visits) in enumerate(zip(df['Дата'], df['Посещения'])):
    plt.text(date, visits, str(visits), ha='center', va='bottom')

plt.legend()
plt.tight_layout()  # Улучшает отображение подписей
plt.show()

# Анализ тренда и сезонности
# Убедимся, что все столбцы — числа
df['year'] = pd.to_numeric(df['year'], errors='coerce')
df['month'] = pd.to_numeric(df['month'], errors='coerce')
df['Посещения'] = pd.to_numeric(df['Посещения'], errors='coerce')

# Удалим NaN, если они появились
df = df.dropna()

# Создаем столбец с датой
df['Дата'] = pd.to_datetime(
    df['year'].astype(int).astype(str) + '-' + 
    df['month'].astype(int).astype(str) + '-01',
    format='%Y-%m-%d'
)

# Графики по годам
years = df['year'].unique()
years.sort()

# Настройка стиля
plt.figure(figsize=(12, 6 * len(years)))
sns.set_theme(style="whitegrid")

for i, year in enumerate(years):
    plt.subplot(len(years), 1, i + 1)
    df_year = df[df['year'] == year]
    
    # Рассчитываем среднее за год
    mean_visits = df_year['Посещения'].mean()
    
    # График посещений по месяцам
    plt.plot(
        df_year['month'], 
        df_year['Посещения'], 
        marker='o', 
        linestyle='-', 
        color='royalblue',
        label=f'Посещения ({year})'
    )
    
    # Линия среднего значения
    plt.axhline(
        y=mean_visits, 
        color='red', 
        linestyle='--', 
        label=f'Среднее: {mean_visits:.1f}'
    )
    
    # Заполнение областей выше/ниже среднего
    plt.fill_between(
        df_year['month'], 
        df_year['Посещения'], 
        mean_visits, 
        where=(df_year['Посещения'] > mean_visits),
        color='lightgreen', 
        alpha=0.3,
        label='Выше среднего'
    )
    plt.fill_between(
        df_year['month'], 
        df_year['Посещения'], 
        mean_visits, 
        where=(df_year['Посещения'] < mean_visits),
        color='salmon', 
        alpha=0.3,
        label='Ниже среднего'
    )
    
    # Настройки отображения
    plt.title(f'Динамика посещений за {year} год', fontsize=14)
    plt.xlabel('Месяц', fontsize=12)
    plt.ylabel('Количество посещений', fontsize=12)
    plt.xticks(range(1, 13))
    plt.legend(loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()

# plt.figure(figsize=(12, 6 * len(years)))
# for i, year in enumerate(years):
#     plt.subplot(len(years), 1, i + 1)
#     df_year = df[df['year'] == year]
#     plt.plot(df_year['month'], df_year['Посещения'], marker='o', label=f'{year}')
#     plt.title(f'Посещения в {year} году')
#     plt.xlabel('Месяц')
#     plt.ylabel('Посещения')
#     plt.xticks(range(1, 13))
#     plt.grid(True)
#     plt.legend()

# plt.tight_layout()
# plt.show()







df['Дата_ind'] = pd.to_datetime(df['Дата'])  # Если даты в отдельном столбце
df.set_index('Дата_ind', inplace=True)
df = df.asfreq('MS')  # 'MS' = начало месяца (Monthly Start)

from statsmodels.tsa.statespace.sarimax import SARIMAX

# Предположим, что df уже загружен, но индекс не настроен
# df.index = pd.to_datetime(df.index)  # Преобразуем индекс в даты
df = df.asfreq('MS')  # Указываем месячную частоту

# Проверяем индекс
print(df.index)

# Строим модель (только если данных достаточно)
model = SARIMAX(df['Посещения'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
model_fit = model.fit(disp=False)

# Прогноз на 12 месяцев вперед
forecast = model_fit.get_forecast(steps=12)
forecast_mean = forecast.predicted_mean
confidence_intervals = forecast.conf_int()  # Доверительные интервалы

print(forecast.predicted_mean)  # Выведет прогноз с датами

# Визуализация
plt.figure(figsize=(12, 6))

# 1. Исторические данные
plt.plot(df.index, df['Посещения'], label='Фактические значения', color='blue')

# 2. Прогноз
forecast_index = pd.date_range(df.index[-1], periods=13, freq='MS')[1:]  # Даты прогноза
plt.plot(forecast_index, forecast_mean, label='Прогноз', color='red', linestyle='--')

# 3. Доверительные интервалы (затененная область)
plt.fill_between(forecast_index,
                 confidence_intervals.iloc[:, 0],
                 confidence_intervals.iloc[:, 1],
                 color='pink', alpha=0.3, label='95% доверительный интервал')

# Настройка графика
plt.title('Прогноз посещений с помощью SARIMA', fontsize=14)
plt.xlabel('Дата', fontsize=12)
plt.ylabel('Количество посещений', fontsize=12)
plt.legend(loc='upper left')
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()

plt.show()
