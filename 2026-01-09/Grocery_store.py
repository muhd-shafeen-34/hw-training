inventory = {"apple" : 50.50,
             "orange" : 45.50,
             "chips": 60.50,
             "tomato" : 45.5,
             "potato" : 30.5}

cart = ["apple","orange","chips","tomato","potato","potato","egg"]

print(type(inventory))

print(type(cart))

print(type(inventory["apple"]))

total_bill = 0

for i in cart:
    if i in inventory:
        total_bill = total_bill + inventory[i]
    else:
        print("selected item: ",i," is not available in the inventory please select another item")
        continue
print(total_bill)

cart = set(cart)

print(cart)

product_categories = ("fruits", "bakery", "vagetable")

print(product_categories)

inventory["banana"] = None

is_discount_applied = False

if total_bill > 100:
    is_discount_applied = True

print(is_discount_applied)
 



