#!/usr/bin/env python3
# Coded by darkboss1
# Advanced Admin Panel Scanner with Menu System

import os
import sys
import requests
import time
import urllib3
from concurrent.futures import ThreadPoolExecutor, as_completed

# SSL warning disable
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class AdminPanelScanner:
    def __init__(self):
        self.found_panels = []
        self.total_tested = 0
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_banner(self):
        self.clear_screen()
        print("\033[94m" + "=" * 70)
        print("           🛡️  ADMIN PANEL SCANNER TOOL 🛡️")
        print("                 Coded by darkboss1")
        print("=" * 70 + "\033[0m")
        print()
    
    def show_menu(self):
        self.show_banner()
        print("📋 MAIN MENU:")
        print("1. Single URL Scan")
        print("2. Multiple URLs from file")
        print("3. Custom wordlist scan")
        print("4. View previous results")
        print("5. Exit")
        print()
    
    def get_admin_paths(self):
        """Return comprehensive list of admin paths"""
        return [
            "/admin", "/administrator", "/admin/login", "/admincp", "/cpanel", 
            "/wp-admin", "/wp-login.php", "/controlpanel", "/webadmin", "/manager",
            "/panel", "/login", "/signin", "/dashboard", "/backend", "/system",
            "/user/login", "/admin_area", "/admin1", "/admin2", "/admin4",
            "/admin/login.php", "/admin/login.asp", "/admin/login.html",
            "/administrator/login.php", "/administrator/login.asp", 
            "/administrator/login.html", "/admin/index.php", "/admin/index.html",
            "/admin/account.php", "/admin/controlpanel.php", "/admin/cp.php",
            "/bb-admin", "/bb-admin/admin.php", "/acceso", "/access", "/account",
            "/adm", "/admusr", "/auth", "/authentication", "/blogindex",
            "/customer_login", "/database_administration", "/directadmin",
            "/fileadmin", "/formslogin", "/hpwebjetadmin", "/irc-macadmin",
            "/liveuser_admin", "/log-in", "/member", "/memberadmin", "/members",
            "/moderator", "/myadmin", "/newsadmin", "/openvpnadmin", "/pages/admin",
            "/panel-administracion", "/pgadmin", "/phpldapadmin", "/phpmyadmin",
            "/phppgadmin", "/pureadmin", "/root", "/server", "/server_admin_small",
            "/siteadmin", "/sql-admin", "/sshadmin", "/super", "/super_index",
            "/superman", "/superuser", "/support_login", "/sys-admin", "/sysadmin",
            "/system-administration", "/typo3", "/ur-admin", "/user", "/users",
            "/utility_login", "/vadmind", "/vmailadmin", "/webmaster", "/wizmysqladmin",
            "/xlogin", "/yonetici", "/yonetim", "/0admin", "/0manager", "/aadmin",
            "/acceso.php", "/access.php", "/account.asp", "/adm.php", "/admin.asp",
            "/admin.htm", "/admin.php", "/admin/", "/admin_area/", "/admincontrol/",
            "/admincp/", "/administr8/", "/administration/", "/administrator/",
            "/adminpanel/", "/admins/", "/autologin/", "/ccp14admin/", "/cmsadmin/",
            "/control/", "/cp/", "/cpanel/", "/member/", "/moderator/", "/pgadmin/",
            "/phpmyadmin/", "/phppgadmin/", "/webadmin/", "/wp-admin/", "/wp-login.php"
        ]
    
    def check_url(self, url, path):
        """Check a single URL path"""
        full_url = url + path
        try:
            response = self.session.get(
                full_url, 
                timeout=8, 
                verify=False,
                allow_redirects=True
            )
            
            # Check if it's a valid admin page
            if response.status_code == 200:
                content_length = len(response.content)
                # Filter out small/error pages and very large pages
                if 100 < content_length < 50000:
                    # Check for common admin keywords in content
                    content_lower = response.text.lower()
                    admin_keywords = ['admin', 'login', 'password', 'username', 'panel', 'dashboard', 'control']
                    keyword_count = sum(1 for keyword in admin_keywords if keyword in content_lower)
                    
                    if keyword_count >= 2:  # At least 2 admin keywords
                        return full_url, response.status_code, content_length
            
            return None
            
        except Exception:
            return None
    
    def scan_single_url(self):
        self.show_banner()
        print("🔍 SINGLE URL SCAN")
        print("-" * 50)
        
        url = input("Enter target URL (e.g., http://example.com): ").strip()
        if not url:
            print("❌ No URL provided!")
            input("Press Enter to continue...")
            return
        
        url = url.rstrip('/')
        
        print(f"\n🎯 Target: {url}")
        print("⏳ Scanning started...")
        print("-" * 50)
        
        admin_paths = self.get_admin_paths()
        self.found_panels = []
        self.total_tested = 0
        
        start_time = time.time()
        
        # Use threading for faster scanning
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_path = {
                executor.submit(self.check_url, url, path): path 
                for path in admin_paths
            }
            
            for future in as_completed(future_to_path):
                self.total_tested += 1
                path = future_to_path[future]
                
                try:
                    result = future.result()
                    if result:
                        full_url, status_code, content_length = result
                        self.found_panels.append(full_url)
                        print(f"\033[92m[✅ FOUND] {full_url} (Size: {content_length} bytes)\033[0m")
                    else:
                        print(f"[{self.total_tested}/{len(admin_paths)}] Testing: {path}")
                        
                except Exception as e:
                    print(f"\033[91m[❌ ERROR] {path}: {str(e)}\033[0m")
        
        end_time = time.time()
        self.show_scan_summary(url, end_time - start_time)
    
    def scan_multiple_urls(self):
        self.show_banner()
        print("🔍 MULTIPLE URL SCAN")
        print("-" * 50)
        
        file_path = input("Enter file path containing URLs (one per line): ").strip()
        
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            input("Press Enter to continue...")
            return
        
        try:
            with open(file_path, 'r') as f:
                urls = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            input("Press Enter to continue...")
            return
        
        if not urls:
            print("❌ No URLs found in file!")
            input("Press Enter to continue...")
            return
        
        print(f"\n📄 Found {len(urls)} URLs to scan")
        input("Press Enter to start scanning...")
        
        all_results = {}
        
        for url in urls:
            url = url.rstrip('/')
            print(f"\n🎯 Scanning: {url}")
            print("-" * 40)
            
            admin_paths = self.get_admin_paths()
            found_for_url = []
            
            # Single URL scan without threading for simplicity
            for i, path in enumerate(admin_paths, 1):
                result = self.check_url(url, path)
                if result:
                    full_url, status_code, content_length = result
                    found_for_url.append(full_url)
                    print(f"\033[92m[✅ FOUND] {full_url}\033[0m")
                else:
                    print(f"[{i}/{len(admin_paths)}] Testing: {path}")
            
            all_results[url] = found_for_url
        
        self.show_multi_scan_summary(all_results)
    
    def custom_wordlist_scan(self):
        self.show_banner()
        print("🔍 CUSTOM WORDLIST SCAN")
        print("-" * 50)
        
        url = input("Enter target URL: ").strip()
        wordlist_path = input("Enter custom wordlist path: ").strip()
        
        if not url or not wordlist_path:
            print("❌ URL and wordlist path are required!")
            input("Press Enter to continue...")
            return
        
        if not os.path.exists(wordlist_path):
            print(f"❌ Wordlist file not found: {wordlist_path}")
            input("Press Enter to continue...")
            return
        
        try:
            with open(wordlist_path, 'r') as f:
                custom_paths = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"❌ Error reading wordlist: {e}")
            input("Press Enter to continue...")
            return
        
        url = url.rstrip('/')
        print(f"\n🎯 Target: {url}")
        print(f"📁 Wordlist: {len(custom_paths)} paths")
        print("⏳ Scanning started...")
        print("-" * 50)
        
        self.found_panels = []
        
        for i, path in enumerate(custom_paths, 1):
            result = self.check_url(url, path)
            if result:
                full_url, status_code, content_length = result
                self.found_panels.append(full_url)
                print(f"\033[92m[✅ FOUND] {full_url}\033[0m")
            else:
                print(f"[{i}/{len(custom_paths)}] Testing: {path}")
        
        self.show_custom_scan_summary(url, len(custom_paths))
    
    def view_previous_results(self):
        self.show_banner()
        print("📊 PREVIOUS RESULTS")
        print("-" * 50)
        
        result_files = [f for f in os.listdir('.') if f.startswith('scan_results_')]
        
        if not result_files:
            print("❌ No previous results found!")
            input("Press Enter to continue...")
            return
        
        print("Available result files:")
        for i, file in enumerate(result_files, 1):
            print(f"{i}. {file}")
        
        try:
            choice = int(input(f"\nSelect file (1-{len(result_files)}): "))
            if 1 <= choice <= len(result_files):
                selected_file = result_files[choice - 1]
                self.show_file_contents(selected_file)
            else:
                print("❌ Invalid selection!")
        except ValueError:
            print("❌ Please enter a valid number!")
        
        input("Press Enter to continue...")
    
    def show_file_contents(self, filename):
        try:
            with open(filename, 'r') as f:
                content = f.read()
            print(f"\n📄 Contents of {filename}:")
            print("=" * 50)
            print(content)
            print("=" * 50)
        except Exception as e:
            print(f"❌ Error reading file: {e}")
    
    def show_scan_summary(self, url, duration):
        print("\n" + "=" * 60)
        print("📊 SCAN SUMMARY")
        print("=" * 60)
        print(f"🎯 Target: {url}")
        print(f"⏰ Duration: {duration:.2f} seconds")
        print(f"🔍 Paths tested: {self.total_tested}")
        print(f"✅ Admin panels found: {len(self.found_panels)}")
        print("=" * 60)
        
        if self.found_panels:
            print("\n📋 FOUND ADMIN PANELS:")
            for i, panel in enumerate(self.found_panels, 1):
                print(f"{i}. {panel}")
            
            # Save results
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"scan_results_{timestamp}.txt"
            
            with open(filename, 'w') as f:
                f.write("Admin Panel Scan Results\n")
                f.write("=" * 40 + "\n")
                f.write(f"Target: {url}\n")
                f.write(f"Time: {time.ctime()}\n")
                f.write(f"Duration: {duration:.2f}s\n")
                f.write(f"Paths tested: {self.total_tested}\n")
                f.write(f"Admin panels found: {len(self.found_panels)}\n\n")
                f.write("Found Panels:\n")
                for panel in self.found_panels:
                    f.write(f"- {panel}\n")
            
            print(f"\n💾 Results saved to: {filename}")
        else:
            print("\n❌ No admin panels found!")
        
        print("=" * 60)
        input("Press Enter to continue...")
    
    def show_multi_scan_summary(self, all_results):
        print("\n" + "=" * 60)
        print("📊 MULTI-SCAN SUMMARY")
        print("=" * 60)
        
        total_found = 0
        for url, panels in all_results.items():
            print(f"🎯 {url}: {len(panels)} panels found")
            total_found += len(panels)
            for panel in panels:
                print(f"   ✅ {panel}")
        
        print(f"\n📈 Total panels found: {total_found}")
        print("=" * 60)
        input("Press Enter to continue...")
    
    def show_custom_scan_summary(self, url, total_paths):
        print("\n" + "=" * 60)
        print("📊 CUSTOM SCAN SUMMARY")
        print("=" * 60)
        print(f"🎯 Target: {url}")
        print(f"🔍 Custom paths tested: {total_paths}")
        print(f"✅ Admin panels found: {len(self.found_panels)}")
        
        if self.found_panels:
            print("\n📋 FOUND ADMIN PANELS:")
            for i, panel in enumerate(self.found_panels, 1):
                print(f"{i}. {panel}")
        else:
            print("\n❌ No admin panels found!")
        
        print("=" * 60)
        input("Press Enter to continue...")
    
    def run(self):
        while True:
            self.show_menu()
            
            try:
                choice = input("Select option (1-5): ").strip()
                
                if choice == '1':
                    self.scan_single_url()
                elif choice == '2':
                    self.scan_multiple_urls()
                elif choice == '3':
                    self.custom_wordlist_scan()
                elif choice == '4':
                    self.view_previous_results()
                elif choice == '5':
                    print("\n👋 Thank you for using Admin Panel Scanner!")
                    print("Coded by darkboss1")
                    break
                else:
                    print("❌ Invalid choice! Please select 1-5.")
                    input("Press Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n\n❌ Scan interrupted by user!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                input("Press Enter to continue...")

if __name__ == "__main__":
    try:
        scanner = AdminPanelScanner()
        scanner.run()
    except KeyboardInterrupt:
        print("\n\n👋 Tool closed by user!")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
