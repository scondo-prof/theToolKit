import base64



def base_64_encode_utf8(string: str) -> str:
    # Encode the string to bytes, then to base64
    encoded_string = base64.b64encode(string.encode('utf-8'))

    # Convert the result back to a string for printing
    print(encoded_string.decode('utf-8'))


string = "We know that from time to time, there arise among human beings, people who seem to exude love as naturally as the sun gives out heat."

base_64_encode_utf8(string=string)
