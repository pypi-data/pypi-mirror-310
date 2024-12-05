import os

from docx import Document

from utils_base.console.Log import Log
from utils_base.file.File import File

log = Log("DOCXFile")


class DOCXFile(File):
    def read(self):
        return Document(self.path)

    def write(self, document):
        document.save(self.path)

    @staticmethod
    def concat(docx_files, output_path):
        document = Document()
        for docx_file in docx_files:
            log.debug(f"{docx_file.path}")
            document1 = docx_file.read()
            for element in document1.element.body:
                document.element.body.append(element)
        DOCXFile(output_path).write(document)

    @staticmethod
    def concat_dir(dir_path, output_file):
        docx_files = [
            DOCXFile(os.path.join(dir_path, f))
            for f in os.listdir(dir_path)
            if f.endswith(".docx")
        ]
        DOCXFile.concat(docx_files, output_file)
        log.debug(f"Concat {dir_path} to {output_file}")
