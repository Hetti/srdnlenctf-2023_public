import requests
import base64

res = requests.post('https://adapt.challs.srdnlen.it/query?perturbation=iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAAAAABXZoBIAAABN0lEQVQoFXXBwUvbYBjA4d8b3WCrL4hzl4A2B8m2z01ynGBvvez7gyO4g6ADT4OB6IaUNRcD28W611tLMEltTAZ5HkGNtqNv8Y0alVDoFwtq9IiFfrHQzwv9VKjFe6TjSRZQKlhSFWouurgHioCCxjuhloQ3EwiKw83Tl%2F9YUoQOT%2B384wUloc1FPEkpCW2OiKWTV9tThBb36%2F1sa5dKihpCy%2FBuc%2BOaZ8IzF%2BVTK2io0Ej%2BJjD%2FykqYCyuK4SG7hihTQy0ROjzZZLE%2B%2Fv4HcJHQ8Xb%2B%2BYSDMKUUvxY61ALWxsdUvojQa%2BeNqAH%2BHON%2FLhQ1dATz6e%2BCDt1BKHkub4ugGAxvBzkrOsokzGH%2FJ3y4clG2eNg7Y8Xnogb4bJaDm5nR0BFCLeEH%2BJQ2NVGMyos5lU%2BZ0XgEMg1dkV7YCFoAAAAASUVORK5CYII%3D')
print(res.json()['Flag'])