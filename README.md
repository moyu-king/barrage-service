# Barrage service

[barrage-chrome-extension](https://github.com/moyu-king/barrage-chrome-extension) 插件的后端服务。

```bash
# 1. 安装环境
python -m scripts.setup_env

# 2. 启动开发服务
uvicorn app.main:app --reload

# 3. 初始化sqlite
python -m scripts.execute_sql_file
```
