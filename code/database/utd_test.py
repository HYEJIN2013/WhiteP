import csv
from modeling.run_model.GrowthModelUrbanTreeDatabase import _formulas

w = csv.writer(self.stdout)
results = []

for itree_region, otm_codes in _formulas.iteritems():
    for otm_code, fn in otm_codes.iteritems():

        key = '{} {}'.format(itree_region, otm_code)

        lo = float('inf')
        hi = -float('inf')

        for i in range(-10, 54):
            try:
                diameter = fn(i)
                lo = min(lo, diameter)
                hi = max(hi, diameter)
            except ValueError:
                pass

        results.append({
            'key': key,
            'lo': lo,
            'hi': hi,
        })

results = sorted(results, key=lambda item: item['lo'])
for item in results:
    w.writerow([item['key'], item['lo'], item['lo'], item['hi'], item['hi']])
