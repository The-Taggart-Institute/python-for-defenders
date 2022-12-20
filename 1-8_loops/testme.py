from random import sample, shuffle

# Load Files
with open("names.txt") as f:
    names = [l.strip() for l in f.readlines()]
    
with open("rockyou-50.txt") as f:
    pws = [l.strip() for l in f.readlines()]

# Constants
NUM_DUMPS = 500
NUM_ACCTS = 200
PCT_CORRECT = 0.1


# Build accounts
acct_users = sample(names, NUM_ACCTS)
acct_pws = sample(pws, NUM_ACCTS)
accounts = {acct_users[i]:acct_pws[i] for i in range(NUM_ACCTS)}

# Build cred dump
account_samples = sample(acct_users, round(NUM_ACCTS * PCT_CORRECT))
dump_users = sample(names, NUM_DUMPS) + account_samples
dump_pws = sample(pws, NUM_DUMPS) + [accounts[p] for p in account_samples]
cred_dump = list(zip(dump_users, dump_pws))
shuffle(cred_dump)

def authenticate(username, password) -> (bool, str):
    if username in accounts:
        if password == accounts[username]:
            return (True, "")
        return (False, "Password is incorrect")
    return (False, "Username does not exist")


def testme_1(valid_users):
    real_users = list(filter(lambda u: u in accounts, dump_users))
    try:
        if sorted(valid_users) == sorted(real_users):
            print("[+] Valid users matched!")
        else:
            print("[-] Valid users do not match!")
    except Error as e:
        print(e)

def testme_2(test_authed):
    true_authed = [a[0] for a in list(filter(lambda d: authenticate(d[0], d[1])[0], cred_dump))]
    try:
        if sorted(true_authed) == sorted(test_authed):
            print("[+] Authenticated users matched!")
        else:
            print("[-] Authenticated users do not match!")
    except Error as e:
        print(e)
