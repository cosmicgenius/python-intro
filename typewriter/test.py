import os
cwd = os.getcwd()

print(cwd)

for stuff in os.walk(cwd):
    print(stuff)
