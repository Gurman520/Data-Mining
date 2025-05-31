# MDX запрос для получения данных
mdx_query_vzr_visit = """
SELECT 
  [Measures].[Число Fact AMB Visits] as count_visit ON COLUMNS,
  [AMB TIME].[Month].[Month].ALLMEMBERS as month * [AMB TIME].[Year].[Year].ALLMEMBERS as year ON ROWS
  FROM (
    select [AMB TIME].[Year].&[2019] : [AMB TIME].[Year].&[2024] on COLUMNS
    from [Med Data]
    )
  where (
    [AMB VISIT].[DEPART].&[Поликлиника (ул.Александрова, д.7)]
  )
"""

mdx_query_det_visit = """
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

