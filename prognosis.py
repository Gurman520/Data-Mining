import pandas as pd
import matplotlib.pyplot as plt

def prognosis_sarimax(df: pd.DataFrame) -> None:
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