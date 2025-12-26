#!/usr/bin/env python3
"""
mcq 自动化本地部署脚本（参考 deploy/部署指导_local.md）

功能概述：
1. 读取/合成 .env（基于 backend/env_example），可从 isw-helper 的 deploy_credentials.json 中填充字段。
2. 执行 deploy/init_deploy_local.sh（构建并启动容器）。
3. 执行 deploy/restart.sh 确保服务加载最新配置。

用法示例：
    python3 deploy/install.py \
        --db-password postgres_pwd \
        --credentials /workspace/isw-helper/output/deploy_credentials.json

可选参数用于覆盖 .env 字段，未提供的字段将保留 env_example 默认值。
"""
from __future__ import annotations

import argparse
import json
import secrets
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, Optional

BASE_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = BASE_DIR / "backend"
DEPLOY_DIR = BASE_DIR / "deploy"
ENV_EXAMPLE = BACKEND_DIR / "env_example"
ENV_FILE = BACKEND_DIR / ".env"
DEFAULT_CREDENTIALS = Path("/workspace/isw-helper/output/deploy_credentials.json")
IAM_PUBLIC_KEY = Path("/workspace/iam/iam/security/public.pem")
MCQ_PUBLIC_KEY = BACKEND_DIR / "security" / "public.pem"
NGINX_CONFIG = DEPLOY_DIR / "nginx" / "mcq_http_nginx.conf"
NGINX_PROJECTS_DIR = Path("/workspace/nginx/projects")


def run(cmd: list[str], cwd: Optional[Path] = None, check: bool = True) -> subprocess.CompletedProcess:
    print(f"[RUN] {' '.join(cmd)} (cwd={cwd or '.'})")
    return subprocess.run(cmd, cwd=cwd, check=check)


def load_credentials(path: Path) -> Dict:
    if not path.exists():
        print(f"⚠️ 未找到凭证文件 {path}，将只使用命令行参数和 env_example 默认值。")
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"⚠️ 读取凭证文件失败：{exc}，将忽略凭证文件。")
        return {}


def generate_key(length: int = 50) -> str:
    # 生成 URL safe 密钥
    return secrets.token_urlsafe(length)


def build_env_map(args: argparse.Namespace, creds: Dict) -> Dict[str, str]:
    # IAM 客户端：直接使用 iam_client_eztview（不做兼容）
    oauth = creds.get("iam_client_eztview") or {}
    influx = creds.get("influxdb", {}) or {}
    postgres = creds.get("postgres", {}) or {}
    # ISW 账号从 credentials 的 system_users.SU_mcq 中获取
    su_mcq = creds.get("system_users", {}).get("SU_mcq", {}) if isinstance(creds.get("system_users"), dict) else {}

    # Influx 优先顺序：命令行 > creds 标准键 > creds 兼容键 > 默认
    influx_url = args.influx_url or "http://127.0.0.1:8086"
    influx_token = args.influx_token or influx.get("INFLUXDB_TOKEN")
    influx_org = args.influx_org or "shhk"

    # 严格从凭证获取 OAuth 信息，若缺失则要求命令行提供
    provider_base = args.iam_base or oauth.get("provider_url")
    client_id = args.iam_client_id or oauth.get("client_id")
    client_secret = args.iam_client_secret or oauth.get("client_secret")
    client_webhook_secret = args.iam_client_webhook_secret or oauth.get("webhook_secret")

    if not provider_base:
        raise RuntimeError("缺少 OAUTH2_PROVIDER_URL_BASE（请通过 --iam-base 或凭证文件提供 provider_url）")
    if not client_id or not client_secret or not client_webhook_secret:
        raise RuntimeError("缺少 OAuth 客户端信息（client_id/client_secret/webhook_secret），请检查 deploy_credentials.json 或命令行参数。")

    updates = {
        # secrets
        "SECRET_KEY": args.secret_key or generate_key(48),
        "JWT_SECRET_KEY": args.jwt_secret_key or generate_key(48),
        # COS 默认关闭，避免误连公网存储
        "USE_COS": "False",
        # db
        "DATABASE_NAME": args.db_name,
        "DATABASE_USER": args.db_user,
        "DATABASE_PASSWORD": args.db_password or postgres.get("password"),
        "DATABASE_HOST": args.db_host,
        "DATABASE_PORT": args.db_port,
        # influx
        "INFLUXDB_URL": influx_url,
        "INFLUXDB_TOKEN": influx_token,
        "INFLUXDB_ORG": influx_org,
        # redis
        "REDIS_HOST": args.redis_host,
        "REDIS_PORT": args.redis_port,
        # oauth
        "OAUTH2_PROVIDER_URL_BASE": provider_base,
        "OAUTH2_CLIENT_ID": client_id,
        "OAUTH2_CLIENT_SECRET": client_secret,
        "OAUTH2_CLIENT_WEBHOOK_SECRET": client_webhook_secret,
        # ISW 适配账号（如凭证中存在则写入）
        "ISW_MQTT_USERNAME": args.isw_mqtt_username or su_mcq.get("username"),
        "ISW_MQTT_PASSWORD": args.isw_mqtt_password or su_mcq.get("password"),
        "ISW_URL": args.isw_url or "http://127.0.0.1:8082/",
        "ISW_API_USER": args.isw_api_user or su_mcq.get("username"),
        "ISW_API_TOKEN": args.isw_api_token or su_mcq.get("password"),
    }
    # 过滤 None，保留非空
    return {k: v for k, v in updates.items() if v is not None}


