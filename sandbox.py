v = {}
for i in range(int(input())):
    N, *a = input().split()
    R, S, D = map(int, a)
    v[N] = 2*R+3*S+D
hello = sorted(v, key=v.get, reverse=True)
mv = 0
for i in hello:
    mv = max(v[i], mv)
count = 0
for i in hello:
    if v[i] == mv:
        count += 1
if len(v) == 1:
    print(hello[0])
elif count >= 2:
    s = []
    for i in hello:
        if v[i] == mv:
            s.append(i)
    s.sort()
    print(s[0])
    print(s[1])
else:
    print(hello[0])
    print(hello[1])
