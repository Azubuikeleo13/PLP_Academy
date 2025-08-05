"""A Conditional Function that applies  discount on price of goods
- Take two argument
- @price - Price of goods
- @discount - Discount on goods
- returns new price of goods if discount is above 20% or old price if below.
"""

def calculate_discount(price, discount_percent):
    
    # Return calculated discount price.
    return price if discount_percent < float(20) else price * ((100 - discount_percent) / 100)

price = float(input("Enter the prize of goods >>> "))
discount_percent = float(input("Enter discount percentage >>> "))

actual_price = calculate_discount(price, discount_percent)

print(f"Price: {actual_price}")