def write_env(updates: Dict[str, str]) -> None:
    if not ENV_EXAMPLE.exists():
        raise FileNotFoundError(f"缺少 {ENV_EXAMPLE}")
    lines = ENV_EXAMPLE.read_text(encoding="utf-8").splitlines()
    new_lines = []
    for line in lines:
        if not line or line.strip().startswith("#") or "=" not in line:
            new_lines.append(line)
            continue
        key, _, _ = line.partition("=")
        if key in updates:
            new_lines.append(f"{key}={updates[key]}")
        else:
            new_lines.append(line)
    ENV_FILE.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    print(f"✓ 已写入 {ENV_FILE}")


def ensure_exec(path: Path) -> None:
    if path.exists():
        path.chmod(path.stat().st_mode | 0o111)


def run_git_tasks() -> None:
    print("配置 git 并拉取代码...")
    run(["git", "config", "core.filemode", "false"], cwd=BASE_DIR, check=False)
    run(["git", "pull"], cwd=BASE_DIR, check=False)


def copy_public_key() -> None:
    if not IAM_PUBLIC_KEY.exists():
        print(f"⚠️ 未找到 IAM 公钥 {IAM_PUBLIC_KEY}，跳过复制。")
        return
    MCQ_PUBLIC_KEY.parent.mkdir(parents=True, exist_ok=True)
    MCQ_PUBLIC_KEY.write_bytes(IAM_PUBLIC_KEY.read_bytes())
    print(f"✓ 已复制 public.pem 至 {MCQ_PUBLIC_KEY}")


def setup_nginx() -> None:
    if not NGINX_CONFIG.exists():
        print(f"⚠️ 未找到 Nginx 配置 {NGINX_CONFIG}，跳过。")
        return
    dest = NGINX_PROJECTS_DIR / "mcq_http_nginx.conf"
    if dest.exists():
        print(f"Nginx 配置已存在：{dest}，跳过复制。")
    else:
        NGINX_PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(NGINX_CONFIG.read_bytes())
        print(f"✓ 已复制 Nginx 配置至 {dest}")
        run(["docker", "restart", "nginx"], check=False)


def docker_compose_up() -> None:
    print("构建并启动容器...")
    run(["docker-compose", "-p", "mcq", "up", "-d"], cwd=DEPLOY_DIR)


def ensure_cron_tasks() -> None:
    # 若 crontab 中不存在 mcq 相关任务，则添加日志清理任务
    result = subprocess.run(
        ["crontab", "-l"], text=True, capture_output=True, check=False
    )
    existing = result.stdout if result.returncode == 0 else ""
    if "mcq" in existing:
        print("cron 任务已存在，跳过。")
        return
    new_lines = [line for line in existing.splitlines() if line.strip()]
    new_lines.append("0 0 * * * sh /workspace/mcq/deploy/uwsgi/uwsgi_log.sh")
    new_lines.append("0 0 * * * sh /workspace/mcq/deploy/nginx/rm-nginxlog.sh")
    content = "\n".join(new_lines) + "\n"
    subprocess.run(["crontab", "-"], input=content, text=True, check=True)
    print("✓ 已添加 cron 任务。")


