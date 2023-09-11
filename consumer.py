from worker import add

results = []
for i in range(100):
    result = add.delay(4, 4)
    results.append(result)
