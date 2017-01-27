import requests
r = requests.get('http://yasdelie.ru/img/profile.png')
print(r.status_code)