import pandas as pd
import matplotlib.pyplot as plt


def create_plt(df: pd.DataFrame) -> None:
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