import requests

p = requests.get('http://127.0.0.1:5000')
print(p)
print(p.text)

p = requests.post('http://127.0.0.1:5000/v1/teachers',
    # data='HW',
    # params={},
    json={'name': 'Tom'},
)
print(p)
print(p.text)

# p = requests.get('http://127.0.0.1:5000/v1/teachers/1')
# print(p)
# print(p.text)

# p = requests.get(
#     'http://127.0.0.1:5000/v1/professors/p_1/papers',
#     params={'pagesize': 5}
# )
# print(p)
# print(p.text)
