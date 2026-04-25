# 路由設計文件 (API Design)：課外活動報名系統

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **前台路由 (main_bp)** | | | | |
| 首頁 (活動列表) | GET | `/` | `index.html` | 顯示所有開放中的活動 |
| 活動詳情 | GET | `/activities/<int:activity_id>` | `activity.html` | 顯示單一活動與報名表單 |
| 送出報名 | POST | `/activities/<int:activity_id>/register`| — | 接收報名資料，存入 DB，重導向 |
| 報名成功頁面 | GET | `/activities/<int:activity_id>/success` | `success.html` | 顯示報名成功訊息 |
| **後台路由 (admin_bp)**| | | | |
| 管理員登入頁 | GET | `/admin/login` | `admin/login.html` | 顯示登入表單 |
| 管理員登入處理 | POST | `/admin/login` | — | 驗證帳密，設定 session，重導向 |
| 管理員登出 | GET | `/admin/logout` | — | 清除 session，重導向至登入頁 |
| 管理後台首頁 | GET | `/admin/` | `admin/dashboard.html`| 顯示所有活動清單與基本狀態 |
| 新增活動頁面 | GET | `/admin/activities/new` | `admin/activity_form.html`| 顯示新增活動表單 |
| 建立活動處理 | POST | `/admin/activities/new` | — | 接收表單存入 DB，重導向 |
| 編輯活動頁面 | GET | `/admin/activities/<int:activity_id>/edit` | `admin/activity_form.html`| 顯示編輯表單並帶入既有資料 |
| 更新活動處理 | POST | `/admin/activities/<int:activity_id>/edit` | — | 接收表單更新 DB，重導向 |
| 刪除活動處理 | POST | `/admin/activities/<int:activity_id>/delete`| — | 刪除活動，重導向回列表 |
| 檢視報名名單 | GET | `/admin/activities/<int:activity_id>/participants`| `admin/participants.html`| 顯示特定活動的報名者清單 |

---

## 2. 每個路由的詳細說明

### 前台路由 (Main)

#### `GET /`
- **處理邏輯**：呼叫 `ActivityModel.get_all()` 取得所有活動。
- **輸出**：渲染 `index.html`，帶入活動列表變數。

#### `GET /activities/<int:activity_id>`
- **處理邏輯**：呼叫 `ActivityModel.get_by_id(activity_id)` 與 `RegistrationModel.count_by_activity_id(activity_id)` 取得活動詳細與目前報名人數。
- **輸出**：渲染 `activity.html`，帶入活動詳情與剩餘名額變數。若找不到活動則回傳 404。

#### `POST /activities/<int:activity_id>/register`
- **輸入**：表單欄位 `name`, `student_id`, `email`, `phone`。
- **處理邏輯**：
  1. 檢查活動是否已額滿。
  2. 若未額滿，呼叫 `RegistrationModel.create()` 建立報名紀錄。
  3. 再次檢查是否達上限，若是則呼叫 `ActivityModel.update_full_status()` 關閉報名。
- **輸出**：成功後重導向至 `GET /activities/<int:activity_id>/success`，失敗則以 `flash` 顯示錯誤並重導向回活動頁。

---

### 後台路由 (Admin)

*(註：所有 `/admin` 底下的路由（除 login 以外）皆需透過裝飾器檢查 session 是否已登入。)*

#### `POST /admin/login`
- **輸入**：表單欄位 `username`, `password`。
- **處理邏輯**：比對帳號密碼，正確則寫入 session 標記已登入。
- **輸出**：成功重導向至 `/admin/`，失敗回傳登入頁並顯示錯誤。

#### `GET /admin/`
- **處理邏輯**：呼叫 `ActivityModel.get_all()`。
- **輸出**：渲染 `admin/dashboard.html`。

#### `POST /admin/activities/new`
- **輸入**：表單欄位 `title`, `description`, `event_time`, `location`, `capacity`。
- **處理邏輯**：呼叫 `ActivityModel.create()`。
- **輸出**：重導向至 `/admin/`。

#### `POST /admin/activities/<int:activity_id>/edit`
- **輸入**：表單欄位（同新增），可能包含 `is_full` 手動切換。
- **處理邏輯**：呼叫 `ActivityModel.update()`。
- **輸出**：重導向至 `/admin/`。

#### `POST /admin/activities/<int:activity_id>/delete`
- **處理邏輯**：呼叫 `ActivityModel.delete()`。
- **輸出**：重導向至 `/admin/`。

#### `GET /admin/activities/<int:activity_id>/participants`
- **處理邏輯**：呼叫 `RegistrationModel.get_by_activity_id(activity_id)` 取得名單。
- **輸出**：渲染 `admin/participants.html`。

---

## 3. Jinja2 模板清單

所有 HTML 檔案將放置於 `app/templates/` 目錄中：

- `base.html`: 基礎骨架模板（包含 `<html>`, `<head>`, 共用導覽列 Navbar 與 Footer），供其他頁面繼承 (`{% extends "base.html" %}`)。
- `index.html`: 前台首頁，繼承 `base.html`。
- `activity.html`: 單一活動詳情與報名表單頁，繼承 `base.html`。
- `success.html`: 報名成功提示頁，繼承 `base.html`。
- `admin/base_admin.html`: 後台專屬基礎模板（包含後台選單）。
- `admin/login.html`: 後台登入頁，繼承 `base.html` 或 `admin/base_admin.html` 皆可。
- `admin/dashboard.html`: 後台首頁（活動清單管理），繼承 `admin/base_admin.html`。
- `admin/activity_form.html`: 共用於新增/編輯活動的表單頁面，繼承 `admin/base_admin.html`。
- `admin/participants.html`: 報名名單檢視頁面，繼承 `admin/base_admin.html`。

---

## 4. 路由骨架程式碼

路由的骨架程式碼已分別建立於 `app/routes/main.py` 與 `app/routes/admin.py` 中。
