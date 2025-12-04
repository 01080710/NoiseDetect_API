# 📣 噪音監控管理系統(SwaggerAPI)
- 本系統旨在協助企業或環境監測單位進行 噪音狀況即時監控，整合現場 **串流影像來源** 與 **感測器資料**，透過統一的後端 API 服務，提供高效且可擴展的監控解決方案。

---

## 📁 專案結構(Overview)
專案主要組成包含：
- **應用程式主程式碼**（main.py …）
- **環境依賴包**（requirements.txt）
- **環境設定檔**（如 `.env`）
- **容器化設定**（Dockerfile、docker-compose.yml）


---

## 🛠 系統需求(Requirements)
- Docker（建議 28+）
- Docker Compose（建議 v2+）
- Windows/macOS 使用者請安裝 [Docker Desktop](https://docs.docker.com/desktop/setup/install/windows-install/)
- Python 3.11

---

## 🚀 快速建置(Getting Start)

### 1. 下載專案
```bash
git clone <repo-url>
```
```bash
cd <project-folder>
```

### 2. 設定環境變數

專案需使用 `.env` 系統設定參數檔案，所有運行所需的連線資訊與服務設定皆在此檔案中進行管理。

以下為 `.env` 所需的參數格式（*不含實際值*）：

```env

### Backend Setting ###
Host=<backend-host-ip>              # Backend Server IP
Port=1433                           # DB Port（依系統調整）
User=<db-username>                  # 資料庫用戶
Password=<db-password>              # 資料庫密碼
Database=<main-database-name>       # 主要資料庫名稱
Database_His=<history-database-name># 歷史資料庫名稱

### Websocket Setting ###
Push_Time=<push-interval-seconds>   # 推播間隔時間（秒）

### Camera Setting ###
PublicIP=<camera-public-ip>         # 攝影機對外 IP


```


### 3. 啟動方式

本專案支援兩種啟動方式，可依需求選擇：


#### 3-1. Docker運行

- 自動啟動所有服務  
- 適合開發 / 測試 / 部署 
- 可依據 `docker-compose.yml` 自動啟動所有必要服務。

**啟動服務**
```bash
docker-compose up -d --build
```

**關閉服務**

```bash
docker-compose down
```


#### 3-2. 本地運行

若你希望不透過 Docker 進行本地開發，可直接以程式原生方式啟動：

```bash
pip install -r requirements.txt
```
```bash
python main.py
```
> ⚠ 注意：本地運行需要自行準備對應語言環境與套件。



---
## 📚 文件與瀏覽器

若專案包含 API 文件，請參考：

* `/docs`
* `/swagger`
* `/redoc`
* 啟動後的[swaggerAPI網址](http://localhost:8009/docs)

