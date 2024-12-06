def generate_latex_table(data):
    """
    Функция для генерации таблицы в формате LaTeX.
    
    :param data: двойной список с данными таблицы
    :return: строка с таблицей в формате LaTeX
    """
    if not data or not all(isinstance(row, list) for row in data):
        raise ValueError("Input must be a non-empty list of lists.")

    # Определяем количество колонок
    column_count = max(len(row) for row in data)
    column_format = "|".join(["c"] * column_count)  # Центрированные колонки с вертикальными линиями
    
    # Генерируем LaTeX-код
    latex_code = [
        "\\documentclass{article}",
        "\\usepackage{graphicx}",
        "\\usepackage{booktabs}",
        "\\begin{document}",
        "\\begin{table}[ht]",
        "\\centering",
        "\\begin{tabular}{" + "|" + column_format + "|}",
        "\\hline"
    ]
    
    for row in data:
        row_content = " & ".join(map(str, row))  # Преобразуем каждую строку в формат LaTeX
        latex_code.append(row_content + " \\\\ \\hline")  # Добавляем разделитель строк
    
    latex_code.append("\\end{tabular}")
    latex_code.append("\\caption{Sample Table}")
    latex_code.append("\\label{tab:sample}")
    latex_code.append("\\end{table}")
    latex_code.append("\\end{document}")
    
    return "\n".join(latex_code)

def generate_latex_image(image_path, caption="Sample Image", label="fig:sample"):
    """
    Функция для генерации LaTeX-кода вставки изображения.
    
    :param image_path: Путь к изображению
    :param caption: Подпись к изображению
    :param label: Метка для ссылки на изображение
    :return: строка с LaTeX-кодом вставки изображения
    """
    latex_code = [
        "\\documentclass{article}",
        "\\usepackage{graphicx}",
        "\\usepackage{booktabs}",
        "\\begin{document}",
        "\\begin{figure}[ht]",
        "\\centering",
        f"\\includegraphics[width=0.8\\textwidth]{{{image_path}}}",
        f"\\caption{{{caption}}}",
        f"\\label{{{label}}}",
        "\\end{figure}",
        "\\end{document}"
    ]
    return "\n".join(latex_code)

