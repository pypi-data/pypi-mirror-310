from typing import List
import itertools as it


def to_table(cells: List[List[str]]) -> str:
    template = """
\documentclass{{article}}

\\begin{{center}}
\\begin{{tabular}}{{c c c}}
{place_holder}    
\end{{tabular}}
\end{{center}}

\end{{document}}
    """
    return template.format(place_holder=" \\\\ \n".join(map(lambda line: " & ".join(line), cells)))


def generate_table_with_image(cells: List[List[str]], imageName: str) -> str:
    template = """
\documentclass{{article}}

\\begin{{center}}
\\begin{{tabular}}{{c c c}}
{place_holder}    
\end{{tabular}}
\end{{center}}


\\usepackage{{graphicx}}
\\graphicspath{{ {{.}} }}
\\includegraphics{{{image_holder}}}


\end{{document}}
    """
    return template.format(
        place_holder=" \\\\ \n".join(map(lambda line: " & ".join(line), cells)),
        image_holder=imageName,
    )