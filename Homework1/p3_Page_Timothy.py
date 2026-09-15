def find_dup_str(s, n):
    for i in range(len(s) - n + 1):
        current = s[i:i+n]

        for j in range(i + n, len(s) - n + 1):
            if current == s[j:j+n]:
                return current

    return ""

s = input("Enter a string: ")
n = int(input("Enter substring length: "))

result = find_dup_str(s, n)
print(result)

def find_max_dup(s):
    longest = ""

    for length in range(1, len(s) // 2 + 1):
        duplicate = find_dup_str(s, length)

        if duplicate != "":
            longest = duplicate

    return longest

s = input("Enter a string: ")

result = find_max_dup(s)

print(result)