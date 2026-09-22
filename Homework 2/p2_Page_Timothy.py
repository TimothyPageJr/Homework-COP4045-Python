# Timothy Page
# Homework 2 - Problem 2


# Part A
quadruples = [
    (a, b, c, d)
    for a in range(1, 11)
    for b in range(1, 11)
    for c in range(1, 11)
    for d in range(1, 11)
    if len({a, b, c, d}) == 4
    and a**2 + b**2 == c**2 + d**2
]


# Part B
words = ['One', 'SEVEN', 'three', 'two', 'Ten']

short_words = [
    (word.lower(), len(word))
    for word in words
    if len(word) < 5
]


# Part C
names = ['Christopher Ashton Kutcher', 'Elizabeth Stamatina Fey']

formatted_names = [
    f"{name.split()[0]} {name.split()[1][0]}. {name.split()[2]}"
    for name in names
]


# Part D
lst1 = ["Spam", "Trams", "Elbows", "Tops", "Astral"]
lst2 = ["Bowels", "Sample", "Altars", "Stop", "Course", "Smart"]

anagram_pairs = [
    (word1, word2)
    for word1 in lst1
    for word2 in lst2
    if sorted(word1.lower()) == sorted(word2.lower())
]


# Part E
s = ['one', 'two', 'three']

string_lengths = {
    word: len(word)
    for word in s
}


# Part F
text = "Hello world"

vowels = {
    index: character
    for index, character in enumerate(text)
    if character.lower() in "aeiou"
}



print("Timothy Page Problem 2")

print("\nPart A:")
print(quadruples)

print("\nPart B:")
print(short_words)

print("\nPart C:")
print(formatted_names)

print("\nPart D:")
print(anagram_pairs)

print("\nPart E:")
print(string_lengths)

print("\nPart F:")
print(vowels)