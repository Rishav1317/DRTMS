# DRTMS — Disaster Relief Resource Management and Tracking System
**VIT Chennai | BCSE301L Software Engineering | Case Study 1**

---

## Project Structure

```
DRTMS/
├── backend/
│   ├── app.py          → Flask REST API (all endpoints)
│   ├── drtms_core.py   → Core DRTMS logic (Resource, DisasterEvent, DRTMS classes)
│   └── requirements.txt
├── frontend/
│   └── index.html      → Full professional UI (single file, no build needed)
├── README.md
├── start.sh            → Linux/macOS startup script
└── start.bat           → Windows startup script
```

---

## How to Run

### Requirements
- **Python 3.7+** must be installed
- **Flask** must be installed (only external dependency)

---

### Step 1 — Install Flask

```bash
pip install flask
```

or on some systems:
```bash
pip3 install flask
```

---

### Step 2 — Start the Backend API

Open a terminal and run:

```bash
cd DRTMS/backend
python app.py
```

You should see:
```
=======================================================
  DRTMS API Server
  http://localhost:5000
=======================================================
```

---

### Step 3 — Open the Frontend

Open the frontend file in your browser:

- **Option A (easiest):** Double-click `frontend/index.html` to open in browser
- **Option B (recommended):** Use VS Code Live Server extension for best experience
- **Option C:** On macOS/Linux: `open frontend/index.html`

The frontend will connect to the backend automatically at `http://localhost:5000`.

---

### Quick Start Scripts

**Windows:** Double-click `start.bat`

**Linux/macOS:** Run `./start.sh` in terminal

---

## API Endpoints

| Method | Endpoint         | Description                     |
|--------|------------------|---------------------------------|
| GET    | /api/stats       | Dashboard statistics            |
| GET    | /api/resources   | List all resources               |
| POST   | /api/resources   | Add a new resource               |
| GET    | /api/disasters   | List all disaster events         |
| POST   | /api/disasters   | Register a new disaster          |
| POST   | /api/allocate    | Allocate resource to disaster    |
| POST   | /api/release     | Release resource from disaster   |
| GET    | /api/log         | Get full transaction log         |
| POST   | /api/tests       | Run all 18 test cases            |
| POST   | /api/reset       | Reset system to initial state    |

---

## Test Cases

The system includes 18 automated test cases:

### Valid Test Cases (8)
| ID     | Test                                      |
|--------|-------------------------------------------|
| TC-V01 | Register valid disaster event             |
| TC-V02 | Register second valid disaster            |
| TC-V03 | Allocate food packets to disaster D001    |
| TC-V04 | Allocate water bottles to disaster D001   |
| TC-V05 | Allocate medical kits to disaster D002    |
| TC-V06 | Allocate rescue personnel to D001         |
| TC-V07 | Release 50 food packets from D001         |
| TC-V08 | Allocate entire available tents to D002   |

### Invalid Test Cases (10)
| ID     | Test                                          |
|--------|-----------------------------------------------|
| TC-I01 | Register disaster with duplicate ID           |
| TC-I02 | Register disaster with severity out of range  |
| TC-I03 | Allocate to non-existent disaster             |
| TC-I04 | Allocate non-existent resource                |
| TC-I05 | Allocate more than available stock            |
| TC-I06 | Allocate zero quantity                        |
| TC-I07 | Allocate negative quantity                    |
| TC-I08 | Release more than allocated quantity          |
| TC-I09 | Release resource not allocated to disaster    |
| TC-I10 | Register disaster with empty ID               |

To run all test cases: click **Test Cases** in the sidebar → **Run All Tests**.

---

## Features

- **Dashboard** — real-time stats, resource utilisation bars, recent transactions
- **Resource Inventory** — view all resources with utilisation %, add new resources
- **Disaster Events** — register disasters, view severity, type, status
- **Allocate Resources** — core use case UC-02 with form validation
- **Release Resources** — UC-03 with dynamic dropdown showing allocated resources
- **Transaction Log** — full filterable audit trail with timestamps
- **Test Cases** — run all 18 test cases with PASS/FAIL results and summary

---

## Technology Stack

| Layer    | Technology                          |
|----------|-------------------------------------|
| Backend  | Python 3, Flask (REST API)          |
| Frontend | HTML5, CSS3, Vanilla JavaScript     |
| Storage  | In-memory (Python dictionaries)     |
| API      | RESTful JSON over HTTP              |
