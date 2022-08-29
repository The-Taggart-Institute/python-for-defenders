def testme(evil_url, indicator_class, url_indicator_class):
    
    print("[+] Testing for class inheritance")
    if isinstance(evil_url, indicator_class):
        print("[+] object is an Indicator")
    else:
        print("[-] object is not an Indicator! It needs to inherit from that parent class!")
        return
    print("[+] Testing for URLIndicatorness")
    try:
        if isinstance(evil_url, url_indicator_class):
            print("[+] object is a URLIndicator")
        else:
            print("[-] object is not a URLIndicator!")
            return
    except:
        print("[!] Whoah! Did you make sure your class is named correctly?")
        return
    
    print("[+] Testing for defanging")
    
    try:
        if evil_url.defang() == evil_url.value.replace("http","hxxp").replace(".","[.]"):
            print("[+] Defanging successful!")
        else:
            print("[-] Defanging didn't seem to work.")
    except:
        print("[!] Whoah! Did you make sure your class has a defang method?")
        return
        