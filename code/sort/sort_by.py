def sort_by(self, criteria):
  keywords = list()
  for keyword, data in self.report.items():
    keywords.append((keyword, data[criteria]))
  return sorted(keywords, key=operator.itemgetter(1))

Adwords(report).sort_by("Clicks")
# =>[('Do Androids Dream of Electric Sheep? ', 109), ('science fiction books about time travel', 50), 
# ('science fiction books about space', 10), ('doctor who books', 8), ('I, Robot', 3)...]

Adwords(report).sort_by("Impressions")
# => [('science fiction books about the future', 1000),  ("The Hitchhiker's Guide to the Galaxy", 346), 
# ('science fiction books about robots', 152), ("The Hitchhiker's Guide to the Galaxy"', 100), ('I, Robot', 55), ...)
