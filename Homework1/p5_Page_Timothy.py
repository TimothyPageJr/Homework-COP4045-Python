import string


def caesar_cipher(text, shift):
	"""Return text encrypted with a Caesar cipher."""
	encrypted_text = ""

	for character in text:
		if character.isupper():
			alphabet = string.ascii_uppercase
			old_index = alphabet.index(character)
			new_index = (old_index + shift) % len(alphabet)
			encrypted_text += alphabet[new_index]
		elif character.islower():
			alphabet = string.ascii_lowercase
			old_index = alphabet.index(character)
			new_index = (old_index + shift) % len(alphabet)
			encrypted_text += alphabet[new_index]
		else:
			encrypted_text += character

	return encrypted_text


def caesar_decipher(cyphertext, shift):
	"""Return the original text by reversing a Caesar cipher."""
	return caesar_cipher(cyphertext, -shift)


def letter_frequency(text):
	"""Return the number of times each letter A-Z appears in text."""
	frequencies = {}

	for letter in string.ascii_uppercase:
		frequencies[letter] = 0

	for character in text:
		if character.isalpha():
			uppercase_character = character.upper()
			if uppercase_character in frequencies:
				frequencies[uppercase_character] += 1

	return frequencies


def main():
	message = ""
	shift = 0
	encrypted_text = ""

	while True:
		print("\nCaesar Cipher Menu")
		print("1. Enter a message")
		print("2. Enter a shift value")
		print("3. See the encrypted text")
		print("4. See the letter-frequency breakdown")
		print("5. See the decrypted text")
		print("6. Quit")

		choice = input("Choose an option: ")

		if choice == "1":
			message = input("Enter a message: ")
			encrypted_text = caesar_cipher(message, shift)
		elif choice == "2":
			shift = int(input("Enter a shift value: "))
			encrypted_text = caesar_cipher(message, shift)
		elif choice == "3":
			encrypted_text = caesar_cipher(message, shift)
			print("Encrypted text:", encrypted_text)
		elif choice == "4":
			frequencies = letter_frequency(message)
			for letter in frequencies:
				print(letter + ":", frequencies[letter])
		elif choice == "5":
			encrypted_text = caesar_cipher(message, shift)
			print("Decrypted text:", caesar_decipher(encrypted_text, shift))
		elif choice == "6":
			print("Goodbye!")
			break
		else:
			print("Please choose a number from 1 to 6.")


if __name__ == "__main__":
	main()
