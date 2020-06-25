import difflib

def main(fname):
    with open("list_bad.txt") as f:
        bad_ingredients = f.readlines()

    bad_ingredients = [x.strip().lower() for x in bad_ingredients]
    with open(fname) as f:
        to_check = f.readlines()
    to_check = [x.strip().lower() for x in to_check[0].split(',')]
    n = len(to_check)
    for index, ingredient in enumerate(to_check):
        close_options = difflib.get_close_matches(ingredient, bad_ingredients, cutoff=0.7)
        rank = (float(n - index) / n) * 100
        if len(close_options) > 0:
            print('{ingredient} | Rank = {rank}%'.format(ingredient=ingredient.capitalize(), rank=rank))
            print('{close_options}\n'.format(close_options=close_options))
if __name__ == '__main__':
    fname = "./check.txt"
    main(fname)