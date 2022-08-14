crew = [
    "Shepard",
    "Joker",
    "Garrus",
    "Liara",
    "Chakwas"
]

def testme_1(data):
    print("[+] Testing initial crew...")
    if sorted(data) == sorted(crew):
        print("[+] Crew assembled! Ready for launch!")
    else:
        print("[-] Hmm, the crew doesn't look quite right.")

def testme_2(data):
    print("[+] Testing expanded crew...")
    added = list(filter(lambda c: c not in crew, data))
    if all([c in data for c in crew]) and len(added) > 0:
        added_str = ", ".join(added)
        print(f"[+] Nice! You added {added_str}")
    else:
        print("[-] Hmm, the expanded crew doesn't look quite right.")
        
    pass

def testme_3(data):
    print("[+] Testing the 'revised' crew")
    removed = crew[:]
    removed.remove("Liara")
    if all([c in data for c in removed]) and "Liara" not in data:
        print("[+] Sorry to see you go, Liara.")
    else:
        print("[-] Uh-oh. Did you remember to remove Liara?")
