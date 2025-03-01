# Web Enumeration Tool

## Overview
The **Web Enumeration Tool** is a powerful cybersecurity application designed to assist ethical hackers and penetration testers in identifying potential security vulnerabilities in web applications. The tool provides both **GUI and CLI** interfaces for flexible interaction, supporting **subdomain enumeration, port scanning, web crawling, directory enumeration, and security misconfiguration detection**.

This tool is developed as part of an **Ethical Hacking and Cybersecurity** project, incorporating **secure authentication, data protection, and resistance to MITM and DDoS attacks**.

## Features
- **Dual Interface Support**: Choose between a **Graphical User Interface (GUI)** or **Command Line Interface (CLI)**.
- **User Authentication**: Secure login and registration with **hashed passwords stored in a MySQL database**.
- **Subdomain Enumeration**: Identifies subdomains like `www`, `test`, `dev`, `staging`, and more.
- **Port Scanning**: Detects open ports such as **80 (HTTP), 443 (HTTPS), 8080, 22 (SSH)**.
- **Directory Enumeration**: Finds hidden directories such as `/admin`, `/backup`, and `/config`.
- **Security Misconfiguration Detection**: Identifies weaknesses such as missing security headers.
- **Data Storage**: Enumeration results are saved in a **structured JSON file (`web_enumeration_results.json`)** for further analysis.
- **Rate Limiting & DoS Protection**: Prevents abuse with rate limiting mechanisms.
- **HTTPS Enforcement & MITM Prevention**: Ensures secure communication between components.

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.10+
- MySQL Database (XAMPP recommended for local testing)
- Required Python libraries: `pip install -r requirements.txt`

### Steps to Install
1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/web-enumeration-tool.git
   cd web-enumeration-tool
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up MySQL Database:
   - Start **XAMPP** (or another MySQL server)
   - Create a database and update database credentials in `config.py`
4. Run the tool:
   - **GUI Mode**:
     ```sh
     python launcher.py --gui
     ```
   - **CLI Mode**:
     ```sh
     python launcher.py --cli
     ```

## Usage
- **Login/Register**: Create an account and authenticate using **secure MySQL-backed login**.
- **Enumeration**: Enter the target domain and perform web enumeration.
- **Results Storage**: Findings are automatically stored in `web_enumeration_results.json`.
- **Manual Guide**: Refer to the built-in help section for guidance on enumeration.

## Screenshots
Include relevant screenshots of:
- **Launcher Selection (GUI/CLI)**
- **Login/Registration Page**
- **Enumeration Input Page**
- **Enumeration Results Page**
- **CLI Execution Output**

## Unit Testing
Unit tests are included to verify the reliability of enumeration functions. Run tests using:
```sh
python -m unittest discover tests/
```
Example output:
```
Ran 5 tests in 1.903s
OK
```

## Future Improvements
- **AI-Based Threat Analysis**: Use ML models for risk assessment.
- **Automated Security Testing**: Extend support for **SQLi, XSS, SSRF, and IDOR detection**.
- **Real-Time Alerts**: Implement notifications for detected vulnerabilities.
- **Cloud-Based Deployment**: Develop a web-based version for remote security assessments.
- **Graphical Result Visualization**: Display results using dashboards and charts.

## Contributing
Contributions are welcome! Follow these steps:
1. Fork the repository
2. Create a new branch (`feature-branch`)
3. Commit changes (`git commit -m "Add feature"`)
4. Push to your fork and submit a PR

## License
This project is licensed under the MIT License - see the `LICENSE` file for details.

## Contact
For queries, reach out via GitHub Issues or email: **your-email@example.com**
