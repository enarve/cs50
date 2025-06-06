from cs50 import get_string
text = get_string("Text: ")

words = len(text.split(" "))
letters = 0
sentences = 0
for c in text:
    if c.isalpha():
        letters += 1
for c in text:
    if c in [".", "!", "?"]:
        sentences += 1

l = 100 * letters / words
s = 100 * sentences / words
index = round(0.0588 * l - 0.296 * s - 15.8)
if index < 1:
    print("Before Grade 1")
elif index >= 16:
    print("Grade 16+")
else:
    print(f"Grade {index}")
