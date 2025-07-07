from pdf2docx import Converter as PdfToDocxConverter
from docx2pdf import convert as DocxToPdfConvert
import os

class DocumentConverter:
    def __init__(self, input_file, output_file=None):
        self.input_file = input_file
        self.output_file = output_file
        self.file_ext = os.path.splitext(input_file)[1].lower()

    def convert(self):
        if self.file_ext == '.pdf':
            return self._convert_pdf_to_docx()
        elif self.file_ext in ['.docx', '.doc']:
            return self._convert_docx_to_pdf()
        else:
            raise ValueError(f"Unsupported file type: {self.file_ext}. Please provide a PDF or Word document.")

    def _generate_output_filename(self, new_ext):
        if self.output_file:
            # 如果指定了输出文件，确保扩展名正确
            base, old_ext = os.path.splitext(self.output_file)
            if old_ext.lower() != f".{new_ext}":
                return f"{base}.{new_ext}"
            return self.output_file
        
        # 如果未指定输出文件，则在输入文件同目录下生成
        base_input = os.path.splitext(self.input_file)[0]
        return f"{base_input}.{new_ext}"

    def _convert_pdf_to_docx(self):
        output_docx = self._generate_output_filename('docx')
        print(f"Converting PDF '{self.input_file}' to DOCX: '{output_docx}'")
        cv = PdfToDocxConverter(self.input_file)
        cv.convert(output_docx)
        cv.close()
        print("PDF to DOCX conversion successful.")
        return output_docx

    def _convert_docx_to_pdf(self):
        output_pdf = self._generate_output_filename('pdf')
        print(f"Converting DOCX '{self.input_file}' to PDF: '{output_pdf}'")
        DocxToPdfConvert(self.input_file, output_pdf)
        print("DOCX to PDF conversion successful.")
        return output_pdf
