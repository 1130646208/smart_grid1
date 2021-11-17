# -- coding: utf-8 --
# 数据清洗，对比家庭中电器的异同

sets = []
with open('数据集/多个家庭/电器对比.csv') as f:
    while True:
        line = f.readline()
        s = set()
        if not line:
            break
        for t in line.split(','):
            if len(t.strip()) > 2:
                s.add(t.strip())
        sets.append(s)


res = []
for a in range(0, len(sets)-1):
    for b in range(a+1, len(sets)):
        r = sets[a] & sets[b]
        res.append((len(r), a+1, b+1, r))

watch = sorted(res, key=lambda x: x[0], reverse=True)
for each in watch:
    print(each)
