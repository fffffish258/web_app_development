# 流程圖文件 (Flowchart)：課外活動報名系統

## 1. 使用者流程圖 (User Flow)

本流程圖展示了兩類主要使用者（一般學生與管理者）在系統中的操作路徑。

```mermaid
flowchart LR
    A([使用者進入系統]) --> B{身分與目的？}

    %% 一般學生流程
    B -->|一般學生瀏覽活動| C[首頁 - 活動列表]
    C -->|點擊特定活動| D[活動詳細資訊頁]
    D --> E{是否已額滿？}
    E -->|是| F[顯示已額滿，報名按鈕隱藏]
    E -->|否| G[點擊報名按鈕]
    G --> H[填寫報名基本資料表單]
    H --> I[送出報名表單]
    I --> J([顯示報名成功畫面])

    %% 管理者流程
    B -->|系統管理者管理活動| K[管理員登入頁]
    K -->|登入成功| L[管理者後台 - Dashboard]
    L --> M{要執行什麼操作？}
    M -->|檢視所有活動| N[活動列表管理]
    M -->|建立新活動| O[填寫新增活動表單]
    O --> P([活動發布成功])
    N -->|檢視特定活動| Q[單一活動管理與報名名單]
    Q -->|匯出名單| R([下載報名者資料])
    Q -->|編輯/刪除活動| S([更新活動狀態])
```

## 2. 系統序列圖 (Sequence Diagram)

本圖描述學生「送出報名表單」到「資料存入資料庫」的完整後端處理流程，特別展示了額滿檢查的機制。

```mermaid
sequenceDiagram
    actor Student as 學生
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Model
    participant DB as SQLite 資料庫

    Student->>Browser: 填寫資料並點擊「送出報名」
    Browser->>Flask: POST /activity/<id>/register (傳送表單資料)
    
    Flask->>Model: 查詢該活動目前報名人數與上限
    Model->>DB: SELECT COUNT(*) FROM registrations
    DB-->>Model: 回傳目前人數
    Model-->>Flask: 目前人數
    
    alt 人數已達上限 (額滿)
        Flask-->>Browser: 回傳錯誤訊息 (已額滿，報名失敗)
        Browser-->>Student: 顯示「報名失敗，名額已滿」
    else 尚有名額
        Flask->>Model: 新增報名紀錄
        Model->>DB: INSERT INTO registrations (name, student_id, ...)
        DB-->>Model: 寫入成功
        Model-->>Flask: 報名成功
        
        %% 檢查是否剛好額滿
        Flask->>Flask: 檢查報名後是否達人數上限
        opt 剛好達上限
            Flask->>Model: 更新活動狀態為「已額滿」
            Model->>DB: UPDATE activities SET is_full = 1
        end
        
        Flask-->>Browser: 重導向至報名成功頁面
        Browser-->>Student: 顯示「報名成功！」
    end
```

## 3. 功能清單對照表

根據 PRD 定的功能需求，以下為系統預計實作的 URL 路徑與 HTTP 方法對照表。

| 功能描述 | 身分 | HTTP 方法 | URL 路徑 (建議) | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **首頁與活動列表** | 學生 | GET | `/` | 顯示所有開放中的活動 |
| **活動詳細資訊** | 學生 | GET | `/activity/<id>` | 顯示單一活動內容、剩餘名額與報名表單 |
| **送出報名表單** | 學生 | POST | `/activity/<id>/register` | 接收學生基本資料並存入資料庫 |
| **管理員登入** | 管理員 | GET/POST | `/admin/login` | 後台登入頁面與登入驗證處理 |
| **管理者後台首頁** | 管理員 | GET | `/admin` | 顯示所有活動狀態的 Dashboard |
| **建立新活動頁面** | 管理員 | GET | `/admin/activity/new` | 顯示新增活動的表單 |
| **新增活動 (處理)** | 管理員 | POST | `/admin/activity/new` | 接收表單資料並寫入資料庫 |
| **編輯活動** | 管理員 | GET/POST | `/admin/activity/<id>/edit` | 修改現有活動資訊 |
| **刪除/取消活動** | 管理員 | POST | `/admin/activity/<id>/delete` | 刪除或下架該活動 |
| **檢視報名名單** | 管理員 | GET | `/admin/activity/<id>/participants`| 查看該活動的所有報名者詳細資料 |
