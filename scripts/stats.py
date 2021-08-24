import sys
from collections import Counter
from pathlib import Path

import numpy as np


fn = sys.argv[1]


# DETERMINE CLASSES:
classes = set()
with Path(fn).open() as f:
    for line in f:
        if not len(line.strip()):
            continue
        token, yg, yp = line.strip().split()
        classes.add(yg)
        classes.add(yp)
tag2idx = {item: i for i, item in enumerate(sorted(list(classes)))}


# READ AND COUNT:
cnt = {item: Counter() for item in tag2idx.keys()}
with Path(fn).open() as f:
    for i, line in enumerate(f):
        # if line == '\n':
        #     continue
        [token, gold, pred] = line.strip().split()
        goldclass = gold  # .split('-')[-1]
        predclass = pred  # .split('-')[-1]
        if predclass == goldclass:
            cnt[predclass]['truepositive'] += 1
        elif predclass != goldclass:
            cnt[predclass]['falsepositive'] += 1
            cnt[goldclass]['falsenegative'] += 1
size = i + 1


# CALCULATE METRICS:
for (clas, counter) in cnt.items():
    cnt[clas]['pr'] = counter['truepositive']*100 / (counter['truepositive'] + counter['falsepositive']) if (counter['truepositive'] + counter['falsepositive']) != 0 else 0
    cnt[clas]['rc'] = counter['truepositive']*100 / (counter['truepositive'] + counter['falsenegative']) if (counter['truepositive'] + counter['falsenegative']) != 0 else 0
    cnt[clas]['f1'] = 2 * cnt[clas]['pr'] * cnt[clas]['rc'] / (cnt[clas]['pr'] + cnt[clas]['rc']) if (cnt[clas]['pr'] + cnt[clas]['rc']) != 0 else 0
    cnt[clas]['gold'] = counter['truepositive'] + counter['falsenegative']
    cnt[clas]['pred'] = counter['truepositive'] + counter['falsepositive']


# CALCULATE MACRO AND MICRO AVERAGES:
macro = Counter()
for field in 'pr rc f1 gold pred'.split():
    macro[field] = np.average([v[field] for k, v in cnt.items() if k != 'O'])

micro_avg = np.sum([counter['truepositive']*100 for clas, counter in cnt.items()]) / size
micro = {key: micro_avg for key in "pr rc f1".split()}
micro.update({key: macro[key] for key in "gold pred".split()})


# PRINT:
print('BelgeTürü PR RC F1 Gold Pred')
for k, v in sorted(cnt.items()):
    # if k == 'O':
    #     continue
    print('{}'.format(k), end=' ', flush=True)
    print(' '.join([str(round(v[field], 2)) for field in 'pr rc f1 gold pred'.split()]))

print('MACRO', end=' ', flush=True)
print(' '.join([str(round(macro[field], 2)) for field in 'pr rc f1 gold pred'.split()]))
print('MICRO', end=' ', flush=True)
print(' '.join([str(round(micro[field], 2)) for field in 'pr rc f1 gold pred'.split()]))

