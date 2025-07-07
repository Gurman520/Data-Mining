from sys import path
path.append('C:\\Program Files\\Microsoft.NET\\ADOMD.NET\\150')
path.append('C:\\Program Files\\Microsoft.NET\\ADOMD.NET\\160')
from pyadomd import Pyadomd

conn_str = "Provider=MSOLAP;Data Source=DESKTOP-FQQHIFA\\MSSQLSERVER_2;Initial Catalog=MultidimensionalProject2;Integrated Security=SSPI;"


try:
    conn = Pyadomd(conn_str)
    conn.open()
    print("Подключение успешно!")
    conn.close()
except Exception as e:
    print(f"Ошибка подключения: {e}")