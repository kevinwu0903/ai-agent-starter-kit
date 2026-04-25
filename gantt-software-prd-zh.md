# 產品需求文件（PRD）— 專案管理甘特圖軟體

## 1. 文件資訊
- **產品名稱**：GanttFlow（暫名）
- **版本**：v0.2（審閱修訂版）
- **日期**：2026-04-25
- **狀態**：待審閱
- **作者**：產品/研發協作草案

---

## 2. 背景與目標
目前多數團隊以 Excel/Sheets 管理時程，常見問題：
1. 任務依賴關係難以維護。
2. 排程變更需大量手動調整。
3. 對內對外報告（Excel/PDF）重工高。

**目標（MVP）**
- 以表單快速建專案與任務，並即時呈現在甘特圖。
- 支援任務依賴、里程碑、進度追蹤。
- 使用者輸入後可一鍵匯出 **Excel（.xlsx）** 與 **PDF（.pdf）**。

**非目標（MVP 不含）**
- AI 自動排程最佳化
- 即時多人同編（先做一般協作）
- 原生手機 App

---

## 3. 角色與權限（RBAC）
| 角色 | 主要能力 |
|---|---|
| Owner/PM | 建立專案、維護任務與依賴、匯出 Excel/PDF |
| Member | 更新任務進度、查看甘特圖 |
| Viewer | 僅查看與下載授權報表 |

> 權限原則：`可查看` ≠ `可匯出`（可獨立控管）。

---

## 4. 使用者故事（User Stories）
1. 作為 PM，我要快速輸入任務與日期並看到甘特圖。
2. 作為 PM，我要設定依賴關係，避免排程衝突。
3. 作為主管，我要一鍵匯出 PDF 於會議使用。
4. 作為 PM，我要匯出 Excel 做彙整分析。

---

## 5. 功能範圍

### 5.1 MVP 功能
- 專案 CRUD
- 任務 CRUD（含里程碑）
- 甘特圖視圖（日/週/月）
- 任務依賴（MVP：FS）
- 進度 (%) 與工時（規劃/實際）
- 匯出中心（Excel / PDF）
- 匯出紀錄（操作者、時間、條件）

### 5.2 後續版本
- Baseline 對比
- 資源負載視圖
- 進階權限與審批流程
- 外部整合（Calendar/Jira/Asana）

---

## 6. 輸入欄位設計

### 6.1 專案層級欄位
| 欄位 | 型別 | 必填 | 規則/說明 |
|---|---|---|---|
| project_name | string | 是 | 1-120 字，不可全空白 |
| project_code | string | 否 | 可設唯一 |
| owner_id | user_id | 是 | 專案負責人 |
| start_date | date | 是 | <= end_date |
| end_date | date | 是 | >= start_date |
| timezone | enum | 是 | 預設租戶時區 |
| working_calendar | enum | 否 | 例：Mon-Fri |
| status | enum | 是 | planning / active / done / archived |
| budget | number | 否 | >= 0 |
| description | text | 否 | <= 2000 字 |

### 6.2 任務層級欄位（甘特核心）
| 欄位 | 型別 | 必填 | 規則/說明 |
|---|---|---|---|
| task_id | string | 系統 | 唯一值 |
| project_id | string | 是 | 關聯專案 |
| task_name | string | 是 | 1-200 字 |
| wbs_code | string | 否 | 階層顯示 |
| task_type | enum | 是 | task / milestone |
| assignee_ids | array[user_id] | 否 | 可多人 |
| start_date | date | 是 | 需落於專案區間（可配置） |
| end_date | date | 是 | milestone 可同日 |
| duration_days | number | 否 | 若未填則由 start/end 推算 |
| progress_percent | int | 是 | 0~100 |
| dependency_task_id | string | 否 | 不可循環依賴 |
| dependency_type | enum | 否 | MVP 僅 FS |
| priority | enum | 否 | low/medium/high/urgent |
| planned_hours | number | 否 | >= 0 |
| actual_hours | number | 否 | >= 0 |
| risk_level | enum | 否 | low/medium/high |
| tags | array[string] | 否 | 單 tag <= 20 字 |
| notes | text | 否 | <= 1000 字 |

