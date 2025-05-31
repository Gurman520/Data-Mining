import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def analysis_trend_seasonality(df: pd.DataFrame) -> None:
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