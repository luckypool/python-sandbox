from shosetsu import Novel

from natto import MeCab
novel = Novel("n1839bd")
paragraph = novel.episodes[0].content.paragraph

nm = MeCab()
print(nm.parse('ピンチの時には必ずヒーローが現れる。'))

import pdb; pdb.set_trace()

print('hi')