### 6.3 匯出設定欄位
| 欄位 | 型別 | 必填 | 規則/說明 |
|---|---|---|---|
| export_format | enum | 是 | excel / pdf |
| date_range_start | date | 否 | 空值代表全部 |
| date_range_end | date | 否 | 空值代表全部 |
| include_completed | bool | 否 | 是否包含已完成 |
| include_dependencies | bool | 否 | 是否含依賴欄位/箭線 |
| include_summary | bool | 否 | 是否附摘要頁 |
| pdf_orientation | enum | PDF必填 | portrait / landscape |
| pdf_page_size | enum | PDF必填 | A4 / A3 / Letter |
| excel_template | enum | Excel必填 | standard / executive |

---

## 7. 主要流程

### 7.1 建立排程
1. 建立專案（專案欄位）
2. 新增任務（任務欄位）
3. 設定依賴（FS）
4. 甘特圖即時刷新

### 7.2 匯出流程（Excel/PDF）
1. 點擊「匯出」
2. 選格式與條件
3. 驗證資料與權限
4. 產檔並下載
5. 寫入匯出紀錄

---

## 8. 匯出規格（可落地）

### 8.1 Excel（.xlsx）
**工作表**
- `Project_Summary`：專案資訊、總進度、關鍵里程碑
- `Task_List`：任務明細（含依賴、工時、風險）
- `Timeline`：日期軸 + 任務橫條（簡化甘特）

**格式要求**
- 日期欄為 date 格式
- 進度欄為百分比
- 凍結首列、開啟篩選
- 欄寬自動調整，超長文字換行

### 8.2 PDF（.pdf）
**內容區塊**
- 封面/摘要（名稱、區間、負責人、狀態）
- 甘特主視圖（日期區間）
- 里程碑與風險清單

**版面要求**
- 支援 A4/A3、直式/橫式
- Header：專案名稱
- Footer：頁碼、匯出時間、操作者

---

## 9. 匯出欄位對應（Input → Output）
| 輸入欄位 | Excel 對應 | PDF 對應 |
|---|---|---|
| project_name | Project_Summary.project_name | 摘要標題 |
| owner_id | Project_Summary.owner | 摘要負責人 |
| status | Project_Summary.status | 摘要狀態 |
| task_name | Task_List.task_name | 甘特列標題 |
| start_date/end_date | Task_List.start/end + Timeline | 甘特時間條 |
| progress_percent | Task_List.progress | 任務進度標示 |
| dependency_task_id | Task_List.dependency | 依賴列表/箭線（可選） |

---

## 10. 驗證規則與錯誤碼
| 規則 | 錯誤碼 | 使用者訊息 |
|---|---|---|
| end_date < start_date | DATE_RANGE_INVALID | 結束日期不可早於開始日期 |
| 依賴形成循環 | DEPENDENCY_CYCLE | 任務依賴不可形成循環 |
| 必填欄位缺漏 | REQUIRED_MISSING | 請完成必填欄位 |
| 無匯出權限 | EXPORT_FORBIDDEN | 你沒有匯出權限 |
| 產檔失敗 | EXPORT_FAILED | 匯出失敗，請稍後重試 |

---

## 11. API 合約草案（MVP）

### 11.1 建立專案
`POST /api/projects`
```json
{
  "project_name": "官網改版 Q3",
  "owner_id": "u_001",
  "start_date": "2026-05-01",
  "end_date": "2026-08-31",
  "timezone": "Asia/Taipei"
}
```

### 11.2 新增任務
`POST /api/projects/{project_id}/tasks`
```json
{
  "task_name": "UI 設計初稿",
  "task_type": "task",
  "start_date": "2026-05-03",
  "end_date": "2026-05-10",
  "progress_percent": 40,
  "dependency_task_id": "T-0000",
  "dependency_type": "FS"
}
```

### 11.3 匯出
`POST /api/projects/{project_id}/exports`
```json
{
  "export_format": "pdf",
  "date_range_start": "2026-05-01",
  "date_range_end": "2026-06-30",
  "include_completed": true,
  "pdf_orientation": "landscape",
  "pdf_page_size": "A4"
}
```

---

