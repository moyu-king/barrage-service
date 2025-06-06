# Barrage service

[barrage-chrome-extension](https://github.com/moyu-king/barrage-chrome-extension) 插件的后端服务。

#### 1. 安装环境
```bash
python -m scripts.setup_env
```
#### 2. 初始化sqlite
```bash
python -m scripts.execute_sql_file
# or
python -m app.db
```

#### 3.启动服务
```bash
uvicorn app.main:app
```
可能会用到的参数：
| 参数            | 说明                                     | 示例                        |
|----------------|-----------------------------------------|-----------------------------|
| `--host`       | 绑定的主机地址，默认 `127.0.0.1`           | `--host 0.0.0.0`            |
| `--port`       | 绑定的端口，默认 `8000`                    | `--port 8080`               |
| `--workers`    | 启动的工作进程数量，默认 `1`                | `--workers 4`               |
| `--reload`     | 代码变动时自动重启，开发环境推荐使用          | `--reload`                  |
| `--log-level`  | 日志级别，可选：`critical`, `error`, `warning`, `info`, `debug`, `trace` | `--log-level debug`          |
| `--debug`      | 启用调试模式，输出更多错误信息               | `--debug`                   |
| `--timeout-keep-alive` | 连接保持活动超时时间（秒）          | `--timeout-keep-alive 5`    |