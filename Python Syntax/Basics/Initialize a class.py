class human:
    def __init__(self, name):
        self.name = name

    def greet(self):
        print(f"Hi, my name is {self.name}")

p1 = human("Timothy")
print(p1.name)
print(p1.greet())