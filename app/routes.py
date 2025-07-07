from flask import Blueprint, render_template, request, send_file, flash, redirect, url_for, current_app
import os
import tempfile
from werkzeug.utils import secure_filename
from .converter import DocumentConverter
import uuid

main = Blueprint('main', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def get_conversion_type(filename):
    """根据文件扩展名确定转换类型"""
    if '.' not in filename:
        return None
    
    parts = filename.rsplit('.', 1)
    if len(parts) < 2:
        return None
        
    ext = parts[1].lower()
    if ext == 'pdf':
        return 'pdf_to_word'
    elif ext in ['docx', 'doc']:
        return 'word_to_pdf'
    return None

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/', methods=['POST'])
def upload_file():
    print("=== 收到文件上传请求 ===")
    print(f"Request files: {request.files}")
    print(f"Request form: {request.form}")
    
    if 'file' not in request.files:
        print("错误: 请求中没有文件字段")
        flash('没有选择文件')
        return redirect(url_for('main.index'))
    
    file = request.files['file']
    print(f"文件对象: {file}")
    print(f"文件名: {file.filename}")
    
    if file.filename == '':
        print("错误: 文件名为空")
        flash('没有选择文件')
        return redirect(url_for('main.index'))
    
    if not allowed_file(file.filename):
        print(f"错误: 不支持的文件类型: {file.filename}")
        flash('只支持PDF和Word文件')
        return redirect(url_for('main.index'))
    
    try:
        # 保存上传文件
        filename = secure_filename(file.filename)
        unique_id = str(uuid.uuid4())
        input_filename = f"{unique_id}_{filename}"
        input_path = os.path.join(current_app.config['UPLOAD_FOLDER'], input_filename)
        
        print(f"保存文件到: {input_path}")
        file.save(input_path)
        print(f"文件保存成功: {os.path.exists(input_path)}")
        
        # 确定转换类型
        conversion_type = get_conversion_type(filename)
        print(f"转换类型: {conversion_type}")
        
        if not conversion_type:
            flash('不支持的文件格式')
            return redirect(url_for('main.index'))
        
        # 生成输出文件名
        name_without_ext = os.path.splitext(filename)[0]
        if conversion_type == 'pdf_to_word':
            output_filename = f"{unique_id}_{name_without_ext}.docx"
            mimetype = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            download_name = f"{name_without_ext}.docx"
        else:  # word_to_pdf
            output_filename = f"{unique_id}_{name_without_ext}.pdf"
            mimetype = 'application/pdf'
            download_name = f"{name_without_ext}.pdf"
        
        output_file = os.path.join(current_app.config['CONVERTED_FOLDER'], output_filename)
        print(f"输出文件路径: {output_file}")
        
        # 执行转换
        print("开始转换...")
        converter = DocumentConverter(input_path, output_file)
        result_file = converter.convert()
        print(f"转换完成: {result_file}")
        
        # 检查输出文件是否存在
        if not os.path.exists(result_file):
            print(f"错误: 输出文件不存在: {result_file}")
            flash('转换失败：输出文件未生成')
            return redirect(url_for('main.index'))
        
        print(f"准备下载文件: {result_file}")
        print(f"文件大小: {os.path.getsize(result_file)} bytes")
        
        # 清理输入文件
        if os.path.exists(input_path):
            os.remove(input_path)
            print(f"已清理输入文件: {input_path}")
        
        # 返回文件供下载
        return send_file(
            result_file, 
            as_attachment=True, 
            download_name=download_name,
            mimetype=mimetype
        )
        
    except Exception as e:
        print(f"转换过程出错: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # 清理文件
        if 'input_path' in locals() and os.path.exists(input_path):
            os.remove(input_path)
        if 'output_file' in locals() and os.path.exists(output_file):
            os.remove(output_file)
            
        flash(f'转换失败: {str(e)}')
        return redirect(url_for('main.index'))
