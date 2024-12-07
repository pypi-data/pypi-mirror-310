from typing import List


def generate_latex_table(values: List[List[str]], file_to_save: str):
    with open(file_to_save, "a") as file:
        file.write("\\begin{center}\n")
        file.write("\\begin{tabular}{" + "c" * len(values[0]) + "}\n")
        for row in values:
            file.write(" & ".join(row) + "\\\\\n")
        file.write("\\end{tabular}\n")
        file.write("\\end{center}\n")
