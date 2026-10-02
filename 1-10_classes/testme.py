def testme(svc_acct, cls, parent):
    
    print("[+] Testing for class inheritance")
    if isinstance(svc_acct, parent):
      print("[+] object is a User")
    else:
      print("[-] object is not a User! It needs to inherit from that parent class!")
      return
    print("[+] Testing for ServiceAccountnesss")
    if isinstance(svc_acct, cls):
      print("[+] object is a ServiceAccount")
    else:
      print("[-] object is not a ServiceAccount!")
      return
    
    print("[+] Testing for password policy")
    
    try:
      password = svc_acct.password
      print("[+] Testing password length...", end="")
      if cls.validate_password("A"*29+"1!"):
        print("Failed")
        return
      print("Succeeded")
      print("[+] Testing password case...", end="")
      if cls.validate_password("a"*32 + "1!"):
        print("Failed")
        return
      print("Succeeded")
      print("[+] Testing Numbers...", end="")
      if cls.validate_password("Aa" * 16 + "!"):
        print("Failed")
        return
      print("Succeeded")
      print("[+] Testing Special Characters...", end="")
      if cls.validate_password("Aa" * 16 + "1"):
        print("Failed")
        return
      print("Succeeded")
      print("[+] Testing spaces...", end="")
      if cls.validate_password("Aa1!"*8 +" a"):
        print("Failed")
        return
      print("Succeeded")
      print("[+] All tests pass")
    except AttributeError:
        print("[!] Whoah! Did you make sure your class has a password?")
        return