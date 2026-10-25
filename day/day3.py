words = ["apple", "banana", "apple", "orange", "banana", "apple"]
dict={}
for word in words:
    if word in dict:
        dict[word]+=1
    else:
        dict[word]=1
print(dict)