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
});

function handleFiles(files) {
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
