with open('typewriter/static/text.txt', 'r+') as f:
    f.seek(0)
    data = f.read()

    while True:
        a = input("A ")

        data += a

        print(data)
        f.write(a)
