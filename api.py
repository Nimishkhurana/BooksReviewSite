import requests
res = requests.get("https://www.goodreads.com/book/rshow_by_isbn.json", params={"key": "sm2j54RqyCDvbeHG2QBtw", "isbns": "9780070669079"})
print(res)