## 12. 非功能需求（NFR）
- **效能**：1000 任務載入 < 3 秒（快取後）
- **可靠性**：匯出成功率 >= 99%
- **安全**：所有匯出需權限驗證 + 審計紀錄
- **相容**：Chrome/Edge/Safari 最新兩版
- **可觀測**：匯出失敗可追蹤（error code + trace id）

---

## 13. KPI 與驗收標準

### 13.1 KPI（上線後 3 個月）
- 活躍專案 70% 至少匯出一次
- PM 每週更新率 >= 50%
- 匯出平均等待 < 10 秒（100 任務）

### 13.2 UAT 驗收
1. 可建立專案並新增 20+ 任務正確顯示於甘特
2. 可設依賴且正確阻擋循環
3. Excel 匯出欄位/格式符合規格
4. PDF 匯出可讀且版面正確
5. 匯出紀錄可查詢（人/時/條件）

---

## 14. 里程碑
- W1：需求凍結 + 欄位確版
- W2-W3：專案/任務 CRUD + 甘特基礎
- W4：依賴驗證與錯誤處理
- W5：Excel/PDF 匯出
- W6：UAT + 修正 + 上線

---

## 15. 待你確認（下一輪）
1. PDF 偏「簡報版」或「任務明細版」？
2. Excel 欄位順序固定或允許自訂？
3. 是否需匯出前預覽？
4. 是否要納入「多人即時協作」到 v1.1？

---

## 16. 功能需求清單（可追蹤）

### 16.1 Functional Requirements（FR）
| ID | 需求描述 | 優先級 | 驗收條件（摘要） |
|---|---|---|---|
| FR-01 | 系統可建立/編輯/封存專案 | Must | 可完成專案 CRUD，封存後不可再編輯任務 |
| FR-02 | 系統可新增/編輯/刪除任務與里程碑 | Must | 任務資料可持久化，甘特圖即時同步 |
| FR-03 | 支援 FS 任務依賴與循環檢查 | Must | 循環依賴建立時需阻擋並顯示錯誤 |
| FR-04 | 支援進度百分比與工時欄位 | Must | 進度 0~100，工時不可負數 |
| FR-05 | 支援 Excel 匯出 | Must | 產出含 Summary/Task/Timeline 三分頁 |
| FR-06 | 支援 PDF 匯出 | Must | 產出含摘要、甘特圖、里程碑/風險 |
| FR-07 | 匯出需記錄審計資訊 | Must | 紀錄操作者、時間、條件、結果 |
| FR-08 | 匯出可依日期區間與條件篩選 | Should | 匯出內容符合篩選條件 |
| FR-09 | 提供匯出歷程查詢頁 | Should | 可查詢近 90 天匯出紀錄 |
| FR-10 | 支援模板（Excel standard/executive） | Could | 可切換模板並輸出成功 |

### 16.2 Non-Functional Requirements（NFR）
| ID | 需求描述 | 指標 |
|---|---|---|
| NFR-01 | 載入效能 | 1000 任務首次載入 < 3 秒（快取後） |
| NFR-02 | 匯出可靠性 | 成功率 >= 99% |
| NFR-03 | 匯出效能 | 100 任務匯出平均 < 10 秒 |
| NFR-04 | 安全性 | 匯出前必須權限驗證 |
| NFR-05 | 可觀測性 | 失敗事件需帶 error code + trace id |

---

## 17. 畫面資訊架構（IA）與頁面需求

### 17.1 頁面清單
1. `Project List`：專案清單、篩選、建立按鈕
2. `Project Detail / Gantt`：甘特主畫面、任務表格、依賴設定
3. `Task Editor Drawer`：任務新增/編輯表單
4. `Export Modal`：選格式與匯出條件
5. `Export History`：匯出紀錄與下載連結

### 17.2 關鍵互動
- 拖曳調整任務條長度 => 更新 start/end。
- 拖曳任務橫條 => 整段平移時間。
- 依賴建立後若衝突 => 顯示錯誤並回復原狀。

---

## 18. 邊界情境（Edge Cases）
1. 任務跨時區顯示偏移：以專案 timezone 為準。
2. 里程碑日期落在非工作日：允許，但標記提示。
3. 匯出期間無任務：仍產出檔案並顯示「No Data」。
4. 任務名稱超長：畫面截斷，完整字串在 tooltip 與輸出保留。
5. 大型專案（>5000 任務）：採分頁/虛擬滾動與背景匯出。

