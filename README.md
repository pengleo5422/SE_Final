# SE_Final 議題提案與討論平台

本專案為 2024 Fall Software Engineering 期末專案，使用 Flask 建置一套議題提案、討論、投票與管理審核平台。系統提供一般使用者發起議題、瀏覽議題、留言討論、收藏、投票與通知查看等功能；管理者則可審核議題、審核留言、管理議題分類與維護公告。

---

## 專案簡介

本系統以「議題提案與公共討論」為核心，模擬一個可讓使用者提出議題、參與討論、表達支持或反對意見的平台。

系統分為使用者端與管理者端：

- 使用者可註冊、登入、編輯個人資料、提出議題、查看議題、留言、收藏、投票與接收通知。
- 管理者可進行議題審核、留言審核、議題分類管理、使用者管理與維護公告管理。

本專案重點在於實作 Flask Web Application 架構、ORM 資料庫模型設計、使用者身份驗證、角色權限區分、議題審核流程與前後端頁面整合。

---

## 技術棧

- Python
- Flask
- Flask-Login
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-WTF
- WTForms
- SQLAlchemy
- PyMySQL
- MySQL
- Jinja2
- HTML / CSS / JavaScript
- Pytest

---

## 核心功能

### 使用者端

- 使用者註冊與登入
- 修改個人資料
- 變更密碼
- 查看議題列表
- 查看議題詳細內容
- 新增議題草稿
- 完成議題提案
- 收藏議題
- 議題投票
- 議題留言
- 查看個人頁面
- 查看通知
- 查看操作紀錄或歷史紀錄

### 管理者端

- 管理者登入
- 管理者首頁
- 議題討論與監控
- 審核議題
- 審核留言
- 管理議題分類
- 管理維護公告
- 會員資料管理

---

## 系統角色

### 一般使用者

一般使用者主要負責參與平台互動，可提出議題、瀏覽議題、留言、投票、收藏，以及查看通知與個人資料。

### 管理者

管理者負責平台內容管理與審核流程，包括議題審核、留言審核、分類維護、公告管理與會員管理。

---

## 系統架構

本專案採用 Flask application package 架構，將主要功能拆分為 models、routes、forms、templates 與 static。

- `models`：定義資料庫模型與資料表關聯
- `routes`：處理不同功能模組的路由與後端邏輯
- `forms`：定義表單驗證邏輯
- `templates`：存放 Jinja2 HTML 頁面
- `static`：存放 CSS、圖片與前端靜態資源
- `migrations`：管理資料庫 migration
- `tests`：存放測試程式

---

## 資料模型

主要資料表包含：

- `User`：使用者資料
- `Issue`：議題資料
- `Category`：議題分類
- `Comment`：留言資料
- `Vote`：投票資料
- `Favorite`：收藏資料
- `Notification`：通知資料

### 資料關係

- 一位使用者可以提出多個議題
- 一個議題可以有多則留言
- 一個議題可以有多筆投票紀錄
- 一個議題可以被多位使用者收藏
- 一位使用者可以收到多則通知
- 一個議題會對應到一個議題分類

---

## 專案結構

```text
SE_Final
├── app
│   ├── forms
│   │   └── registration_form.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── category.py
│   │   ├── comment.py
│   │   ├── favorite.py
│   │   ├── issue.py
│   │   ├── notification.py
│   │   ├── user.py
│   │   └── vote.py
│   ├── routes
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── hist.py
│   │   ├── issue.py
│   │   ├── login.py
│   │   ├── main.py
│   │   ├── member.py
│   │   ├── notification.py
│   │   ├── propose.py
│   │   ├── register.py
│   │   └── routes.py
│   ├── static
│   ├── templates
│   │   ├── add_issue.html
│   │   ├── editPWD.html
│   │   ├── finish_issue.html
│   │   ├── history.html
│   │   ├── index.html
│   │   ├── issue.html
│   │   ├── issueDetail.html
│   │   ├── login.html
│   │   ├── maintenance_notice.html
│   │   ├── member.html
│   │   ├── member_auth.html
│   │   ├── member_homepage.html
│   │   ├── member_manage.html
│   │   ├── memberedit.html
│   │   ├── notifications.html
│   │   ├── propose_category_manage.html
│   │   ├── propose_manage.html
│   │   ├── register.html
│   │   ├── review_comment.html
│   │   ├── review_issue.html
│   │   ├── usrNotification.html
│   │   └── usrProfile.html
│   └── __init__.py
├── instance
├── migrations
├── static
├── tests
│   ├── conftest.py
│   └── test_routes.py
├── app.py
├── config.py
├── requirements.txt
└── README.md
```

