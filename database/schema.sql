-- schema.sql
-- 此檔案用於初始化 SQLite 資料庫的資料表結構

-- 1. 管理者資料表 (admins)
CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. 活動資料表 (activities)
CREATE TABLE IF NOT EXISTS activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    event_time DATETIME NOT NULL,
    location TEXT NOT NULL,
    capacity INTEGER NOT NULL,
    is_full BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 3. 報名紀錄資料表 (registrations)
CREATE TABLE IF NOT EXISTS registrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    activity_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    student_id TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (activity_id) REFERENCES activities(id) ON DELETE CASCADE
);
