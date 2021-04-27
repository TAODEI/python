def a():
    a1 = 1
    a2 = 2
    print(a1, a2)
    swag(a1, a2)
    print(a1, a2)

def swag(a1, a2):
    a1, a2 = a2, a1
    print(a1, a2)
a()