#basic data types
name = "John"
age = 19
maths = 30.5
english = 45.5
hindi = 50.5
marks = [maths, english, hindi]
details = {"Name" : name,
           "Age" : age,
           "Marks": marks}
remarks = None 

print(type(name))
print(type(age))
print(type(english))
print(type(marks))
print(type(details))

#basic math operations

total_marks = maths + english + hindi
average_marks = total_marks / 3

#if condition statement

if average_marks >= 40:
    is_passed = True
else:
    is_passed = False
print(is_passed)
#basic For loop  

for i in marks:
    print(i)

marks = set(marks)
print(marks)

subject_names = ("maths", "english", "hindi")

print(subject_names)

print(type(is_passed))
print(type(remarks))

#student report

print("student report")
print("---------------------------")
for i,l in details.items():
    print(i," : ",l)
    print("Passed : ",is_passed)
