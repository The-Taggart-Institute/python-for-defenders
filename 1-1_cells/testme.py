def testme(whiz):
    try:
        print(whiz)
        if whiz == "Bang!":
            print("Congrats! You did it!")
        else:
            print(f"Hmm. {whiz} isn't quite the value I'm looking for...")
    except ValueError:
        print("Uh-oh. Did whiz get defined?")