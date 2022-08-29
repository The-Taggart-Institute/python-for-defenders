"""
🎵 Your password must be... 🎵

🎵 Longer than eight characters 🎵

🎵 But not just alphabetical 🎵

🎵 Be sure to use a capital 🎵

🎵 And digits would be radical 🎵

🎵 And for that extra dash of strength 🎵

🎵 Use symbols to extend the length 🎵

🎵 If you follow these few simple rules 🎵

🎵 Your password won't be guessed by fools 🎵

🎵 And that's the password song!🎵
"""

pw_tests = {
    "should pass": "AbCdefgHijkL1234!",
    "length": "abc123",
    "mixed case": "abc12345ksla",
    "digits": "AbCdefgHijkL",
    "symbols": "AbCdefgHijkL134",
    
}

def testme(pw_func):
    for t in pw_tests:
        pw = pw_tests[t]
        if t == "should pass":
            print("[+] Testing known good password")
            if pw_func(pw):
                print("[+] Good password validates")
            else:
                print("[-] Good password fails validation")
        else:
            print(f"[+] Testing validation for {t}")
            if pw_func(pw):
                print(f"[-] Password validated without {t}")
            else:
                print(f"[+] Password failed validation without {t}")