def testme_1(data):
    print("[+] Testing for floatiness...")
    if type(data) == float:
        print(f"[+] {data} is a float!")
    else:
        print(f"[!] {data} is not a float!")

def testme_2(x, y):
    print("[+] Testing for modiness...")
    if x % y == 5:
        print(f"[+] Success! {x} % {y} is 5!")
    else:
        print(f"[!] Hmm, {x} % {y} does not yield a remainder of 5...")