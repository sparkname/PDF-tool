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

if __name__ == '__main__':
    # 创建测试目录
    test_dir = 'converter_test_files'
    os.makedirs(test_dir, exist_ok=True)

    # 示例：PDF 转 Word
    pdf_file = os.path.join(test_dir, 'test_doc.pdf')
    from reportlab.pdfgen import canvas
    c = canvas.Canvas(pdf_file)
    c.drawString(100, 750, "Hello World from PDF for Word conversion!")
    c.save()
    print(f"Created test PDF: {pdf_file}")

    converter_pdf_to_word = DocumentConverter(pdf_file)
    word_output = None
    try:
        word_output = converter_pdf_to_word.convert()
        print(f"SUCCESS: PDF '{pdf_file}' converted to Word: '{word_output}'")
        assert os.path.exists(word_output), "Word output file not found!"
    except Exception as e:
        print(f"ERROR converting PDF to Word: {e}")
    
    print("-"*20)

    # 示例：Word 转 PDF
    word_file = os.path.join(test_dir, 'test_doc.docx')
    from docx import Document
    doc = Document()
    doc.add_paragraph('Hello World from Word for PDF conversion!')
    doc.save(word_file)
    print(f"Created test Word: {word_file}")

    converter_word_to_pdf = DocumentConverter(word_file)
    pdf_output = None
    try:
        pdf_output = converter_word_to_pdf.convert()
        print(f"SUCCESS: Word '{word_file}' converted to PDF: '{pdf_output}'")
        assert os.path.exists(pdf_output), "PDF output file not found!"
    except Exception as e:
        print(f"ERROR converting Word to PDF: {e}")

    # 清理测试文件和目录
    print("-"*20)
    print("Cleaning up test files...")
    files_to_remove = [pdf_file, word_file]
    if word_output and os.path.exists(word_output):
        files_to_remove.append(word_output)
    if pdf_output and os.path.exists(pdf_output):
        files_to_remove.append(pdf_output)
    
    for f_path in files_to_remove:
        if os.path.exists(f_path):
            try:
                os.remove(f_path)
                print(f"Removed: {f_path}")
            except Exception as e:
                print(f"Error removing {f_path}: {e}")
    
    if os.path.exists(test_dir):
        try:
            # 确保目录为空再删除
            if not os.listdir(test_dir):
                 os.rmdir(test_dir)
                 print(f"Removed directory: {test_dir}")
            else:
                print(f"Directory {test_dir} not empty, skipping removal.")
        except Exception as e:
            print(f"Error removing directory {test_dir}: {e}")
    print("Test complete.")
