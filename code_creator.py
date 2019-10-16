import requests


while True:
    print(requests.post("http://127.0.0.1:8080/api/create",
                        headers={"type": input("type: \n"),
                                 "amount": input("amount: \n"),
                                 "api_key": input("api key: \n")}).text)
