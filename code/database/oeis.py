import re
import sys
import argparse
import requests


def main():
	parser = argparse.ArgumentParser(description="Search the OEIS database")
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument(
		'-s', '--sequence', nargs='+', type=int,
		help="Search for a sequence")
	mode.add_argument(
		"-i", "--id", type=str,
		help="retrive sequence by OEIS id")
	args = parser.parse_args()

	#Print first result for given id
	if args.id:
		payload = {"fmt": "text", "q": "id:" + sys.argv[2]}
		request = requests.get("http://oeis.org/search", params=payload)
		text = request.text.split("\n")[6:-2]

		print(args.id)
		for i, row in enumerate(text):
			row = re.sub("\(AT\)", "@", row)
			row = re.sub("<a href=\"(.+)\">(.+)</a>", "[\g<2>](\g<1>)", row)
			if text[i - 1][:2] != text[i][:2]:
				print(" ")
			print(row[11:])

	#Print results
	else:
		payload = {"fmt": "text", "q": ",".join(map(str, args.sequence))}
		request = requests.get("http://oeis.org/search", params=payload)
		print(request.text)
		text = request.text.split("\n\n")[2:-1]

		for sequence in text:
			sequence = sequence.split("\n")
			code = sequence[0][3::]
			for row in sequence:
				if row[:2] == "%N":
					print(row[3:10], "-", row[11:], sep=" ")
				break

if __name__ == "__main__":
	main()
