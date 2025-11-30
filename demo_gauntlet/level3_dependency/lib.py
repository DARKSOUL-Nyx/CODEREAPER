
def process_data(data):
    # This function is spaghetti, BUT its signature (data) is locked by dependency.
    res = []
    for i in data:
        if i > 5:
            res.append(i * 2)
    return res
