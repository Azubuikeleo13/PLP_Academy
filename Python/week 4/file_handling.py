"""A program that reads a file and writes to a
new file the modified content
"""

file_name = str(input("Enter file name..? "))

try:
    with open(file_name, 'r') as f:
        content = f.read()
except FileNotFoundError:
    print(f"File: {file_name} not found. Cross Check file name")
except:
    print("An error occured.")

with open("output.txt", 'w') as f:
    f.write(content)
