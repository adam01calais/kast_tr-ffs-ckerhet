fst_fibonacci = 1
snd_fibonacci = 1
fibonacci = [fst_fibonacci, snd_fibonacci]
for i in range(2,10):
    temp = fst_fibonacci
    fst_fibonacci = snd_fibonacci
    snd_fibonacci = fst_fibonacci + temp  
    fibonacci.append(snd_fibonacci)
#kommentar

print(fibonacci)