---

## 環境建置

### 1. Clone 專案

```bash
git clone https://github.com/pengleo5422/SE_Final.git
cd SE_Final
```

### 2. 建立虛擬環境

```bash
python -m venv venv
```

Windows：

```bash
venv\Scripts\activate
```

macOS / Linux：

```bash
source venv/bin/activate
```

### 3. 安裝套件

```bash
pip install -r requirements.txt
```

如缺少套件，可額外安裝：

```bash
pip install Flask-WTF flask-login pytest
```

---

## 環境變數設定

建議使用 `.env` 管理敏感資訊，例如資料庫連線字串與 Flask Secret Key。

可建立 `.env`：

```env
SECRET_KEY=your_secret_key
DATABASE_URL=mysql+pymysql://username:password@host:port/database_name
```

並在 `config.py` 中改為讀取環境變數，避免將資料庫帳號密碼直接寫在程式碼中。

---

## 資料庫初始化

### 1. 初始化 migration

```bash
flask db init
```

### 2. 建立 migration

```bash
flask db migrate
```

### 3. 更新資料庫

```bash
flask db upgrade
```

資料庫建立後，相關檔案會產生於 `instance` 或資料庫設定指定的位置。

---

## 執行專案

```bash
python app.py
```

啟動後可在瀏覽器開啟：

```text
http://127.0.0.1:5000
```

---

## 測試

本專案包含 pytest 測試檔案，可使用以下指令執行測試：

```bash
pytest
```

---

## 核心實作重點

- 使用 Flask 建立 Web Application
- 使用 Flask-Login 處理登入狀態
- 使用 SQLAlchemy 建立資料表模型與關聯
- 使用 Flask-Migrate 管理資料庫版本
- 使用 Jinja2 Template 建立前端頁面
- 將路由依功能拆分為 login、register、member、issue、propose、admin、notification 等模組
- 實作使用者與管理者角色區分
- 實作議題提案、審核、留言、收藏、投票與通知流程
- 使用 Pytest 建立基本路由測試

---

## 專案畫面

### 登入頁面

<p align="center">
  <img src="asset/readme/登入頁面.png" width="700">
</p>

### 議題列表與詳細頁面

<p align="center">
  <img src="asset/readme/議題列表頁面.png" width="700">
</p>

<p align="center">
  <img src="asset/readme/議題詳細頁面.png" width="700">
</p>

### 新增、預覽與編輯議題

<p align="center">
  <img src="asset/readme/新增議題.png" width="700">
</p>

<p align="center">
  <img src="asset/readme/預覽議題.png" width="700">
</p>

<p align="center">
  <img src="asset/readme/議題編輯頁面.png" width="700">
</p>

### 議題歷史頁面

<p align="center">
  <img src="asset/readme/議題歷史頁面.png" width="700">
</p>

### 管理者頁面

<p align="center">
  <img src="asset/readme/管理者首頁.png" width="700">
</p>

<p align="center">
  <img src="asset/readme/議題審核頁面.png" width="700">
</p>

<p align="center">
  <img src="asset/readme/議題審核頁面詳細.png" width="700">
</p>

## 作者

GitHub: https://github.com/pengleo5422
