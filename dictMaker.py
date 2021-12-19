with open("dict3.txt", "w") as fout:
    for i in range(97, 123):
        for ii in range(97, 123):
            for iii in range(97, 123):
                fout.write(f"{chr(i)}{chr(ii)}{chr(iii)}\n")