def wait_for_container(name: str, timeout: int = 180) -> bool:
    """等待容器启动"""
    print(f"等待容器 {name} 启动...")
    for _ in range(timeout):
        result = subprocess.run(
            ["docker", "ps", "--filter", f"name={name}", "--format", "{{.Status}}"],
            text=True,
            capture_output=True,
            check=False,
        )
        if result.stdout.strip().startswith("Up"):
            print(f"✓ 容器 {name} 已启动")
            return True
        time.sleep(1)
    print(f"⚠️ 容器 {name} 在 {timeout}s 内未就绪")
    return False


def wait_for_migrations(timeout: int = 180) -> bool:
    """等待 Django migrate 完成"""
    print("等待容器内的 Django migrate 完成...")
    for i in range(timeout):
        result = subprocess.run(
            ["docker", "exec", "mcq_web_server", "python", "manage.py", "migrate", "--check"],
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode == 0:
            print("✓ Django migrate 已完成")
            return True
        if i % 3 == 0 and i > 0:
            print(f"  等待中... ({i}/{timeout}s)")
        time.sleep(1)
    print(f"⚠️ Django migrate 在 {timeout}s 内未完成")
    return False


def run_manage(*args: str, check: bool = True, capture: bool = False) -> subprocess.CompletedProcess | str:
    """在容器内执行 Django manage.py 命令"""
    cmd = ["docker", "exec", "mcq_web_server", "python", "manage.py"] + list(args)
    result = subprocess.run(cmd, text=True, capture_output=capture, check=check)
    if capture:
        return (result.stdout or "").strip()
    return result


def sync_user_from_iam(username: str, password: str, iam_base: str) -> None:
    """在容器内使用 Django 管理命令从 IAM 同步用户
    
    Args:
        username: IAM 用户名
        password: IAM 用户密码
        iam_base: IAM 服务基地址
        
    Raises:
        RuntimeError: 如果命令执行失败或同步失败
    """
    # 使用 Django 管理命令同步用户（命令会自动从 IAM 获取数据）
    cmd = [
        "docker", "exec", "mcq_web_server", "python", "manage.py", "sync_user",
        "--username", username,
        "--password", password,
        "--iam-base", iam_base,
    ]
    print(f"→ 执行命令: python manage.py sync_user --username {username} --iam-base {iam_base}")
    result = subprocess.run(
        cmd,
        text=True,
        capture_output=True,
        check=False,
    )
    
    # 输出 stdout
    if result.stdout:
        print(result.stdout.strip())
    
    # 输出 stderr（如果有）
    if result.stderr:
        print("错误输出:", result.stderr.strip(), file=sys.stderr)
    
    # 检查退出码
    if result.returncode != 0:
        error_msg = result.stderr.strip() if result.stderr else "未知错误"
        raise RuntimeError(f"同步用户命令执行失败（退出码: {result.returncode}）: {error_msg}")
    
    # 检查输出中是否有错误标记
    output = (result.stdout or "").strip()
    if "✗" in output or "ERROR" in output or "Exception" in output or "Traceback" in output:
        raise RuntimeError(f"同步用户时发生错误，请查看上面的错误信息")
    
    # 检查是否有成功信息
    if "✓" not in output and "SUCCESS" not in output:
        raise RuntimeError(f"同步用户未返回成功信息，输出: {output}")


def sync_admin_from_iam(creds: Dict, iam_base: Optional[str] = None) -> None:
    """从 IAM 同步 admin 用户到 mcq"""
    # 获取 IAM admin 凭证
    iam_admin = creds.get("iam_admin", {})
    username = iam_admin.get("username", "admin")
    password = iam_admin.get("password")
    
    if not password:
        print("⚠️ 未找到 IAM admin 密码，跳过从 IAM 同步 admin 用户。")
        print("   提示：请确保 deploy_credentials.json 中包含 iam_admin.password")
        return
    
    # 获取 IAM 基地址
    if not iam_base:
        # 尝试从环境变量或凭证中获取
        oauth = creds.get("iam_client_eztview", {})
        iam_base = oauth.get("provider_url")
        if not iam_base:
            print("⚠️ 未找到 IAM 基地址，跳过从 IAM 同步 admin 用户。")
            return
    
    # 确保以 / 结尾
    if not iam_base.endswith("/"):
        iam_base += "/"
    
    try:
        print(f"正在从 IAM 同步 admin 用户 ({username})...")
        # 使用 Django 管理命令，命令会自动从 IAM 获取用户数据并同步
        sync_user_from_iam(username, password, iam_base)
        print("✓ 已从 IAM 同步 admin 用户到 mcq")
    except RuntimeError:
        # RuntimeError 已经包含详细的错误信息，直接抛出
        raise
    except Exception as e:
        raise RuntimeError(f"同步用户时发生错误: {str(e)}")


def perform_local_deploy() -> None:
    print("==== 本地部署（原 init_deploy_local.sh） ====")
    run_git_tasks()
    print("注意：请确保前端打包已完成")
    copy_public_key()
    (BACKEND_DIR / "log").mkdir(parents=True, exist_ok=True)
    setup_nginx()
    docker_compose_up()
    ensure_cron_tasks()
    print("==== 本地部署步骤完成 ====")


def main():
    parser = argparse.ArgumentParser(description="mcq 本地自动化部署")
    parser.add_argument("--credentials", type=Path, default=DEFAULT_CREDENTIALS, help="isw-helper 输出的 deploy_credentials.json 路径")
    parser.add_argument("--db-password", dest="db_password", help="PostgreSQL 密码")
    parser.add_argument("--db-host", default="127.0.0.1")
    parser.add_argument("--db-port", default="55432")
    parser.add_argument("--db-name", default="mcq")
    parser.add_argument("--db-user", default="postgres")
    parser.add_argument("--secret-key", dest="secret_key")
    parser.add_argument("--jwt-secret-key", dest="jwt_secret_key")
    parser.add_argument("--influx-url")
    parser.add_argument("--influx-token")
    parser.add_argument("--influx-org")
    parser.add_argument("--redis-host", default="127.0.0.1")
    parser.add_argument("--redis-port", default="48025")
    parser.add_argument("--iam-base", help="IAM 基础地址，如 https://iam.eztcloud.com/")
    parser.add_argument("--iam-client-id")
    parser.add_argument("--iam-client-secret")
    parser.add_argument("--iam-client-webhook-secret")
    parser.add_argument("--isw-url", dest="isw_url", help="isw_v2 API 基础地址，如 http://<ip>:8082/")
    parser.add_argument("--isw-mqtt-username")
    parser.add_argument("--isw-mqtt-password")
    parser.add_argument("--isw-api-user")
    parser.add_argument("--isw-api-token")
    args = parser.parse_args()

    creds = load_credentials(args.credentials)
    updates = build_env_map(args, creds)
    write_env(updates)

    # 执行原 init_deploy_local.sh 的功能
    perform_local_deploy()

    # 等待容器启动
    if not wait_for_container("mcq_web_server", timeout=240):
        print("⚠️ 容器启动超时，跳过后续步骤")
        return

    # 等待 migrate 完成
    if not wait_for_migrations(timeout=180):
        print("⚠️ migrate 未完成，跳过用户同步")
    else:
        # 从 IAM 同步 admin 用户
        print("\n=== 从 IAM 同步 admin 用户 ===")
        iam_base = args.iam_base or creds.get("iam_client_eztview", {}).get("provider_url")
        try:
            sync_admin_from_iam(creds, iam_base)
        except Exception as e:
            print(f"⚠️ 同步 admin 用户失败: {e}")

    # 重启服务，确保加载最新配置
    restart_script = DEPLOY_DIR / "restart.sh"
    ensure_exec(restart_script)
    run([str(restart_script)], cwd=DEPLOY_DIR)
    print("✅ mcq 部署完成")


if __name__ == "__main__":
    main()

