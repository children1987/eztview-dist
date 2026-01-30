# mcq local development helper script
# 用途：
# - 第一次运行：自动完成本地环境初始化（等价于原 setup_local_dev.ps1）
# - 之后运行：直接启动 Django 开发服务器（等价于原 run_local_dev.ps1）
#
# 使用方式（从项目根目录）：
#   cd .\backend
#   .\local_dev.ps1

Write-Host "=== mcq Local Development Helper ===" -ForegroundColor Green

# 是否只做初始化或只启动，可以通过参数控制：
#   .\local_dev.ps1 setup   只做环境初始化
#   .\local_dev.ps1 run     只启动服务（环境必须已就绪）
$mode = $null
if ($args.Length -gt 0) {
    $mode = $args[0].ToLower()
}

function Invoke-Setup {
    Write-Host "`n[SETUP] Setting up local development environment..." -ForegroundColor Green

    # 1. Check uv
    Write-Host "`n[1/6] Checking uv..." -ForegroundColor Yellow
    try {
        $uvVersion = uv --version
        Write-Host "OK uv installed: $uvVersion" -ForegroundColor Green
    } catch {
        Write-Host "ERROR: uv not installed, please install from: https://github.com/astral-sh/uv" -ForegroundColor Red
        exit 1
    }

    # 2. Check Python 3.11
    Write-Host "`n[2/6] Checking Python 3.11..." -ForegroundColor Yellow
    try {
        $pythonVersion = python --version
        if ($pythonVersion -match "3\.11") {
            Write-Host "OK Python 3.11 installed: $pythonVersion" -ForegroundColor Green
        } else {
            Write-Host "WARNING: Current Python version: $pythonVersion, Python 3.11 recommended" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "ERROR: Python not installed or not in PATH" -ForegroundColor Red
        exit 1
    }

    # 3. Create virtual environment
    Write-Host "`n[3/6] Creating virtual environment..." -ForegroundColor Yellow
    $venvPath = ".venv"
    if (Test-Path $venvPath) {
        Write-Host "WARNING: Virtual environment already exists, skipping creation" -ForegroundColor Yellow
    } else {
        uv venv --python 3.11
        Write-Host "OK Virtual environment created" -ForegroundColor Green
    }

    # 4. Install dependencies
    Write-Host "`n[4/6] Installing dependencies..." -ForegroundColor Yellow
    Write-Host "(This may take a few minutes)" -ForegroundColor Gray

    $requirementsContent = @"
django==4.2.20
djangorestframework==3.15.2
django-redis==6.0.0
django-environ==0.4.5
django-extensions==3.1.5
django-cors-headers==3.10.1
cryptography==40.0.2
argon2-cffi==23.1.0
celery==5.2.7
openpyxl==3.0.10
django-filter==21.1
djangorestframework-simplejwt==5.3.1
sphinx==2.0.1
psycopg2-binary==2.9.9
django-coverage-plugin==1.6.0
factory-boy==2.12.0
cos-python-sdk-v5==1.9.36
qcloud-python-sts==3.0.5
xlrd==1.2.0
pycryptodome==3.20.0
django-mptt==0.14.0
pyyaml==6.0.1
django-requestlogs==0.7.1
drf-dynamic-fields==0.4.0
daphne==4.0.0
paho-mqtt==1.5.1
django-celery-beat==2.5.0
drf-spectacular==0.27.0
chinesecalendar==1.8.0
requests==2.32.3
django-utils-six==2.0
influxdb-client==1.40.0
PyExecJS==1.5.1
tencentcloud-sdk-python==3.0.1015
werkzeug==2.2.3
twisted==22.10.0
pillow==10.1.0
psycopg2==2.9.7
django-postgres-extra==2.0.8
watchdog==3.0.0
taospy==2.7.21
concurrent-log-handler==0.9.26
taos-ws-py==0.3.8
"@

    $requirementsFile = "requirements_temp.txt"
    $requirementsContent | Out-File -FilePath $requirementsFile -Encoding utf8

    uv pip install -r $requirementsFile
    Remove-Item $requirementsFile -ErrorAction SilentlyContinue

    if ($LASTEXITCODE -eq 0) {
        Write-Host "OK Dependencies installed successfully" -ForegroundColor Green
    } else {
        Write-Host "ERROR: Dependency installation failed, please check error messages" -ForegroundColor Red
        Write-Host "You can try manual installation: uv pip install -r requirements_temp.txt" -ForegroundColor Yellow
        exit 1
    }

    # 5. Create .env file
    Write-Host "`n[5/6] Configuring environment variables..." -ForegroundColor Yellow
    if (Test-Path ".env") {
        Write-Host "WARNING: .env file already exists, skipping creation" -ForegroundColor Yellow
        Write-Host "To reconfigure, delete .env and run this script again" -ForegroundColor Gray
    } else {
        Copy-Item "env_example" ".env"
        Write-Host "OK .env file created (based on env_example)" -ForegroundColor Green
        Write-Host "WARNING: Please edit .env file to configure database, Redis, etc." -ForegroundColor Yellow
    }

    # 6. Next steps
    Write-Host "`n[6/6] Setup complete!" -ForegroundColor Green
}

function Invoke-Run {
    Write-Host "`n[RUN] Starting mcq local development server..." -ForegroundColor Green

    # 检查虚拟环境和 .env
    if (-not (Test-Path ".venv")) {
        Write-Host "✗ 虚拟环境不存在，请先完成初始化（运行: .\local_dev.ps1 setup）" -ForegroundColor Red
        exit 1
    }
    if (-not (Test-Path ".env")) {
        Write-Host "✗ .env 文件不存在，请先完成初始化（运行: .\local_dev.ps1 setup）" -ForegroundColor Red
        exit 1
    }

    # 激活虚拟环境
    Write-Host "`n激活虚拟环境..." -ForegroundColor Yellow
    & ".venv\Scripts\Activate.ps1"

    # 运行迁移（允许失败）
    Write-Host "`n运行数据库迁移..." -ForegroundColor Yellow
    python manage.py migrate --noinput
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠ 数据库迁移失败，但继续启动服务器..." -ForegroundColor Yellow
        Write-Host "  请检查 .env 中的数据库配置" -ForegroundColor Gray
    }

    # 启动服务器
    Write-Host "`n启动 Django 开发服务器..." -ForegroundColor Yellow
    Write-Host "访问地址: http://localhost:8000" -ForegroundColor Cyan
    Write-Host "API Schema: http://localhost:8000/api/schema/" -ForegroundColor Cyan
    Write-Host "`n按 Ctrl+C 停止服务器`n" -ForegroundColor Gray

    python manage.py runserver
}

if ($mode -eq "setup") {
    Invoke-Setup
    Write-Host "`nSetup finished. You can now run: .\local_dev.ps1 run" -ForegroundColor Cyan
} elseif ($mode -eq "run") {
    Invoke-Run
} else {
    # 智能模式：如果还没 .venv 或 .env，就先做 setup，再 run
    $needSetup = -not (Test-Path ".venv") -or -not (Test-Path ".env")
    if ($needSetup) {
        Write-Host "`n[INFO] Environment not fully initialized, running setup first..." -ForegroundColor Yellow
        Invoke-Setup
    } else {
        Write-Host "`n[INFO] Environment detected, skipping setup." -ForegroundColor Green
    }
    Invoke-Run
}


