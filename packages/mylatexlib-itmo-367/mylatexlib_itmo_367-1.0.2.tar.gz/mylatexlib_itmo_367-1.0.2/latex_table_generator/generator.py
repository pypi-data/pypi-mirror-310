import subprocess
import os


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

def compile_latex(tex_file_path, output_dir="."):
    """
    Компилирует LaTeX-файл в PDF с помощью pdflatex.
    
    :param tex_file_path: Путь к .tex файлу
    :param output_dir: Директория для вывода PDF
    """
    # Получаем имя файла без расширения
    file_name = os.path.splitext(os.path.basename(tex_file_path))[0]
    output_pdf_path = os.path.join(output_dir, f"{file_name}.pdf")
    
    # Запуск pdflatex
    try:
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-output-directory", output_dir, tex_file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.returncode != 0:
            print("Ошибка компиляции LaTeX:")
            print(result.stderr)
        else:
            print(f"Компиляция LaTeX успешно завершена, {output_pdf_path}")
    except FileNotFoundError:
        print("Ошибка: pdflatex не найден. Убедитесь, что он установлен и добавлен в PATH.")
        return None
