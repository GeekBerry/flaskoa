import requests

p = requests.get('http://127.0.0.1:5000')
print(p)
print(p.text)

p = requests.post('http://127.0.0.1:5000/v1/teachers/?q1=1&q2=hi',
    # data='HW',
    json={1: 100}
)
print(p)
print(p.text)

p = requests.get('http://127.0.0.1:5000/v1/teachers/1')
print(p)
print(p.text)
