# Barrage service

[barrage-chrome-extension](https://github.com/moyu-king/barrage-chrome-extension) 插件的后端服务。

#### 1. 安装环境
```bash
python -m scripts.setup_env
```
#### 2. 初始化sqlite
```bash
python -m scripts.execute_sql_file
```
或者
```bash
python -m app.db
```

#### 3.启动服务
```bash
uvicorn app.main:app --reload
```