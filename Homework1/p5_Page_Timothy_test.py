import unittest

from p5_Page_Timothy import caesar_cipher, caesar_decipher, letter_frequency


class TestCaesarCipher(unittest.TestCase):
	def test_caesar_cipher_shifts_uppercase_and_lowercase(self):
		self.assertEqual(caesar_cipher("Abc Xyz", 3), "Def Abc")

	def test_caesar_cipher_preserves_spaces_and_punctuation(self):
		self.assertEqual(caesar_cipher("Hello, World!", 2), "Jgnnq, Yqtnf!")

	def test_caesar_cipher_wraps_at_end_of_alphabet(self):
		self.assertEqual(caesar_cipher("Zz", 1), "Aa")

	def test_caesar_decipher_returns_original_text(self):
		encrypted_text = caesar_cipher("Meet me at 5!", 7)
		self.assertEqual(caesar_decipher(encrypted_text, 7), "Meet me at 5!")

	def test_letter_frequency_ignores_case_and_non_letters(self):
		frequencies = letter_frequency("Apple pie! A1")

		self.assertEqual(frequencies["A"], 2)
		self.assertEqual(frequencies["P"], 3)
		self.assertEqual(frequencies["E"], 2)
		self.assertEqual(frequencies["I"], 1)
		self.assertEqual(frequencies["Z"], 0)


if __name__ == "__main__":
	unittest.main()
