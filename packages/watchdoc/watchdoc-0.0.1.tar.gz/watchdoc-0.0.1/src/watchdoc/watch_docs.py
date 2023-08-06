import os
import sys
import time
import watchdog.events
import watchdog.observers
from docx_manager import to_docx
from pptx_manager import to_pptx
from odt_manager import to_odt
from markdown_manager import to_ipynb, to_md


class Handler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self):
        # Set the patterns for PatternMatchingEventHandler
        watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.ipynb', '*.md'],
                                                             ignore_directories=True, case_sensitive=False)
        print(sys.getdefaultencoding())

    def on_created(self, event):
        print(f"{event.src_path} is created.")
        # Event is created, you can process it now

    def on_modified(self, event):

        if event.src_path.endswith(".ipynb") and os.path.isfile(event.src_path):
            ipynb_file = event.src_path
            # Event is modified, you can process it now
            md_file = ipynb_file.replace(".ipynb", ".md")

            to_md(ipynb_file)
            to_docx(md_file)
            to_pptx(ipynb_file)

        # elif event.src_path.endswith(".md") and os.path.isfile(event.src_path):
        #     # Event is modified, you can process it now
        #     md_file = event.src_path
        #     ipynb_file = md_file.replace(".md", ".ipynb")

        #     to_ipynb(md_file)
        #     to_docx(md_file)
        #     # to_pptx(ipynb_file)

    def on_deleted(self, event):

        if event.src_path.endswith(".ipynb"):
            ipynb_file = event.src_path
            md_file = ipynb_file.replace(".ipynb", ".md")
            docx_file = ipynb_file.replace(".ipynb", ".docx")
            pptx_file = ipynb_file.replace(".ipynb", ".pptx")
            if os.path.exists(md_file) and os.path.isfile(md_file):
                os.remove(md_file)

            if os.path.exists(docx_file) and os.path.isfile(docx_file):
                os.remove(docx_file)

            if os.path.exists(pptx_file) and os.path.isfile(pptx_file):
                os.remove(pptx_file)

        # elif event.src_path.endswith(".md"):
        #     md_file = event.src_path
        #     ipynb_file = md_file.replace(".md", ".ipynb")
        #     docx_file = ipynb_file.replace(".ipynb", ".docx")
        #     pptx_file = ipynb_file.replace(".ipynb", ".pptx")
        #     os.remove(ipynb_file)
        #     os.remove(docx_file)
        #     os.remove(pptx_file)


if __name__ == "__main__":
    src_path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    event_handler = Handler()
    observer = watchdog.observers.Observer()
    observer.schedule(event_handler, path=src_path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
