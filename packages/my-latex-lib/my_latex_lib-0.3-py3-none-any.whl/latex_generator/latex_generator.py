def generate_table(data):
    """
    Генерирует LaTeX-код для таблицы на основе входных данных.

    :param data: Список списков, представляющих строки и столбцы таблицы
    :return: Строка с LaTeX-кодом таблицы
    """
    num_columns = len(data[0]) if data else 0
    column_alignment = "|".join(["c"] * num_columns)
    header = "\\begin{tabular}{|" + column_alignment + "|}\n\\hline\n"
    footer = "\\end{tabular}"

    rows = []
    for row in data:
        formatted_row = " & ".join(map(str, row)) + " \\\\ \\hline"
        rows.append(formatted_row)

    table_body = "\n".join(rows)
    table_code = header + table_body + "\n" + footer
    return table_code


def include_image(image_path, caption="", label=""):
    """
    Генерирует LaTeX-код для вставки изображения.

    :param image_path: Путь к файлу изображения
    :param caption: Подпись к изображению
    :param label: Метка для ссылки на изображение

    :return: Строка с LaTeX-кодом для вставки изображения
    """
    image_code = r"""
\begin{figure}[h]
    \centering
    \includegraphics[width=0.8\linewidth]{%s}
    \caption{%s}
    \label{%s}
\end{figure}
    """ % (image_path, caption, label)
    return image_code
