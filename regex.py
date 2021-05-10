import re

text = "temperature girl"

pattern = re.compile("[a-zA-Z]+\s[a-zA-Z]+")

result = pattern.search(text)
print(result)