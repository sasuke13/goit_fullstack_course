from email.message import _PayloadType
import requests

# try:
#     headers = {
#         "Authorization": "Bearer 1234567890",
#         "Content-Type": "application/json",
#         "Accept": "application/json",
#     }
#     payload = {
#         "name": "John",
#         "email": "john@example.com"
#     }
#     response = requests.post(
#         "https://api.example.com/submit",
#         headers=headers,
#         json=payload
#     )
#     response.raise_for_status()
#     print(response.json())

# except Exception as e:
#     print(f"Error: {e}")


with requests.Session() as session:
    response = session.get("https://api.example.com/protected")
    response.raise_for_status()
    print(response.json())
