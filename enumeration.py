import requests
import threading
import socket
import json
import logging
import re
import bcrypt
import os
import jwt
import time
from queue import Queue
from abc import ABC, abstractmethod
from urllib.parse import urljoin

# Configure Logging
logging.basicConfig(
    filename='web_enumeration.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Security Config
USER_FILE = "users.json"
SECRET_KEY = "your_secret_key"  # Change this for security
TOKEN_EXPIRATION = 3600  # 1 hour

# Load & Save Users
def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as file:
        return json.load(file)

def save_users(users):
    with open(USER_FILE, "w") as file:
        json.dump(users, file, indent=4)

# Hash & Verify Passwords
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

# Generate & Verify JWT Tokens
def generate_token(username):
    payload = {"user": username, "exp": time.time() + TOKEN_EXPIRATION}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user"]
    except jwt.ExpiredSignatureError:
        print("❌ Token expired! Please log in again.")
    except jwt.InvalidTokenError:
        print("❌ Invalid token! Please log in again.")
    return None

# User Authentication System
def authenticate_user():
    users = load_users()
    token = None
    
    while not token:
        print("\n🔒 User Authentication")
        print("[1] Login")
        print("[2] Register")
        print("[3] Exit")
        choice = input("Select an option: ").strip()

        if choice == "1":  # Login
            username = input("Username: ").strip()
            password = input("Password: ").strip()

            if username in users and verify_password(password, users[username]):
                token = generate_token(username)
                print("✅ Login Successful!")
            else:
                print("❌ Invalid Credentials. Try again.")

        elif choice == "2":  # Register
            username = input("Choose a Username: ").strip()
            if username in users:
                print("❌ Username already exists!")
                continue
            password = input("Choose a Password: ").strip()
            users[username] = hash_password(password)
            save_users(users)
            print("✅ Registration successful! You can now log in.")

        elif choice == "3":  # Exit
            print("Exiting... Goodbye!")
            exit()

        else:
            print("❌ Invalid choice, try again.")
    return token

# Abstract Class for Enumeration
class Enumerator(ABC):
    def __init__(self, target):
        self.target = target
    @abstractmethod
    def enumerate(self):
        pass

# Subdomain Enumeration
class SubdomainEnumerator(Enumerator):
    def __init__(self, target, subdomains):
        super().__init__(target)
        self.subdomains = subdomains
    def enumerate(self):
        found_subdomains = []
        for subdomain in self.subdomains:
            url = f"https://{subdomain}.{self.target}"
            try:
                response = requests.get(url, timeout=3)
                if response.status_code < 400:
                    found_subdomains.append(url)
            except requests.exceptions.RequestException:
                pass
        return found_subdomains

# Port Scanning
class PortScanner(Enumerator):
    def __init__(self, target, ports):
        super().__init__(target)
        self.ports = ports
    def enumerate(self):
        open_ports = []
        for port in self.ports:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                if s.connect_ex((self.target, port)) == 0:
                    open_ports.append(port)
        return open_ports

# Run Enumeration
def run_enumeration(target):
    print(f"\n🔍 Enumerating: {target}\n")

    subdomains = ["www", "test", "dev", "staging"]
    sub_enum = SubdomainEnumerator(target, subdomains)
    found_subdomains = sub_enum.enumerate()
    print(f"✅ Found subdomains: {found_subdomains}")

    ports = [80, 443, 8080, 22]
    port_scan = PortScanner(target, ports)
    open_ports = port_scan.enumerate()
    print(f"✅ Open ports: {open_ports}")

    results = {
        "subdomains": found_subdomains,
        "open_ports": open_ports
    }
    with open("web_enumeration_results.json", "w") as f:
        json.dump(results, f, indent=4)

    print("\n✅ Results saved to 'web_enumeration_results.json'")
    print("📌 Enumeration Completed!\n")

# CLI Menu
def main():
    token = authenticate_user()
    if not verify_token(token):
        return

    while True:
        print("\n🌐 Web Enumeration Tool")
        print("----------------------------")
        print("[1] Run Enumeration")
        print("[2] Exit")
        choice = input("Select an option: ").strip()

        if choice == "1":
            target = input("\nEnter Target Domain (e.g., example.com): ").strip()
            if target:
                run_enumeration(target)
            else:
                print("❌ Please enter a valid target domain.")

        elif choice == "2":
            print("Exiting... Goodbye!")
            exit()

        else:
            print("❌ Invalid choice, try again.")

# Run CLI Tool
if __name__ == "__main__":
    main()



# import requests
# import threading
# import socket
# import json
# import logging
# import re
# import bcrypt
# import os
# from queue import Queue
# from abc import ABC, abstractmethod
# from urllib.parse import urljoin, urlparse, urlunparse

# # Configure Logging
# logging.basicConfig(
#     filename='web_enumeration.log',
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )

# # User Authentication File
# USER_FILE = "users.json"

# # Load & Save Users
# def load_users():
#     if not os.path.exists(USER_FILE):
#         return {}
#     with open(USER_FILE, "r") as file:
#         return json.load(file)

# def save_users(users):
#     with open(USER_FILE, "w") as file:
#         json.dump(users, file, indent=4)

# # Hash & Verify Passwords
# def hash_password(password):
#     return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# def verify_password(password, hashed):
#     return bcrypt.checkpw(password.encode(), hashed.encode())

# # User Authentication System
# def authenticate_user():
#     users = load_users()
    
#     while True:
#         print("\n🔒 User Authentication")
#         print("[1] Login")
#         print("[2] Register")
#         print("[3] Exit")
#         choice = input("Select an option: ").strip()

