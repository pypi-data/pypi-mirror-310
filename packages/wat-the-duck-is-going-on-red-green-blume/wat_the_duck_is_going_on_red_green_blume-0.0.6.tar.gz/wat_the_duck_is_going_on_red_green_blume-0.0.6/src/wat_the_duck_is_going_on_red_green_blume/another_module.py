from func import to_table, generate_table_with_image

def main():
    # task_2_1()
    task_2_2()


def task_2_1():
    with open("out.tex", "w") as f:
        f.write(
            to_table(
                [
                    ["a", "b"],
                    ["d", "c"],
                ]
            )
        )
        
        
def task_2_2():
    out = "out2.tex"
    with open(out, "w") as f:
        latex = generate_table_with_image(
            [
                ["a", "b"],
                ["d", "c"],
            ],
            "image.jpeg",
        )
        print(latex)
        f.write(latex)
        
    from pdflatex import PDFLaTeX

    pdfl = PDFLaTeX.from_texfile(out)
    pdf, log, completed_process = pdfl.create_pdf(keep_pdf_file=True, keep_log_file=True)
    

main()
