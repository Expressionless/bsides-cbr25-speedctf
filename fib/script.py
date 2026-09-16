enc = [64, 80, 76, 76, 72, 70, 16, 7, 107, 165, 200]

curr = 1
prev = 1
tmp = 0

tmp_password = [0] * 11
for i in range(11):
    tmp = curr;
    curr += prev;
    prev = tmp;
    tmp_password[i] = enc[i] ^ curr;

print([chr(x) for x in tmp_password])
