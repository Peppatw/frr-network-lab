
nums = ["a","a","a","b","b","c","d","d","d","d",]
k = 2
count = {}
for i in nums:
     if i not in count:
        count[i] = 0
     count[i] += 1
pairs = []
for ch, c in count.items():
    pairs.append((c, ch))
pairs.sort(reverse=True)

result = []
for i in range(k):
    result.append(pairs[i][1])
print(result)