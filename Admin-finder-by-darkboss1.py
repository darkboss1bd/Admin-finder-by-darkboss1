#!/usr/bin/env python3
# Coded by darkboss1
# Improved version with enhanced error handling and more admin paths

import os
import sys
import requests
from time import sleep

def main():
    # Clear screen based on OS
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Check if URL argument is provided
    if len(sys.argv) != 2:
        print("Usage: python3 admin_scanner.py <target_url>")
        print("Example: python3 admin_scanner.py http://example.com")
        sys.exit(1)
    
    url = sys.argv[1].rstrip('/')  # Remove trailing slash if present
    
    # Admin panel paths list (integrated all paths)
    admin_paths = [
        "/0admin/", "/0manager/", "/aadmin/", "/acceso.php", "/acceso.asp", 
        "/acceso.html", "/access.php", "/access.asp", "/access.html", "/access/", 
        "/account.asp", "/account.html", "/account.php", "/accounts/", "/acct_login/", 
        "/adm.php", "/adm.asp", "/adm.html", "/adm/", "/adm_user", "/admusr", 
        "/admin1.asp", "/admin1.htm", "/admin1.html", "/admin1.php", "/admin1/", 
        "/admin2.asp", "/admin2.html", "/admin2.php", "/admin4_account/", 
        "/admin4_colon/", "/admin.asp", "/admin.htm", "/admin.html", "/admin.php", 
        "/admin/", "/admin/account.asp", "/admin/account.html", "/admin/account.php", 
        "/admin/adminLogin.htm", "/admin/adminLogin.html", "/admin/controlpanel.asp", 
        "/admin/controlpanel.htm", "/admin/controlpanel.html", "/admin/controlpanel.php", 
        "/admin/cp.asp", "/admin/cp.html", "/admin/cp.php", "/admin/home.asp", 
        "/admin/home.php", "/admin/index.asp", "/admin/index.html", "/admin/index.php", 
        "/admin/login.asp", "/admin/login.htm", "/admin/login.html", "/admin/login.php", 
        "/admin_area/", "/admin_area.asp", "/admin_area.html", "/admin_area.php", 
        "/admin_area/admin.php", "/admin_area/admin.asp", "/admin_area/admin.html", 
        "/admin_area/login.php", "/admin_area/login.asp", "/admin_area/login.html", 
        "/adminArea", "/adminarea", "/adminarea.html", "/adminarea.php", 
        "/admincontrol.asp", "/admincontrol.html", "/admincontrol.php", "/admincontrol/", 
        "/admincp/", "/administer/", "/administr8.asp", "/administr8.html", 
        "/administr8.php", "/administr8/", "/administration.html", "/administration.php", 
        "/administration/", "/administrator.asp", "/administrator.html", 
        "/administrator.php", "/administrator/", "/administrator/account.asp", 
        "/administrator/account.html", "/administrator/account.php", 
        "/administrator/index.asp", "/administrator/index.html", "/administrator/index.php", 
        "/administrator/login.asp", "/administrator/login.html", "/administrator/login.php", 
        "/administratoraccounts/", "/administratorlogin.php", "/administratorlogin.asp", 
        "/administratorlogin.html", "/administratorlogin/", "/administrators.php", 
        "/administrators.asp", "/administrators.html", "/administrators/", 
        "/administrivia/", "/adminitem/", "/adminitems/", "/adminLogin/", 
        "/adminpanel.asp", "/adminpanel.html", "/adminpanel.php", "/adminpanel/", 
        "/adminpro/", "/admins.asp", "/admins.html", "/admins.php", "/admins/", 
        "/adminsite/", "/AdminTools/", "/admuser", "/admusr", "/auth.php", 
        "/auth.asp", "/auth.html", "/authadmin.php", "/authadmin.asp", "/authadmin.html", 
        "/authadmin/", "/authenticate.php", "/authenticate.asp", "/authenticate.html", 
        "/authenticate/", "/authentication.php", "/authentication.asp", 
        "/authentication.html", "/authentication/", "/authuser.php", "/authuser.asp", 
        "/authuser.html", "/autologin.php", "/autologin.asp", "/autologin.html", 
        "/autologin/", "/banneradmin/", "/bb-admin/", "/bb-admin/admin.php", 
        "/bb-admin/admin.html", "/bb-admin/login.asp", "/bbadmin/", "/bigadmin/", 
        "/blogindex/", "/cadmins/", "/ccp14admin/", "/cgi-bin/login", "/cmsadmin.php", 
        "/cmsadmin.asp", "/cmsadmin.html", "/cmsadmin/", "/control.php", "/control.asp", 
        "/control.html", "/control/", "/controlpanel.asp", "/controlpanel.html", 
        "/controlpanel.php", "/controlpanel/", "/cp.asp", "/cp.html", "/cp.php", 
        "/cp/", "/cpanel/", "/cpanel_file/", "/customer_login/", "/Database_Administration/", 
        "/database_administration/", "/dir-login/", "/directadmin/", "/ezsqliteadmin/", 
        "/fileadmin.asp", "/fileadmin.html", "/fileadmin.php", "/fileadmin/", 
        "/formslogin/", "/globes_admin/", "/hpwebjetadmin/", "/Indy_admin/", 
        "/irc-macadmin/", "/isadmin.php", "/isadmin.asp", "/isadmin.html", "/isadmin/", 
        "/kpanel/", "/letmein/", "/LiveUser_Admin/", "/log-in.php", "/log-in.asp", 
        "/log-in.html", "/log-in/", "/log_in.php", "/log_in.asp", "/log_in.html", 
        "/log_in/", "/login1/", "/login-redirect/", "/login-us/", "/login.admin.php", 
        "/login.asp", "/login.htm", "/login.html", "/login.php", "/login/", 
        "/login_admin.php", "/login_admin.asp", "/login_admin.html", "/login_admin/", 
        "/login_db/", "/login_user.php", "/login_user.asp", "/login_user.html", 
        "/login_user/", "/loginerror/", "/loginflat/", "/loginok/", "/loginsave/", 
        "/loginsuper/", "/logo_sysadmin/", "/Lotus_Domino_Admin/", "/macadmin/", 
        "/manage.php", "/manage.asp", "/manage.html", "/manage/", "/management.php", 
        "/management.asp", "/management.html", "/management/", "/manager.php", 
        "/manager.asp", "/manager.html", "/manager/", "/managment/admin", "/manuallogin/", 
        "/member.php", "/member.asp", "/member.html", "/member/", "/memberadmin.php", 
        "/memberadmin.asp", "/memberadmin.html", "/memberadmin/", "/members.php", 
        "/members.asp", "/members.html", "/members/", "/memlogin/", "/meta_login/", 
        "/modelsearch/login.asp", "/modelsearch/login.php", "/moderator.asp", 
        "/moderator.html", "/moderator.php", "/moderator/", "/moderator/admin.asp", 
        "/moderator/admin.html", "/moderator/admin.php", "/moderator/login.asp", 
        "/moderator/login.html", "/moderator/login.php", "/modules/admin/", "/myadmin/", 
        "/navSiteAdmin/", "/newsadmin/", "/openvpnadmin/", "/pages/admin/", 
        "/pages/admin/admin-login.php", "/pages/admin/admin-login.asp", 
        "/pages/admin/admin-login.html", "/panel-administracion/", 
        "/panel-administracion/login.php", "/panel-administracion/login.asp", 
        "/panel-administracion/login.html", "/panel.php", "/panel.asp", "/panel.html", 
        "/panel/", "/pgadmin/", "/phpldapadmin/", "/phpmyadmin/", "/phppgadmin/", 
        "/phpSQLiteAdmin/", "/platz_login/", "/power_user/", "/processlogin.php", 
        "/processlogin.asp", "/processlogin.html", "/processlogin.php/", 
        "/project-admins/", "/PSUser/", "/pureadmin/", "/pwadmin", "/radmind-1/", 
        "/radmind/", "/rcLogin/", "/relogin.asp", "/relogin.php", "/relogin.html", 
        "/relogin/", "/root/", "/secret/", "/secrets/", "/secure/", "/security/", 
        "/Server.asp", "/Server.html", "/Server.php", "/Server/", "/server/", 
        "/server_admin_small/", "/ServerAdministrator/", "/showlogin/", "/sign-in.php", 
        "/sign-in.asp", "/sign-in.html", "/sign-in/", "/sign_in.php", "/sign_in.asp", 
        "/sign_in.html", "/sign_in/", "/signin.php", "/signin.asp", "/signin.html", 
        "/signin/", "/simpleLogin/", "/siteadmin.php", "/siteadmin.asp", "/siteadmin.html", 
        "/siteadmin/", "/smblogin/", "/sql-admin/", "/ss_vms_admin_sm/", "/sshadmin/", 
        "/staradmin/", "/sub-login/", "/super1.php", "/super1.asp", "/super1.html", 
        "/super1/", "/super.php", "/super.asp", "/super.html", "/super/", "/Super-Admin/", 
        "/super_index.php", "/super_index.asp", "/super_index.html", "/super_index/", 
        "/super_login.php", "/super_login.asp", "/super_login.html", "/superman.php", 
        "/superman.asp", "/superman.html", "/superman/", "/supermanager.php", 
        "/supermanager.asp", "/supermanager.html", "/superuser.php", "/superuser.asp", 
        "/superuser.html", "/superuser/", "/supervise/", "/supervise/Login", 
        "/supervisor/", "/support_login/", "/sys-admin/", "/sys_user", "/sys_usr", 
        "/sysadm/", "/SysAdmin2/", "/sysadmin.asp", "/sysadmin.html", "/sysadmin.php", 
        "/SysAdmin/", "/sysadmin/", "/sysadmins/", "/system-administration/", 
        "/system_administration/", "/sysuser", "/sysusr", "/typo3/", "/ur-admin.asp", 
        "/ur-admin.html", "/ur-admin.php", "/ur-admin/", "/user/", "/useradmin/", 
        "/UserLogin/", "/users/", "/usr/", "/utility_login/", "/uvpanel/", "/vadmind/", 
        "/vmailadmin/", "/vorod/", "/vorud/", "/webadmin.asp", "/webadmin.html", 
        "/webadmin.php", "/WebAdmin/", "/webadmin/", "/webmaster/", "/wizmysqladmin/", 
        "/wp-admin/", "/wp-login.php", "/wp-login/", "/xlogin/", "/yonetici.asp", 
        "/yonetici.html", "/yonetici.php", "/yonetim.asp", "/yonetim.html", "/yonetim.php"
    ]

    print(f"Target URL: {url}")
    print("Starting Admin Panel Scanner...")
    print("=" * 50)
    
    found_panels = []
    
    try:
        for path in admin_paths:
            full_url = url + path
            try:
                # Add timeout and proper headers to avoid blocking
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                response = requests.get(full_url, headers=headers, timeout=10, verify=False)
                
                if response.status_code == 200:
                    print("=" * 50)
                    print(f"\033[92m[+] Admin panel found --> {full_url} \033[0m")
                    print("=" * 50)
                    found_panels.append(full_url)
                else:
                    print(f"\033[91m[-] Not found ({response.status_code}) --> {full_url} \033[0m")
                
                # Small delay to avoid overwhelming the server
                sleep(0.1)
                
            except requests.exceptions.RequestException as e:
                print(f"\033[93m[!] Error accessing {full_url}: {str(e)} \033[0m")
                continue
            except KeyboardInterrupt:
                print("\n\033[91m[!] Scan interrupted by user \033[0m")
                break
    
    except Exception as e:
        print(f"\033[91m[!] Unexpected error: {str(e)} \033[0m")
    
    # Print summary
    print("\n" + "=" * 50)
    print("SCAN SUMMARY")
    print("=" * 50)
    if found_panels:
        print(f"\033[92m[+] Found {len(found_panels)} admin panel(s):\033[0m")
        for panel in found_panels:
            print(f"  - {panel}")
    else:
        print("\033[91m[-] No admin panels found \033[0m")
    print("=" * 50)

if __name__ == "__main__":
    main()
