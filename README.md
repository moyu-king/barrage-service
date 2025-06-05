# Barrage service

[barrage-chrome-extension](https://github.com/moyu-king/barrage-chrome-extension) 插件的后端服务。

```bash
# 1. 安装环境
python -m scripts.setup_env

# 2. 初始化sqlite
python -m scripts.execute_sql_file

# 3. 启动服务
uvicorn app.main:app --reload
```