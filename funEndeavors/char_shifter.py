import sys


def new_char(input_char_integer: int, shifter: int, shift: bool) -> chr:
    valid_char_integers = [
        48,
        49,
        50,
        51,
        52,
        53,
        54,
        55,
        56,
        57,
        65,
        66,
        67,
        68,
        69,
        70,
        71,
        72,
        73,
        74,
        75,
        76,
        77,
        78,
        79,
        80,
        81,
        82,
        83,
        84,
        85,
        86,
        87,
        88,
        89,
        90,
        97,
        98,
        99,
        100,
        101,
        102,
        103,
        104,
        105,
        106,
        107,
        108,
        109,
        110,
        111,
        112,
        113,
        114,
        115,
        116,
        117,
        118,
        119,
        120,
        121,
        122,
    ]

    if input_char_integer in valid_char_integers:
        index = 0
        for char_integer in valid_char_integers:
            if input_char_integer == char_integer:
                break
            index += 1

        if shift:
            new_char_index = index + shifter
        else:
            new_char_index = index - shifter
        new_char = chr(valid_char_integers[new_char_index % 62])

        return new_char
    else:
        return chr(input_char_integer)


def char_shifter(input_str: str, shifter: int, shift: bool) -> str:
    """Shifts the characters in the input string the amount of chars in the second input."""
    shifted_text = ""
    for char in input_str:
        shifted_text += new_char(
            input_char_integer=ord(char), shifter=shifter, shift=shift
        )

    return shifted_text


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python char_shifter.py '<input_string>' '<shifter-int>' '<1/0>'")
        sys.exit(1)

    input_str = sys.argv[1]
    shifter = int(sys.argv[2])
    shift = int(sys.argv[3])

    if shift == 0:
        shift = False
        shifted_text = char_shifter(input_str=input_str, shifter=shifter, shift=shift)
        print(shifted_text)
    elif shift == 1:
        shift = True
        shifted_text = char_shifter(input_str=input_str, shifter=shifter, shift=shift)
        print(shifted_text)
    else:
        print("Argument in space 3 must be either 1 || 0")
