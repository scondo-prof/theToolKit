import random

def dyslexic_dance(input: str) ->str:
    
    dyslexic_string = ""
    input_list = list(input)

    for _ in range(len(input)):
        target_value = random.randint(0, len(input_list)-1)
        target = input_list[target_value]
        del input_list[target_value]
        dyslexic_string += target

    print(dyslexic_string)
    


dyslexic_dance("smacking-my-robust-rump")