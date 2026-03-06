# 🧪 SauceDemo Automation Framework

![CI](https://github.com/Arunkambrekar/saucedemo-automation-framework/actions/workflows/test.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Selenium](https://img.shields.io/badge/Selenium-4.x-green)
![PyTest](https://img.shields.io/badge/PyTest-8.x-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

A professional end-to-end test automation framework for the 
[SauceDemo](https://www.saucedemo.com) e-commerce application.
Built using **Selenium WebDriver**, **PyTest**, and 
**Page Object Model (POM)** design pattern with 
**CI/CD via GitHub Actions**.

---

## 🚀 Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.11 | Core language |
| Selenium WebDriver 4.x | Browser automation |
| PyTest | Test execution framework |
| Page Object Model (POM) | Design pattern |
| WebDriver Manager | Auto driver management |
| pytest-html | HTML report generation |
| GitHub Actions | CI/CD pipeline |

---

## 📁 Project Structure
```
saucedemo-automation-framework/
│
├── pages/                    # POM page classes
│   ├── login_page.py         # Login page locators & methods
│   ├── inventory_page.py     # Product listing page
│   ├── cart_page.py          # Shopping cart page
│   └── checkout_page.py      # Checkout flow page
│
├── tests/                    # Test cases
│   ├── test_login.py         # Login test scenarios
│   ├── test_inventory.py     # Product & cart tests
│   ├── test_checkout.py      # End-to-end checkout tests
│   └── test_api.py           # API test cases
│
├── utilities/                # Reusable helpers
│   ├── driver_factory.py     # Browser setup
│   └── config.py             # Base URLs & credentials
│
├── reports/                  # Auto-generated HTML reports
├── .github/
│   └── workflows/
│       └── test.yml          # GitHub Actions CI/CD pipeline
├── conftest.py               # PyTest fixtures & setup
├── requirements.txt          # Project dependencies
└── README.md
```

---

## ✅ Test Coverage

| Module | Test Cases | Status |
|--------|-----------|--------|
| Login | 5 | ✅ Passing |
| Inventory & Cart | 4 | ✅ Passing |
| Checkout | 3 | ✅ Passing |
| API Testing | 5 | ✅ Passing |
| **Total** | **17** | ✅ All Passing |

---

## 🧪 Test Scenarios Covered

**Login Module:**
- Valid login with correct credentials
- Invalid login with wrong password
- Login with empty username
- Login with empty password
- Locked out user error validation

**Inventory & Cart Module:**
- All products load on inventory page
- Add single item to cart
- Add multiple items to cart
- Remove item from cart
- Product sort by price and name

**Checkout Module:**
- Successful end-to-end purchase flow
- Checkout with missing first name
- Checkout with missing postal code

**API Module (reqres.in):**
- GET users — status code validation
- GET users — response body validation
- POST create user
- PUT update user
- DELETE user

---

## ⚙️ How to Run

### 1. Clone the repository
```bash
git clone https://github.com/Arunkambrekar/saucedemo-automation-framework.git
cd saucedemo-automation-framework
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run all tests
```bash
python -m pytest tests/ -v
```

### 4. Run with HTML report
```bash
python -m pytest tests/ -v --html=reports/report.html --self-contained-html
```

### 5. Run specific module only
```bash
python -m pytest tests/test_login.py -v
python -m pytest tests/test_api.py -v
```

---

## 🔄 CI/CD Pipeline

This framework runs automatically on every push to `main` via 
**GitHub Actions**:

- ✅ Installs Python 3.11
- ✅ Installs all dependencies
- ✅ Runs full test suite
- ✅ Uploads HTML report as artifact

---

## 📊 Sample Test Output
```
tests/test_login.py::TestLogin::test_valid_login         PASSED
tests/test_login.py::TestLogin::test_invalid_password    PASSED
tests/test_login.py::TestLogin::test_empty_username      PASSED
tests/test_login.py::TestLogin::test_locked_user         PASSED
tests/test_cart.py::TestCart::test_add_single_item       PASSED
tests/test_cart.py::TestCart::test_add_multiple_items    PASSED
tests/test_checkout.py::TestCheckout::test_successful    PASSED
tests/test_api.py::TestAPI::test_get_users               PASSED

8 passed in 35.42s
```

---

## 🎯 Key Design Decisions

**Why POM?**
Page Object Model separates test logic from UI locators.
If a locator changes, only the page class needs updating —
not every test file.

**Why explicit waits over implicit?**
Explicit waits target specific elements with specific 
conditions, making tests more stable and reliable 
than global implicit waits.

**Why GitHub Actions?**
Automated CI/CD ensures tests run on every code change,
catching regressions early without manual effort.

---

## 👨‍💻 Author

**Arun Kambrekar**  
QA Automation Engineer  
[LinkedIn](https://linkedin.com/in/arun-kambrekar) | 
[GitHub](https://github.com/Arunkambrekar)