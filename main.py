"""
PDF转Word转换器 - 主应用入口
支持PDF到Word和Word到PDF的双向转换
"""
import os
from app import create_app
from app.config import config

def main():
    # 获取运行环境
    env = os.environ.get('FLASK_ENV', 'development')
    
    # 创建应用实例
    app = create_app(config.get(env, config['default']))
    
    # 运行配置
    port = int(os.environ.get('PORT', 5000))
    debug_mode = env == 'development'
    
    print("启动PDF转Word转换服务...")
    if debug_mode:
        print("访问地址: http://localhost:5000")
    else:
        print(f"生产环境启动，端口: {port}")
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port)

if __name__ == '__main__':
    main()
