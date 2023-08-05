class Coder:
	def __init__(self):
		self.chars = [
			'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e',
			'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
			'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
			'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
			'Y', 'Z', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-',
			'.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
			'{', '|', '}', '~', ' ', '\t', '\n', '\r', '\x0b', '\x0c'
		]

		self.chars_special = ["Ä", "Ö", "Ü", "ä", "ö", "ü", "ß"]

	def encode(self, string):
		res = []
		for i in string:
			if i not in self.chars_special:
				mov = f"n{self.chars.index(i)}"
			else:
				mov = f"ns{self.chars_special.index(i)}"
			res.append(mov)

		res = "".join(res)
		return res

	def decode(self, string):
		split = string.split("n")
		dec = ""
		del split[0]

		for i in split:
			if "s" not in i:
				dec += self.chars[int(i)]
			else:
				dec += self.chars_special[int(i.replace("s", ""))]

		return dec