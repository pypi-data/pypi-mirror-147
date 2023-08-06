import os


def to_md(ipynb_file: str) -> str:
    cmdlet = f"jupyter nbconvert --to markdown \"{ipynb_file}\""
    os.system(cmdlet)
    return ipynb_file.replace(".ipynb", ".md")


def to_ipynb(md_file: str) -> str:
    ipynb_file = md_file.replace(".md", ".ipynb")
    cmdlet = f"pandoc \"{md_file}\" -o \"{ipynb_file}\""
    os.system(cmdlet)
    return ipynb_file
