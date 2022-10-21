import os

def testme():
    # Check to see if the file exists
    print("[+] Making sure we have indicator.py")
    try:
        os.stat("indicator.py")
        print("[+] Module found")
    except FileNotFoundError:
        print("[!] Hey what gives?! I don't even have an indicator.py file!")
        return
    
    # Import the stuff we want
    print("[+] Importing our classes")
    try:
        from indicator import URLIndicator, DomainIndicator, IPv4Indicator
    except ImportError as e:
        print(f"[!] {e}")
        return
    
    # Make sane indicators
    print("[+] Making IP indicator")
    try:
        bad_ip = IPv4Indicator("192.168.99.1")
        print(f"[+] {bad_ip.defang()}")
    except:
        print("[!] Couldn't make/defang IP indicator!")
        return
        
    print("[+] Making domain indicator")
    try:
        bad_domain = DomainIndicator("evil.com")
        print(f"[+] {bad_ip.defang()}")
    except:
        print("[!] Couldn't make/defang domain indicator!")
        return
        
    print("[+] Making URL indicator")
    try:
        bad_url = URLIndicator("https://taggart-tech.com")
        print(f"[+] {bad_url.defang()}")
    except:
        print("[!] Couldn't make/defang URL indicator!")
        return
        
        
    

    
    