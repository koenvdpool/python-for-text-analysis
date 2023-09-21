starting_num_bottles = 99  # the total number of bottles to start with

for bottles in range(starting_num_bottles, -1, -1):  # end range function at -1 to include 0 bottles
    remaining_num_bottles = bottles - 1
    # initialize text used for the majority of the verses
    text_bottles = "bottles"
    text_remaining_bottles = "bottles"
    key_sentence = "Take one down, pass it around,"  # the only sentence that changes in the last verse

    # change text accordingly to the current number of bottles
    if bottles == 2:
        text_remaining_bottles = "bottle"
    elif bottles == 1:
        text_bottles = "bottle"
        remaining_num_bottles = "no more"
    elif bottles == 0:  # change text accordingly for the special final verse
        bottles = "No more"
        key_sentence = "Go to the store and buy some more,"  # change key sentence
        remaining_num_bottles = starting_num_bottles  # change to inital number of bottles

    print(f"{bottles} {text_bottles} of beer on the wall,")
    print(
        f"{'no more' if bottles == 'No more' else bottles} {text_bottles} of beer.")  # get rid of capital letter in final verse
    print(f"{key_sentence}")
    print(f"{remaining_num_bottles} {text_remaining_bottles} of beer on the wall.")
    print()
