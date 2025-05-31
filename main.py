import pandas as pd
from sys import path
path.append('C:\\Program Files\\Microsoft.NET\\ADOMD.NET\\150')
path.append('C:\\Program Files\\Microsoft.NET\\ADOMD.NET\\160')
from pyadomd import Pyadomd
from statsmodels.tsa.seasonal import seasonal_decompose
import mdx
from prognosis import prognosis_sarimax
from create_plt import create_plt
from trend import analysis_trend_seasonality


# Строка соединения
conn_str = "Provider=MSOLAP;Data Source=DESKTOP-FQQHIFA\\MSSQLSERVER_2;Initial Catalog=MultidimensionalProject2;Integrated Security=SSPI;"

def get_data_from_bd(conn_str, mdx_query) -> pd.DataFrame:
  with Pyadomd(conn_str) as conn:
    with conn.cursor().execute(mdx_query) as cursor:
      df = pd.DataFrame(cursor.fetchall(), columns=[col.name for col in cursor.description])

  df = df.rename(columns={
    "[Measures].[Число Fact AMB Visits]": "Посещения",
    "[AMB TIME].[Month].[Month].[MEMBER_CAPTION]": "month",
    "[AMB TIME].[Year].[Year].[MEMBER_CAPTION]": "year"
  })
  return df


def add_column_date(df: pd.DataFrame) -> pd.DataFrame:
  df['Дата'] = pd.to_datetime(
    df['year'].astype(str) + '-' + df['month'].astype(str) + '-01',  # Добавляем '-01' для дня
    format='%Y-%m-%d'  # Явно указываем формат даты
  )
  return df


det_df = get_data_from_bd(conn_str, mdx.mdx_query_det_visit)
vzr_df = get_data_from_bd(conn_str, mdx.mdx_query_vzr_visit)

det_df = add_column_date(det_df)
vzr_df = add_column_date(vzr_df)

# Сохраним копию данных в csv
# det_df.to_csv('2022-2024_DET.csv', index=False)
# vzr_df.to_csv('2019-2024_VZR.csv', index=False)

# Сортируем данные по дате (на случай, если они не упорядочены)
det_df = det_df.sort_values('Дата')
vzr_df = vzr_df.sort_values('Дата')


# Полный процесс анализа Детской поликлиники
# Строим график
create_plt(det_df)
# Анализ тренда и сезонности
analysis_trend_seasonality(det_df)
# Прогназирование
prognosis_sarimax(det_df)


# Полный процесс анализа Взрослой поликлиники
# Строим график
create_plt(vzr_df)
# Анализ тренда и сезонности
analysis_trend_seasonality(vzr_df)
# Прогназирование
prognosis_sarimax(vzr_df)