#         if choice == "1":  # Login
#             username = input("Username: ").strip()
#             password = input("Password: ").strip()

#             if username in users and verify_password(password, users[username]):
#                 print("✅ Login Successful!\n")
#                 return True
#             else:
#                 print("❌ Invalid Credentials. Try again.")

#         elif choice == "2":  # Register
#             username = input("Choose a Username: ").strip()
#             if username in users:
#                 print("❌ Username already exists!")
#                 continue
            
#             password = input("Choose a Password: ").strip()
#             users[username] = hash_password(password)
#             save_users(users)
#             print("✅ Registration successful! You can now log in.")

#         elif choice == "3":  # Exit
#             print("Exiting... Goodbye!")
#             exit()

#         else:
#             print("❌ Invalid choice, try again.")

# # Abstract Class for Enumeration
# class Enumerator(ABC):
#     def __init__(self, target):
#         self.target = target

#     @abstractmethod
#     def enumerate(self):
#         pass

# # Subdomain Enumeration
# class SubdomainEnumerator(Enumerator):
#     def __init__(self, target, subdomains):
#         super().__init__(target)
#         self.subdomains = subdomains

#     def enumerate(self):
#         found_subdomains = []
#         for subdomain in self.subdomains:
#             url = f"http://{subdomain}.{self.target}"
#             try:
#                 response = requests.get(url, timeout=3)
#                 if response.status_code < 400:
#                     found_subdomains.append(url)
#             except requests.exceptions.RequestException:
#                 pass
#         return found_subdomains

# # Port Scanning
# class PortScanner(Enumerator):
#     def __init__(self, target, ports):
#         super().__init__(target)
#         self.ports = ports

#     def enumerate(self):
#         open_ports = []
#         for port in self.ports:
#             with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#                 s.settimeout(1)
#                 if s.connect_ex((self.target, port)) == 0:
#                     open_ports.append(port)
#         return open_ports

# # Web Crawling
# class WebCrawler(Enumerator):
#     def __init__(self, target_url):
#         super().__init__(target_url)
#         self.visited = set()

#     def enumerate(self):
#         self._crawl(self.target)
#         return self.visited

#     def _crawl(self, url):
#         if url in self.visited:
#             return
#         try:
#             response = requests.get(url)
#             self.visited.add(url)
#             for link in re.findall(r'href=[\'"]?([^\'" >]+)', response.text):
#                 absolute_link = urljoin(url, link)
#                 self._crawl(absolute_link)
#         except requests.exceptions.RequestException:
#             pass

# # Directory Enumeration
# class DirectoryEnumerator(Enumerator):
#     def __init__(self, target, wordlist):
#         super().__init__(target)
#         self.wordlist = wordlist

#     def enumerate(self):
#         found_directories = []
#         for directory in self.wordlist:
#             url = f"http://{self.target}/{directory}"
#             try:
#                 response = requests.get(url, timeout=3)
#                 if response.status_code < 400:
#                     found_directories.append(url)
#             except requests.exceptions.RequestException:
#                 pass
#         return found_directories

# # Run Enumeration
# def run_enumeration(target):
#     print(f"\n🔍 Enumerating: {target}\n")

#     # Subdomain Enumeration
#     subdomains = ["www", "test", "dev", "staging"]
#     subdomain_enum = SubdomainEnumerator(target, subdomains)
#     print("🔹 Enumerating subdomains...")
#     found_subdomains = subdomain_enum.enumerate()
#     print(f"✅ Found subdomains: {found_subdomains}")

#     # Port Scanning
#     ports = [80, 443, 8080, 22]
#     port_scanner = PortScanner(target, ports)
#     print("🔹 Scanning ports...")
#     open_ports = port_scanner.enumerate()
#     print(f"✅ Open ports: {open_ports}")

#     # Web Crawling
#     crawler = WebCrawler(f"http://{target}")
#     print("🔹 Starting web crawling...")
#     crawled_urls = crawler.enumerate()
#     print(f"✅ Crawled URLs: {list(crawled_urls)}")

#     # Directory Enumeration
#     wordlist = ["admin", "backup", "hidden", "config", "uploads"]
#     directory_enum = DirectoryEnumerator(target, wordlist)
#     print("🔹 Enumerating directories...")
#     found_directories = directory_enum.enumerate()
#     print(f"✅ Found directories: {found_directories}")

#     # Save Results
#     results = {
#         "subdomains": found_subdomains,
#         "open_ports": open_ports,
#         "crawled_urls": list(crawled_urls),
#         "found_directories": found_directories
#     }
#     with open("web_enumeration_results.json", "w") as f:
#         json.dump(results, f, indent=4)

#     print("\n✅ Results saved to 'web_enumeration_results.json'")
#     print("📌 Enumeration Completed!\n")

# # CLI Menu
# def main():
#     # Authenticate User
#     authenticate_user()

#     while True:
#         print("\n🌐 Web Enumeration Tool")
#         print("----------------------------")
#         print("[1] Run Enumeration")
#         print("[2] Exit")
#         choice = input("Select an option: ").strip()

#         if choice == "1":
#             target = input("\nEnter Target Domain (e.g., example.com): ").strip()
#             if target:
#                 run_enumeration(target)
#             else:
#                 print("❌ Please enter a valid target domain.")

#         elif choice == "2":
#             print("Exiting... Goodbye!")
#             exit()

#         else:
#             print("❌ Invalid choice, try again.")

# # Run CLI Tool
# if __name__ == "__main__":
#     main()