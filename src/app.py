from flask import Flask, render_template_string, request, send_file, flash, redirect, url_for
import os
import tempfile
from werkzeug.utils import secure_filename
from document_converter import DocumentConverter
import uuid

app = Flask(__name__)
app.secret_key = 'document-converter-secret-key'

# 配置
UPLOAD_FOLDER = os.path.abspath('uploads')
CONVERTED_FOLDER = os.path.abspath('converted')
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}

# 确保上传和转换目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

print(f"上传目录: {UPLOAD_FOLDER}")
print(f"转换目录: {CONVERTED_FOLDER}")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

# 现代化的HTML模板
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PDF转Word在线转换工具 - 专业版</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #ff7b7b 100%);
            min-height: 100vh;
            position: relative;
            overflow-x: hidden;
        }
        
        /* 动态背景粒子效果 */
        .particles {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1;
        }
        
        .particle {
            position: absolute;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 50%;
            animation: float 6s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(180deg); }
        }
        
        /* 主容器 */
        .main-container {
            position: relative;
            z-index: 2;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .converter-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: 24px;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
            padding: 60px 50px;
            max-width: 600px;
            width: 100%;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.2);
            animation: slideUp 0.8s ease-out;
        }
        
        @keyframes slideUp {
            from { transform: translateY(30px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        /* 标题区域 */
        .header {
            margin-bottom: 50px;
        }
        
        .logo {
            font-size: 4em;
            margin-bottom: 20px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .title {
            color: #2d3748;
            font-size: 2.5em;
            margin-bottom: 15px;
            font-weight: 700;
            letter-spacing: -1px;
        }
        
        .subtitle {
            color: #718096;
            font-size: 1.1em;
            line-height: 1.6;
        }
        
        /* 上传区域 */
        .upload-zone {
            position: relative;
            margin-bottom: 40px;
        }
        
        .drag-drop-area {
            border: 3px dashed #e2e8f0;
            border-radius: 16px;
            padding: 60px 30px;
            background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }
        
        .drag-drop-area:hover,
        .drag-drop-area.dragover {
            border-color: #667eea;
            background: linear-gradient(135deg, #f0f4ff 0%, #e6f3ff 100%);
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.15);
        }
        
        .upload-icon {
            font-size: 4em;
            color: #a0aec0;
            margin-bottom: 20px;
            transition: all 0.3s ease;
        }
        
        .drag-drop-area:hover .upload-icon {
            color: #667eea;
            transform: scale(1.1);
        }
        
        .upload-text {
            font-size: 1.2em;
            color: #4a5568;
            margin-bottom: 15px;
            font-weight: 600;
        }
        
        .upload-hint {
            color: #718096;
            font-size: 0.95em;
        }
        
        .file-input {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            opacity: 0;
            cursor: pointer;
        }
        
        /* 文件信息显示 */
        .file-info {
            display: none;
            background: #f0fff4;
            border: 2px solid #68d391;
            border-radius: 12px;
            padding: 20px;
            margin-top: 20px;
            animation: fadeIn 0.5s ease;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .file-name {
            font-weight: 600;
            color: #22543d;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }
          /* 转换按钮 */
        .button-container {
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
            margin-top: 30px;
            margin-bottom: 20px;
        }
        
        .convert-button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 18px 50px;
            border-radius: 50px;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
            position: relative;
            overflow: hidden;
            min-width: 200px;
        }
        
        .convert-button:hover:not(:disabled) {
            transform: translateY(-3px);
            box-shadow: 0 15px 30px rgba(102, 126, 234, 0.4);
        }
        
        .convert-button:active {
            transform: translateY(-1px);
        }
        
        .convert-button:disabled {
            background: #cbd5e0;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }
          /* 加载动画 */
        .loading {
            display: none;
            margin-top: 30px;
            margin-bottom: 20px;
            text-align: center;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .loading-text {
            color: #4a5568;
            font-weight: 500;
        }
        
        /* 消息提示 */
        .message {
            padding: 20px;
            border-radius: 12px;
            margin: 20px 0;
            font-weight: 500;
            animation: slideDown 0.5s ease;
        }
        
        @keyframes slideDown {
            from { transform: translateY(-10px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        .error {
            background: linear-gradient(135deg, #fed7d7 0%, #feb2b2 100%);
            color: #c53030;
            border-left: 5px solid #f56565;
        }
        
        .success {
            background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
            color: #155724;
            border-left: 5px solid #28a745;
        }
        
        /* 功能特点 */
        .features {
            margin-top: 50px;
            padding-top: 40px;
            border-top: 2px solid #e2e8f0;
        }
        
        .features-title {
            color: #2d3748;
            font-size: 1.3em;
            font-weight: 600;
            margin-bottom: 25px;
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            text-align: left;
        }
        
        .feature-item {
            background: rgba(102, 126, 234, 0.05);
            padding: 20px;
            border-radius: 12px;
            border-left: 4px solid #667eea;
            transition: all 0.3s ease;
        }
        
        .feature-item:hover {
            background: rgba(102, 126, 234, 0.1);
            transform: translateX(5px);
        }
        
        .feature-icon {
            color: #667eea;
            font-size: 1.5em;
            margin-bottom: 10px;
        }
        
        .feature-title {
            color: #2d3748;
            font-weight: 600;
            margin-bottom: 8px;
        }
        
        .feature-desc {
            color: #718096;
            font-size: 0.9em;
            line-height: 1.4;
        }
        
        /* 页脚 */
        .footer {
            margin-top: 40px;
            padding-top: 30px;
            border-top: 1px solid #e2e8f0;
            color: #a0aec0;
            font-size: 0.9em;
        }
        
        /* 响应式设计 */
        @media (max-width: 768px) {
            .converter-card {
                padding: 40px 30px;
                margin: 10px;
            }
            
            .title {
                font-size: 2em;
            }
            
            .logo {
                font-size: 3em;
            }
            
            .drag-drop-area {
                padding: 40px 20px;
            }
            
            .features-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <!-- 动态背景粒子 -->
    <div class="particles" id="particles"></div>
    
    <div class="main-container">
        <div class="converter-card">
            <!-- 头部区域 -->
            <div class="header">
                <div class="logo">
                    <i class="fas fa-file-pdf"></i>
                    <i class="fas fa-arrow-right" style="font-size: 0.6em; margin: 0 20px;"></i>
                    <i class="fas fa-file-word"></i>
                </div>                <h1 class="title">文档转换器</h1>
                <p class="subtitle">支持PDF ↔ Word双向转换，保持原始格式与布局</p>
            </div>
            
            <!-- 消息提示 -->
            {% with messages = get_flashed_messages() %}
                {% if messages %}
                    {% for message in messages %}
                        <div class="message error">
                            <i class="fas fa-exclamation-triangle" style="margin-right: 10px;"></i>
                            {{ message }}
                        </div>
                    {% endfor %}
                {% endif %}
            {% endwith %}
            
            <!-- 上传表单 -->
            <form method="post" enctype="multipart/form-data" id="uploadForm">                <div class="upload-zone">                    <div class="drag-drop-area" id="dropArea">
                        <input type="file" name="file" accept=".pdf,.docx,.doc" required class="file-input" id="fileInput">
                        <div class="upload-content">
                            <div class="upload-icon">
                                <i class="fas fa-cloud-upload-alt"></i>
                            </div>
                            <div class="upload-text">拖拽文档到此处</div>
                            <div class="upload-hint">支持PDF ↔ Word双向转换（最大100MB）</div>
                        </div>
                    </div>
                    
                    <div class="file-info" id="fileInfo">
                        <div class="file-name" id="fileName">
                            <i class="fas fa-file-pdf"></i>
                            <span></span>
                        </div>
                    </div>
                </div>
                
                <div class="button-container">
                    <button type="submit" class="convert-button" id="convertBtn" disabled>
                        <i class="fas fa-magic" style="margin-right: 10px;"></i>
                        开始转换
                    </button>
                </div>
                
                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    <div class="loading-text">正在转换中，请稍候...</div>
                </div>
            </form>
            
            <!-- 功能特点 -->
            <div class="features">
                <h3 class="features-title">为什么选择我们？</h3>
                <div class="features-grid">
                    <div class="feature-item">
                        <div class="feature-icon">
                            <i class="fas fa-shield-alt"></i>
                        </div>
                        <div class="feature-title">隐私保护</div>
                        <div class="feature-desc">本地处理，文件不上传云端，保护您的隐私安全</div>
                    </div>
                    
                    <div class="feature-item">
                        <div class="feature-icon">
                            <i class="fas fa-palette"></i>
                        </div>
                        <div class="feature-title">格式保持</div>
                        <div class="feature-desc">智能识别文字、图片、表格，完美保持原始格式</div>
                    </div>
                    
                    <div class="feature-item">
                        <div class="feature-icon">
                            <i class="fas fa-rocket"></i>
                        </div>
                        <div class="feature-title">高速转换</div>
                        <div class="feature-desc">优化的转换算法，快速处理大文件</div>
                    </div>
                    
                    <div class="feature-item">
                        <div class="feature-icon">
                            <i class="fas fa-download"></i>
                        </div>
                        <div class="feature-title">即时下载</div>
                        <div class="feature-desc">转换完成后立即下载，无需等待</div>
                    </div>
                </div>
            </div>
            
            <!-- 页脚 -->
            <div class="footer">
                <p>© 2024 PDF转Word转换器 - 专业文档转换工具</p>
            </div>
        </div>
    </div>
    
    <script>
        // 粒子背景效果
        function createParticles() {
            const particles = document.getElementById('particles');
            const particleCount = 50;
            
            for (let i = 0; i < particleCount; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.top = Math.random() * 100 + '%';
                particle.style.width = Math.random() * 6 + 2 + 'px';
                particle.style.height = particle.style.width;
                particle.style.animationDelay = Math.random() * 6 + 's';
                particle.style.animationDuration = (Math.random() * 4 + 4) + 's';
                particles.appendChild(particle);
            }
        }
        
        // 文件上传处理
        const dropArea = document.getElementById('dropArea');
        const fileInput = document.getElementById('fileInput');
        const fileInfo = document.getElementById('fileInfo');
        const fileName = document.getElementById('fileName').querySelector('span');
        const convertBtn = document.getElementById('convertBtn');
        const uploadForm = document.getElementById('uploadForm');
        const loading = document.getElementById('loading');
        
        // 防止默认拖拽行为
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropArea.addEventListener(eventName, preventDefaults, false);
            document.body.addEventListener(eventName, preventDefaults, false);
        });
        
        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }
        
        // 拖拽高亮效果
        ['dragenter', 'dragover'].forEach(eventName => {
            dropArea.addEventListener(eventName, highlight, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            dropArea.addEventListener(eventName, unhighlight, false);
        });
        
        function highlight(e) {
            dropArea.classList.add('dragover');
        }
        
        function unhighlight(e) {
            dropArea.classList.remove('dragover');
        }
        
        // 处理文件拖拽
        dropArea.addEventListener('drop', handleDrop, false);
        
        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            handleFiles(files);
        }
        
        // 处理文件选择
        fileInput.addEventListener('change', function(e) {
            handleFiles(this.files);
        });        function handleFiles(files) {
            if (files.length > 0) {
                const file = files[0];
                const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword'];
                const allowedExtensions = ['.pdf', '.docx', '.doc'];
                
                const isValidType = allowedTypes.includes(file.type) || 
                                  allowedExtensions.some(ext => file.name.toLowerCase().endsWith(ext));
                
                if (isValidType) {
                    // 显示转换方向
                    const ext = file.name.toLowerCase().split('.').pop();
                    let conversionInfo = '';
                    if (ext === 'pdf') {
                        conversionInfo = ' → Word文档';
                        fileName.innerHTML = '<i class="fas fa-file-pdf" style="color: #e74c3c;"></i> ' + file.name + conversionInfo;
                    } else if (ext === 'docx' || ext === 'doc') {
                        conversionInfo = ' → PDF文档';
                        fileName.innerHTML = '<i class="fas fa-file-word" style="color: #2980b9;"></i> ' + file.name + conversionInfo;
                    }
                    
                    fileInfo.style.display = 'block';
                    convertBtn.disabled = false;
                } else {
                    alert('请选择PDF或Word文件！');
                    fileInput.value = '';
                }
            }
        }
          // 表单提交处理
        uploadForm.addEventListener('submit', function(e) {
            if (!fileInput.files.length) {
                e.preventDefault();
                alert('请先选择文件！');
                return;
            }
            
            // 显示加载动画
            convertBtn.style.display = 'none';
            loading.style.display = 'block';
            
            // 设置一个定时器来检测下载完成后重置状态
            setTimeout(function() {
                resetForm();
            }, 5000); // 5秒后重置表单
        });
          // 重置表单状态的函数
        function resetForm() {
            // 重置文件输入
            fileInput.value = '';
            
            // 隐藏文件信息
            fileInfo.style.display = 'none';
            
            // 隐藏加载动画
            loading.style.display = 'none';
            
            // 显示转换按钮并禁用
            convertBtn.style.display = 'block';
            convertBtn.disabled = true;
            
            // 重置文件名显示为初始状态
            fileName.innerHTML = '<i class="fas fa-file-pdf"></i><span></span>';
        }
        
        // 监听页面的visibilitychange事件来处理下载完成后的重置
        document.addEventListener('visibilitychange', function() {
            if (!document.hidden && loading.style.display === 'block') {
                setTimeout(resetForm, 1000);
            }
        });
        
        // 监听窗口焦点事件
        window.addEventListener('focus', function() {
            if (loading.style.display === 'block') {
                setTimeout(resetForm, 1000);
            }
        });
        
        // 初始化粒子效果
        document.addEventListener('DOMContentLoaded', function() {
            createParticles();
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/', methods=['POST'])
def upload_file():
    print("=== 收到文件上传请求 ===")
    print(f"Request files: {request.files}")
    print(f"Request form: {request.form}")
    
    if 'file' not in request.files:
        print("错误: 请求中没有文件字段")
        flash('没有选择文件')
        return redirect(url_for('index'))
    
    file = request.files['file']
    print(f"文件对象: {file}")
    print(f"文件名: {file.filename}")
    
    if file.filename == '':
        print("错误: 文件名为空")
        flash('没有选择文件')
        return redirect(url_for('index'))
    
    if not allowed_file(file.filename):
        print(f"错误: 不支持的文件类型: {file.filename}")
        flash('只支持PDF和Word文件')
        return redirect(url_for('index'))
    
    try:
        print("开始处理文件...")
        
        # 生成唯一文件名
        file_id = str(uuid.uuid4())
        print(f"原始文件名: {file.filename}")
        
        # 直接从原始文件名获取扩展名，避免secure_filename移除扩展名
        if '.' not in file.filename:
            print("错误: 原始文件名没有扩展名")
            flash('文件名格式不正确')
            return redirect(url_for('index'))
            
        # 从原始文件名获取扩展名
        file_ext = file.filename.rsplit('.', 1)[1].lower()
        print(f"文件扩展名: {file_ext}")
        
        # 为了安全，使用处理后的文件名，但保持扩展名
        safe_filename = secure_filename(file.filename)
        if '.' not in safe_filename:
            # 如果secure_filename移除了扩展名，我们手动添加回去
            safe_filename = f"document.{file_ext}"
        
        print(f"安全文件名: {safe_filename}")
        filename = safe_filename
        
        # 保存上传的文件
        input_path = os.path.join(UPLOAD_FOLDER, f"{file_id}.{file_ext}")
        print(f"保存文件到: {input_path}")
        
        file.save(input_path)
          # 验证文件是否保存成功
        if not os.path.exists(input_path):
            print("错误: 文件保存失败")
            flash('文件保存失败')
            return redirect(url_for('index'))
        
        file_size = os.path.getsize(input_path)
        print(f"文件保存成功，大小: {file_size} 字节")
        
        if file_size == 0:
            print("错误: 保存的文件为空")
            os.remove(input_path)
            flash('上传的文件为空')
            return redirect(url_for('index'))
        
        # 确定转换类型和输出路径
        conversion_type = get_conversion_type(filename)
        if conversion_type == 'pdf_to_word':
            output_path = os.path.join(CONVERTED_FOLDER, f"{file_id}.docx")
            # 安全获取文件名（不含扩展名）
            base_name = filename.rsplit('.', 1)[0] if '.' in filename else filename
            download_name = f"{base_name}.docx"
            mimetype = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        elif conversion_type == 'word_to_pdf':
            output_path = os.path.join(CONVERTED_FOLDER, f"{file_id}.pdf")
            # 安全获取文件名（不含扩展名）
            base_name = filename.rsplit('.', 1)[0] if '.' in filename else filename
            download_name = f"{base_name}.pdf"
            mimetype = 'application/pdf'
        else:
            print("错误: 无法确定转换类型")
            os.remove(input_path)
            flash('不支持的文件格式')
            return redirect(url_for('index'))
        
        print(f"开始转换: {input_path} -> {output_path}")
        print(f"转换类型: {conversion_type}")
        
        # 执行转换
        converter = DocumentConverter(input_path, output_path)
        output_file = converter.convert()
        
        if not output_file or not os.path.exists(output_file):
            print("错误: 转换失败")
            os.remove(input_path)
            flash('文档转换失败，请检查文件格式')
            return redirect(url_for('index'))
        
        print("转换完成")
        
        # 验证转换结果
        if not os.path.exists(output_file):
            print("错误: 转换失败，输出文件不存在")
            os.remove(input_path)
            flash('转换失败')
            return redirect(url_for('index'))
        
        output_size = os.path.getsize(output_file)
        print(f"转换成功，输出文件大小: {output_size} 字节")
        
        # 删除临时输入文件
        os.remove(input_path)
        
        print(f"发送文件下载: {download_name}")
        
        # 返回文件下载
        return send_file(
            output_file, 
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
        return redirect(url_for('index'))

if __name__ == '__main__':
    print("启动PDF转Word转换服务...")
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV', 'development') == 'development'
    
    if debug_mode:
        print("访问地址: http://localhost:5000")
    else:
        print(f"生产环境启动，端口: {port}")
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
