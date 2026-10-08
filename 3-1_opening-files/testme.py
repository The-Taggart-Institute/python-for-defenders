names_1_test = [
    "Charles",
    "Scott",
    "Jean",
    "Logan",
    "Ororo",
    "Remy"
]

names_2_test = [
    "Clark",
    "Bruce",
    "Diana",
    "Arthur",
    "Kendra",
]

names_3_test = [
    "Oliver",
    "Laurel",
    "Dinah",
    "John",
    "Barry",
    "Felicity"
]

with open("names_2.txt") as f:
    names_2_test = [l.strip() for l in f.readlines()]

with open("names_3.txt") as f:
    names_3_test = [l.strip() for l in f.readlines()]
        

def testme_1():
    try:
        with open("names_1.txt") as f:
            print("[+] names_1.txt found!")
            names_1 = [n.strip() for n in f.readlines()]
            if names_1_test == names_1:
                print("[+] File contents match!")
            else:
                print("[-] File contents don't match the names")
    except:
        print("[!] names_1.txt not found!")
        
def testme_2(names_2_user):
    
    if names_2_test == names_2_user:
        print("[+] File contents match!")
    else:
        print("[-] File contents don't match the names")


def testme_3():
    with open("names_3.txt") as f:
        names_3_appended = [l.strip() for l in f.readlines()]
    if sorted(names_1_test + names_2_test + names_3_test) == sorted(names_3_appended):
         print("[+] File contents match!")
    else:
        print("[-] File contents don't match the names")
        
def reset():
    with open("names_1.txt", "w") as f:
        f.write("\n".join(names_1_test))

    with open("names_2.txt", "w") as f:
        f.write("\n".join(names_2_test))
    
    with open("names_3.txt", "w") as f:
        f.write("\n".join(names_3_test))
        f.write("\n")