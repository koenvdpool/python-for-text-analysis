import os
from utils import get_paths, get_basic_stats

# calling the function ans assigning the resulted list to the variable get_paths_books
get_paths_books = get_paths("../Data/books")

# print the result to test exercise 1
print(f"Exercise 1: {get_paths_books}")
print()

# initialize empty dictionary
book2stats = {}

# looping over list of text files
for book_path in get_paths_books:
    
    # getting the name of the book
    basename = os.path.basename(book_path)
    book = basename.split('.')[0]
    
    # getting the statistics of the book
    book_stats = get_basic_stats(book_path)
    
    # print the statistics of the book to test exercise 2
    print(f"Exercise 2 and 4: {book} - {book_stats}")
    
    # updating book2stats
    book2stats[book] = book_stats

print()

# initialize empty dictionary
stats2book_with_highest_value = {}

# looping over the unpacked items of book2stats
for book, stats_of_book in book2stats.items():

    # looping over the unpacked items of stats_of_book
    for stat, value in stats_of_book.items():
        # as the top_30_token is not a quantitative statistic, we do not want to add it to the dictionary
        if stat == 'top_30_tokens':
            # instead, if we reach the stat top_30_tokens, we add the elements to a file for exercise 4
            with open(f"top_30_{book}.txt", "w") as outfile:
                for item in value:
                    outfile.write(f"{item}\n")
            # after adding to the file, we continue to the next iteration
            continue
        # if the stat is not yet in the dictionary, add it
        if stat not in stats2book_with_highest_value:
            stats2book_with_highest_value[stat] = book
        else:
            # assigning the name of the current book with the highest value to a variable
            name_book_highest_value = stats2book_with_highest_value[stat]

            # assigning the current highest value to the variable current_highest_value
            current_highest_value = book2stats[name_book_highest_value][stat]

            # checking if the value is higher than the current highest value
            if value > current_highest_value:
                # if yes, modify the dictionary
                stats2book_with_highest_value[stat] = book

# print the dictionary test exercise 3
print(f"Exercise 3: {stats2book_with_highest_value}")
