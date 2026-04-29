# Financial Transaction Automation

Automates the entry of financial transactions into an accounting system using Python and Playwright.

Instead of manually entering each transaction, this script reads a spreadsheet and automatically fills in the data in the system — reducing human error and saving time.

---

## 🎯 Who is this for?

- Accounting professionals who need to enter large volumes of transactions
- Developers learning web automation with Playwright and Python

---

## 🛠️ Tech Stack

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-45ba4b?style=for-the-badge&logo=playwright&logoColor=white)](https://playwright.dev/python/)
[![openpyxl](https://img.shields.io/badge/openpyxl-217346?style=for-the-badge&logo=microsoftexcel&logoColor=white)](https://openpyxl.readthedocs.io/)
[![python-dotenv](https://img.shields.io/badge/python--dotenv-ECD53F?style=for-the-badge&logo=dotenv&logoColor=black)](https://pypi.org/project/python-dotenv/)

---

## 📁 Project Structure

```
financial-automation/
│
├── data/
│   └── lancamentos.xlsx      # Sample spreadsheet with transactions
│
├── logs/                     # Execution logs (auto-generated)
│
├── src/
│   ├── __init__.py
│   ├── login.py              # Authentication module
│   ├── spreadsheet.py        # Spreadsheet reading and validation
│   └── transactions.py       # Transaction insertion and reporting
│
├── tests/                    # Future test suite
│
├── main.py                   # Entry point
├── .env.example              # Environment variables template
├── requirements.txt          # Project dependencies
└── README.md
```

---

## ⚙️ Setup

**1. Clone the repository**

```bash
git clone https://github.com/your-username/financial-automation.git
cd financial-automation
```

**2. Create and activate a virtual environment**

```bash
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # macOS/Linux
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
playwright install chromium
```

**4. Configure environment variables**

```bash
cp .env.example .env
```

Open `.env` and fill in your credentials:

```env
EMAIL=your_email@example.com
PASSWORD=your_password
```

---

## 📊 Spreadsheet Format

The spreadsheet must have a sheet named `Lançamentos` with the following columns:

| description  | amount  | date       | type    | category | status   |
| ------------ | ------- | ---------- | ------- | -------- | -------- |
| Product sale | 1500.00 | 2024-01-10 | RECEITA | Vendas   | PAGO     |
| Office rent  | 2000.00 | 2024-01-15 | DESPESA | Moradia  | PENDENTE |

---

## ▶️ Usage

```bash
python main.py
```

Execution logs are saved to `logs/exec.log`. If any transaction fails, a screenshot is automatically saved in the project root for debugging.

---

## 🔍 How it works

The script is divided into four modules, each with a single responsibility:

**1. Spreadsheet reading (`spreadsheet.py`)**
Before opening the browser, the script reads and validates the Excel file row by row. Each row is converted into a `Transaction` object with normalized fields — amounts are formatted to two decimal places and dates are converted to `DD/MM/YYYY`. Invalid rows are skipped and logged without stopping the process.

**2. Authentication (`login.py`)**
The script navigates to the accounting system login page and fills in the credentials from the `.env` file. Login success is confirmed by waiting for a post-login element to become visible. If login fails, the script exits immediately with an error code.

**3. Transaction insertion (`transactions.py`)**
For each `Transaction` object, the script opens the new transaction modal, fills in all fields and waits for the modal to close as confirmation that the data was saved. If a transaction fails, a screenshot is captured automatically and the script moves on to the next one without stopping.

**4. Execution report**
At the end of each run, a summary is logged with the total number of transactions processed, how many succeeded and how many failed — including the error message for each failure.

```
==================================================
FINAL REPORT — 5 transactions processed
✅ Success: 4
❌ Failure: 1
  → 'Office rent': Timeout waiting for element
==================================================
```

---

## 👤 Author

<img src="https://avatars.githubusercontent.com/u/49914443?v=4" alt="José Neto" width="100" style="border-radius: 50%"/>

**José Neto** 👽

Made with ❤️ by José Neto 🤙 Get in touch!

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/josé-neto-299920152)
