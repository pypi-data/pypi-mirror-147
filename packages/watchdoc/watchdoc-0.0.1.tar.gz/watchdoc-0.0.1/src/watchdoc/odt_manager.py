import os


def to_odt(md_file):
    odt_file = md_file.replace(".md", "odt")
    cmdlet = f"pandoc -t odt \"{md_file}\" -o \"{odt_file}\""
    os.system(cmdlet)
