def pyramid(rows):
    for i in range(1, rows + 1):
        yield "*" * i

for line in pyramid(9):
    print(line)
