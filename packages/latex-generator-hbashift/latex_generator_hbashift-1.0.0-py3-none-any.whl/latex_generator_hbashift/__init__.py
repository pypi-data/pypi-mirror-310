def generate_latex_table(data):
    """
    Генерирует LaTeX-код для таблицы на основе двойного списка.

    :param data: Двойной список с данными для таблицы.
    :return: Строка с валидным кодом LaTeX.
    """
    if not data or not all(isinstance(row, list) for row in data):
        raise ValueError("Input must be a non-empty list of lists.")

    num_columns = len(data[0])
    if any(len(row) != num_columns for row in data):
        raise ValueError("All rows must have the same number of columns.")

    table_latex = "\\begin{tabular}{" + "|".join(["c"] * num_columns) + "}\n\\hline\n"
    for row in data:
        table_latex += " & ".join(map(str, row)) + " \\\\\n\\hline\n"
    table_latex += "\\end{tabular}"
    return table_latex


def generate_latex_image(image_path, caption="Image", label="fig:image"):
    """
    Генерирует LaTeX-код для вставки картинки.

    :param image_path: Путь к картинке.
    :param caption: Подпись к картинке.
    :param label: Метка для картинки.
    :return: Строка с валидным кодом LaTeX.
    """
    return (
        "\\begin{figure}[h!]\n"
        "\\centering\n"
        f"\\includegraphics[width=0.8\\textwidth]{{{image_path}}}\n"
        f"\\caption{{{caption}}}\n"
        f"\\label{{{label}}}\n"
        "\\end{figure}"
    )


