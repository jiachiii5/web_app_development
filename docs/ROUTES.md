# 路由與頁面設計文件

本文件根據 PRD、系統架構與資料庫設計，列出 Flask 後端的路由規劃、詳細邏輯與預計建立的頁面模板。

## 1. 路由總覽表格

| 功能模組 | HTTP 方法 | URL 路徑 | 對應模板 / 處理結果 | 說明 |
| --- | --- | --- | --- | --- |
| **首頁** | GET | `/` | `index.html` | 顯示歡迎畫面、介紹與準備抽籤入口 |
| **註冊/登入** | GET | `/auth/login` | `login.html` | 顯示會員註冊與登入表單 |
| | POST | `/auth/register` | 重導向至 `/auth/login` 或登入狀態 | 接收表單並建立新會員，存入資料庫 |
| | POST | `/auth/login` | 重導向至 `/` | 驗證帳密並將資料寫入 Session |
| | GET/POST | `/auth/logout` | 重導向至 `/` | 清除 Session，登出會員 |
| **個人紀錄** | GET | `/profile` | `history.html` | 從資料庫讀取該使用者的算命紀錄 |
| **抽籤算命** | POST | `/fortune/draw` | 重導向至 `/fortune/result/<id>` | 隨機抽出籤號並導向結果頁 |
| | GET | `/fortune/result/<id>` | `result.html` | 顯示對應 ID 的籤詩內容與詳解 |
| | POST | `/fortune/save` | 重導向至 `/profile` | 將抽籤結果與登入者綁定並寫入歷史紀錄 |
| | GET | `/fortune/share/<id>` | `share.html` (或單純縮圖 API) | 產生分享預覽或社群 meta tag 畫面 |
| **香油錢** | GET | `/donation` | `donation.html` | 顯示捐款說明與金額填寫選項 |
| | POST | `/donation/submit` | 重導向至 `/donation/success` | 將捐獻資料存入 DB |
| | GET | `/donation/success` | `donation_success.html` | 感謝使用者捐款的完成畫面 |

## 2. 每個路由的詳細說明

### 2.1 Main Router (`main.py`)
主要處理首頁、抽籤、個人紀錄頁面。

- **`GET /`**
  - 輸入：無
  - 處理邏輯：檢查 Session 的登入狀態，將使用者狀態帶入。
  - 輸出：渲染 `index.html`。
- **`POST /fortune/draw`**
  - 輸入：可能有隱藏欄位防止 CSRF。
  - 處理邏輯：
    1. 呼叫隨機演算法從 1~N (籤詩總數) 抽出一支籤。
    2. 若系統決定採用即時存檔，亦可在當下直接綁定歷史，但依規劃是由使用者到結果頁點擊「儲存籤詩」才存檔。
  - 輸出：重導向 `redirect(url_for('main.fortune_result', id=poem_id))`。
- **`GET /fortune/result/<id>`**
  - 輸入：URL 參數 `id` (poem.id)
  - 處理邏輯：呼叫 `Poem.get_by_id(id)`，找不到則 404。
  - 輸出：渲染 `result.html`。
- **`POST /fortune/save`**
  - 輸入：表單欄位 `poem_id`
  - 處理邏輯：
    1. 驗證是否登入 (`session.get('user_id')`)，若未登入則導向 `/auth/login`。
    2. 呼叫 `History.create(user_id, poem_id)`。
  - 輸出：重導向至 `/profile` 並彈出「儲存成功」訊息 (flash)。
- **`GET /profile`**
  - 輸入：無。
  - 處理邏輯：
    1. 驗證登入授權。
    2. 呼叫 `History.get_by_user(user_id)` 取得該使用者的過往紀錄。
  - 輸出：渲染 `history.html`。
- **`GET /fortune/share/<id>`**
  - 輸入：URL 參數 `id`。
  - 處理邏輯：取得 Poem 資訊，組合特定的 og:image 等 OpenGraph tags 供爬蟲抓取。
  - 輸出：渲染 `share.html`。

### 2.2 Auth Router (`auth.py`)
會員處理模組。

- **`GET /auth/login`**
  - 輸出：渲染 `login.html` (包含登入與註冊在同一頁切換或分成兩塊)。
- **`POST /auth/register`**
  - 輸入：表單 `username`, `password`, `email`
  - 處理邏輯：檢查 `username` 是否重複。若有重複閃現錯誤，若無則儲存 hash password 且呼叫 `User.create`，隨後寫入 `session`。
  - 輸出：重導向 `/` 或 `/auth/login`。
- **`POST /auth/login`**
  - 輸入：表單 `username`, `password`
  - 處理邏輯：`User.get_by_username()`，驗證雜湊密碼是否吻合。若是則寫入 `session['user_id']`，否則閃現錯誤。
  - 輸出：重導向 `/` 或返回 `/auth/login`。
- **`GET/POST /auth/logout`**
  - 處理邏輯：`session.clear()` 踢除對話。
  - 輸出：重導向 `/`。

### 2.3 Donation Router (`donation.py`)
香油錢與回饋功能。

- **`GET /donation`**
  - 輸入：無
  - 處理邏輯：取得登入使用者資訊（作為預設填寫）。
  - 輸出：渲染 `donation.html`。
- **`POST /donation/submit`**
  - 輸入：表單 `amount`, `message`
  - 處理邏輯：呼叫 `Donation.create` 寫入捐備紀錄。若未登入 `user_id` 可為 `None`。
  - 輸出：重導向 `/donation/success`。
- **`GET /donation/success`**
  - 輸出：渲染 `donation_success.html` 感謝頁面。

## 3. Jinja2 模板清單

所有的模板將繼承自核心 `base.html` 確保風格一致。

| 檔案名稱 | 繼承自 | 說明 |
| --- | --- | --- |
| `base.html` | (無) | 全站共用框架：包含 Header (導覽列/登入狀態)、Footer 及引入共用 CSS/JS |
| `index.html` | `base.html` | 首頁與籤筒動畫首頁介面 |
| `login.html` | `base.html` | 註冊與登入的表單畫 |
| `result.html` | `base.html` | 呈現籤首、解籤詳情介面 |
| `history.html` | `base.html` | 表格或卡片列出過往所有抽籤紀錄 |
| `donation.html` | `base.html` | 香油錢捐贈頁面與表單 |
| `donation_success.html` | `base.html` | 金流完成 (Mock) 之感謝介面 |
| `share.html` | `base.html` | 用於單一籤詩讓 FB/Line 爬蟲抓取的 Metadata 頁 |
