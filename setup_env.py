import os
import sys
import platform
import subprocess


def main():
    # 1. 创建虚拟环境
    venv_name = "venv"
    print(f"🐍 创建虚拟环境: {venv_name}")
    subprocess.run([sys.executable, "-m", "venv", venv_name], check=True)

    # 2. 激活虚拟环境并安装依赖
    requirements_file = "requirements.txt"

    if platform.system() == "Windows":
        # Windows 激活
        activate_script = os.path.join(venv_name, "Scripts", "activate")
        pip_executable = os.path.join(venv_name, "Scripts", "pip")
        activate_cmd = f"cmd /c \"{activate_script} && {pip_executable} install -r {requirements_file}\""
    else:
        # Linux/macOS 激活
        activate_script = os.path.join(venv_name, "bin", "activate")
        pip_executable = os.path.join(venv_name, "bin", "pip")
        activate_cmd = f"source {activate_script} && {pip_executable} install -r {requirements_file}"

    print("🔧 安装依赖...")
    if platform.system() == "Windows":
        subprocess.run(activate_cmd, shell=True, check=True)
    else:
        subprocess.run(
            activate_cmd,
            shell=True,
            executable="/bin/bash",
            check=True
        )

    print("✅ 完成！虚拟环境已创建并安装依赖。")
    print("👉 手动激活命令:")
    if platform.system() == "Windows":
        print(f"    {os.path.join(venv_name, 'Scripts', 'activate')}")
    else:
        print(f"    source {os.path.join(venv_name, 'bin', 'activate')}")


if __name__ == "__main__":
    if not os.path.exists("requirements.txt"):
        print("❌ 错误：当前目录下未找到 requirements.txt 文件")
        sys.exit(1)
    main()
