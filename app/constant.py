from dotenv import load_dotenv
from enum import Enum
import os

# 项目路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))

# 环境变量
dotenv_path = os.path.join(project_root, '.env')
load_dotenv(dotenv_path)

# 数据库
db_name = os.getenv('DB_NAME')
db_path = os.path.join(project_root, db_name + '.db')

# 枚举
class Platform(Enum):
    TENCENT = 1
    BILIBILI = 2


__all__ = ['project_root', 'db_path', 'Platform']
