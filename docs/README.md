# PDF ⇄ Word 双向转换工具

这是一个功能强大的文档转换工具，支持PDF转Word和Word转PDF双向转换，提供图形界面、命令行和Web三种使用方式。

## 功能特点

- ✅ **双向转换**: 支持PDF→Word和Word→PDF双向转换
- ✅ **高质量转换**: 使用先进的转换库，保持原始文档格式
- ✅ **三种界面**: 图形界面、命令行和Web界面，满足不同使用需求
- ✅ **批量转换**: 支持批量处理和脚本自动化
- ✅ **自定义选项**: 可选择页面范围、保持布局等
- ✅ **实时进度**: 实时显示转换进度和状态
- ✅ **现代化Web界面**: 美观的响应式设计，支持拖拽上传

## 系统要求

- Python 3.7 或更高版本
- Windows/macOS/Linux操作系统
- 至少500MB可用磁盘空间

## 安装方法

### 方法1: 自动安装（推荐）
双击运行 `install.bat` 文件，它会自动安装所有必需的依赖包。

### 方法2: 手动安装
```bash
# 安装依赖包
pip install -r requirements.txt
```

## 使用方法

### Web界面版本

```bash
python simple_web.py
```

Web界面功能说明：
1. **访问地址**: 在浏览器中打开 http://localhost:5000
2. **文件上传**: 支持拖拽或点击上传PDF或Word文件
3. **自动识别**: 系统自动识别文件类型并确定转换方向
   - PDF文件 → Word文档(.docx)
   - Word文件(.doc/.docx) → PDF文档
4. **即时下载**: 转换完成后自动下载转换后的文件
5. **现代化界面**: 美观的响应式设计，支持移动设备

### 图形界面版本

```bash
python pdf_to_word_gui.py
```

界面功能说明：
1. **选择文件**: 点击"浏览"按钮选择要转换的文件
2. **选择输出目录**: 选择转换后文件的保存位置
3. **转换选项**: 
   - 保持原始布局：尽可能保持原始排版
   - 提取图片：将文档中的图片正确提取
4. **开始转换**: 点击"开始转换"按钮开始转换过程
5. **查看日志**: 在底部文本框中查看转换进度和结果

### 命令行版本

#### 基本用法
```bash
# 转换单个PDF文件到Word
python pdf_to_word_cli.py input.pdf

# 转换单个Word文件到PDF
python pdf_to_word_cli.py input.docx

# 指定输出文件路径
python pdf_to_word_cli.py input.pdf -o output.docx
python pdf_to_word_cli.py input.docx -o output.pdf

# 转换指定页面范围（仅适用于PDF转Word）
python pdf_to_word_cli.py input.pdf -s 0 -e 5

# 批量转换目录中的所有文档文件
python pdf_to_word_cli.py /path/to/files/folder -b

# 批量转换并指定输出目录
python pdf_to_word_cli.py /path/to/files/folder -o /path/to/output/folder -b
```

#### 命令行参数说明
- `input`: 输入文档文件路径或包含文档文件的目录
- `-o, --output`: 输出文件路径或目录
- `-s, --start`: 开始页码（从0开始，默认为0，仅适用于PDF转Word）
- `-e, --end`: 结束页码（不指定则转换到最后一页，仅适用于PDF转Word）
- `-b, --batch`: 批量转换模式

## 使用示例

### 示例1: 转换单个文件
```bash
python pdf_to_word_cli.py "C:\Documents\报告.pdf"
```
这会在同一目录下生成 `报告.docx` 文件。

### 示例2: 转换文件的前10页
```bash
python pdf_to_word_cli.py "document.pdf" -s 0 -e 9 -o "first_10_pages.docx"
```

### 示例3: 批量转换
```bash
python pdf_to_word_cli.py "C:\PDFs" -o "C:\WordDocs" -b
```
这会将 `C:\PDFs` 目录中的所有PDF文件转换为Word文档，并保存到 `C:\WordDocs` 目录。

## 常见问题

### Q: 转换后的Word文档格式不正确怎么办？
A: 这通常是因为PDF文件的复杂性导致的。建议：
- 尝试转换PDF的不同页面范围
- 对于扫描版PDF，可能需要先进行OCR识别
- 复杂的表格和图表可能需要手动调整

### Q: 转换速度很慢怎么办？
A: 转换速度取决于PDF文件的大小和复杂度：
- 大文件建议分页转换
- 确保有足够的系统内存
- 关闭不必要的程序释放系统资源

### Q: 出现"权限被拒绝"错误？
A: 这可能是因为：
- 输出文件正在被其他程序打开
- 没有写入目标目录的权限
- PDF文件被加密或受保护

### Q: 支持哪些PDF格式？
A: 支持大多数标准PDF格式，包括：
- 文本PDF
- 包含图片的PDF
- 表格和图表
- 注意：扫描版PDF（纯图片）的转换效果可能不理想

## 技术支持

如果遇到问题或有改进建议，请：
1. 检查错误日志中的详细信息
2. 确认PDF文件没有损坏
3. 尝试转换其他PDF文件以排除特定文件问题
4. 更新到最新版本的依赖库

## 依赖库

- `pdf2docx`: PDF到Word转换核心库
- `python-docx`: Word文档处理库
- `PyPDF2`: PDF文件处理库
- `tkinter`: 图形界面库（Python内置）
- `pillow`: 图像处理库

## 许可证

本工具基于开源许可证发布，仅供学习和个人使用。

## 更新日志

- v1.0.0: 初始版本，支持基本的PDF转Word功能
  - 图形界面和命令行两种使用方式
  - 支持批量转换
  - 支持页面范围选择





& python.exe "C:\Users\lin\Desktop\program\pdf-to-word-converter\simple_web.py"