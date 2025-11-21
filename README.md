## Restful Booker API Automation Framework

### Overview
This project is a professionally structured End-to-End API automation framework for the Restful Booker service. It demonstrates modern API testing practices including OOP design, test isolation, configuration management, and scalable architecture using Python and pytest.

### Objectives
- Validate API functionality via real HTTP requests
- Demonstrate CRUD journey flow
- Showcase professional test automation structure
- Provide reusable API client abstraction

### Technology Stack
- Python 3.10+
- Pytest
- Requests
- Pydantic

### Features
- Token-based authentication
- Full booking lifecycle coverage
- OOP-based API wrapper
- Modular design & scalable structure
- CI-ready configuration

### How to Run
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pytest
```

### Reports Generation

#### HTML Reports
Pytest can generate a human-readable HTML report:
1. Install the plugin:
```bash
pip install pytest-html
```
2. Run tests with HTML report:
```bash
pytest --html=report.html
```
3. Open `report.html` in a browser to view test results.

#### Allure Reports (Optional, Professional)
Allure provides rich, interactive test reports:
1. Install dependencies:
```bash
pip install allure-pytest
```
2. Run tests with Allure reporting:
```bash
pytest --alluredir=allure-results
```
3. Generate and serve the report:
```bash
allure serve allure-results
```
4. The report shows:
   - Step-by-step execution
   - Status of each test
   - Attachments (screenshots, logs, JSON responses)
   - Historical trend charts (if run multiple times)

