from typing import Any
import pandas as pd

"""
Функция для создания xlsx файла всего сырья с минимальными, максимальными и средними значениями составляющих.
"""


def report(data: Any, date: str):
    df = pd.DataFrame(data)
    filename = f'report_by_{date}.xlsx'
    df.to_excel(filename, index=False)
    return filename
