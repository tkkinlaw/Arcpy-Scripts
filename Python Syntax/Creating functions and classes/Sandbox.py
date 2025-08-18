import MyFunctions, MyClasses

person = MyClasses.Person("Tim")

result = MyFunctions.Greeting(person.name)
print(result)

result = MyFunctions.Goodbye(person.name)
print(result)