---

## 19. QA 測試案例（精簡版）
| Case ID | 測試目標 | 前置條件 | 預期結果 |
|---|---|---|---|
| QA-01 | 建立專案成功 | 具 PM 權限 | 專案建立成功並可進入甘特頁 |
| QA-02 | 日期檢核 | end < start | 阻擋送出並顯示 DATE_RANGE_INVALID |
| QA-03 | 依賴循環檢核 | A->B->A | 阻擋儲存並顯示 DEPENDENCY_CYCLE |
| QA-04 | Excel 匯出內容 | 有 20 筆任務 | 三分頁完整且欄位正確 |
| QA-05 | PDF 匯出版面 | 選 A4 橫式 | 版面正常，含頁首頁尾 |
| QA-06 | 權限檢核 | Viewer 無匯出權 | 回傳 EXPORT_FORBIDDEN |

---

## 20. 版本切分建議（Release Plan）
- **v1.0（MVP）**：FR-01 ~ FR-07（核心流程可閉環）
- **v1.1**：FR-08、FR-09（匯出治理與管理性）
- **v1.2**：FR-10 + 多人即時協作評估

---

## 21. 表單與按鈕行為規格（UI/UX）

### 21.1 專案表單（Create/Edit Project）
- 主要按鈕：`儲存`、`取消`
- 次要按鈕：`儲存並新增任務`
- 驗證行為：
  - 欄位 blur 即時驗證（格式/必填）
  - 點擊 `儲存` 進行整體驗證
  - 若驗證失敗，聚焦第一個錯誤欄位

### 21.2 任務表單（Task Drawer）
- 主要按鈕：`儲存任務`
- 次要按鈕：`刪除任務`（編輯模式）
- 行為規則：
  - `task_type=milestone` 時，自動鎖定 `duration_days=0`
  - `progress_percent=100` 時，提示是否同步狀態為 done

### 21.3 匯出按鈕（核心需求）
- 畫面位置：甘特頁右上角 `匯出`
- 點擊後：開啟 `Export Modal`，可選 `Excel` / `PDF`
- 按鈕狀態：
  - `匯出中...`：disabled，顯示 loading
  - `匯出完成`：toast + 下載連結
  - `匯出失敗`：toast + 錯誤碼 + `重試`
- 權限控制：無匯出權限時，按鈕隱藏或 disabled（由租戶策略決定）

### 21.4 匯出 Modal 欄位互斥規則
- 選 `Excel`：顯示 `excel_template`，隱藏 PDF 版面設定。
- 選 `PDF`：顯示 `pdf_orientation`、`pdf_page_size`，隱藏 Excel 模板。
- 未填必填參數：`開始匯出` 按鈕 disabled。

---

## 22. 匯出檔案內容驗收清單（Checklist）

### 22.1 Excel 驗收清單
- [ ] 檔名格式：`{project_code}_{YYYYMMDD_HHmm}.xlsx`
- [ ] `Project_Summary` 存在且關鍵欄位完整
- [ ] `Task_List` 含 task_name/start/end/progress/dependency
- [ ] `Timeline` 日期軸連續且無格式錯亂
- [ ] 日期欄位可被 Excel 視為日期（非文字）

### 22.2 PDF 驗收清單
- [ ] 檔名格式：`{project_code}_{YYYYMMDD_HHmm}.pdf`
- [ ] 頁首顯示專案名稱
- [ ] 頁尾顯示頁碼與匯出時間
- [ ] 甘特圖可閱讀（字體/比例/頁面裁切正常）
- [ ] 若無資料，顯示 No Data 並保留摘要頁

---

## 23. 稽核與法遵需求（Audit/Compliance）
- 匯出行為需寫入審計日誌：
  - user_id
  - project_id
  - export_format
  - filter_payload（遮罩敏感資訊）
  - result（success/fail）
  - timestamp（UTC）
- 審計資料保留期：預設 180 天（可配置）。
- 若租戶啟用法遵模式：
  - 匯出檔自動加浮水印（使用者/時間）
  - 可限制僅 PDF 可匯出（禁用 Excel）
