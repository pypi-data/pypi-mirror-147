#!/usr/bin/env python


from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
    AdaptiveETA, FileTransferSpeed, FormatLabel, Percentage, \
    ProgressBar, ReverseBar, RotatingMarker, \
    SimpleProgress, Timer, UnknownLength
import os
import sys
import json
import time
import uuid
from folder_manager import notebook_file_paths
from docx_manager import to_docx, add_header, add_footer
from pptx_manager import to_pptx
from markdown_manager import to_md, to_ipynb

if __name__ == "__main__":

    src_path = input(
        "Please paste here the absolute path of the root folder: "
    )

    if src_path == "":
        src = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()

    base = input(
        "What is the source file extension? .ipynb | .md | .docx | .pptx | .odt : "
    )

    logo_file = input(
        "Please enter the URL for logo image (Acceptable formats are PNG and JPG): "
    )

    source_file_list = notebook_file_paths(src_path, base)

    pBarMax = len(source_file_list)
    widgets = [Percentage(),
               ' ', Bar(),
               ' ', ETA(),
               ' ', AdaptiveETA()]
    pBar = ProgressBar(widgets=widgets, maxval=pBarMax)

    pBar.start()
    pBarCount = 0
    for source_file in source_file_list:

        if base in ".ipynb":
            md_file = source_file.replace(".ipynb", ".md")

            to_md(source_file)
            to_docx(md_file)
            to_pptx(source_file, logo_file)

        elif base in ".md":
            ipynb_file = source_file.replace(".md", ".ipynb")

            to_ipynb(source_file)
            to_docx(source_file)
            to_pptx(ipynb_file, logo_file)

        pBarCount += 1
        pBar.update(pBarCount)

    pBar.finish()
