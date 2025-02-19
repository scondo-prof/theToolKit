import random
import sys


def dyslexic_dance(input_str: str) -> str:
    """Shuffles the characters in the input string randomly."""
    input_list = list(input_str)
    random.shuffle(input_list)
    return "".join(input_list)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python dyslexic_dance.py '<your-text>'")
        sys.exit(1)

    input_text = sys.argv[1]  # Get input from the command line argument
    shuffled_text = dyslexic_dance(input_text)
    print(f"wild tuna: {shuffled_text}")
