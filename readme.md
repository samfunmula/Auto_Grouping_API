### Start Fast API
```bash
cd src/
python3 main.py
```

## Request
## POST
### /api/v1/grouping/autogrouping/

### Curl
``` bash 
curl -X 'POST' \
  'http://127.0.0.1:8000/api/v1/grouping/autogrouping/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"title":"SYM三陽機車 WOO 115 七期鼓煞 CBS版 2023新車"}'
```

### Response
```
{
  "query_string": "(SYM OR 三陽機車) WOO 115",
  "price_range": {
    "min_price": 30000
  }
} 
```

## Errors
### UNSUPPORTED REQUEST FORMAT
```json
HTTP/1.1 400
{"result": "UNSUPPORTED_REQUEST_FORMAT"}
```

### GENERATE QUERY STRING ERROR
```json
HTTP/1.1 400
{"result": "GENERATE_QUERY_STRING_ERROR"}
```

### INTERNAL_ERROR LANGUAGE
```json
HTTP/1.1 500
{"result": "INTERNAL_ERROR"}
```

# Client send request demo code
## JavaScript
POST
```javascript
    const jsonData = JSON.stringify({"title":"SYM三陽機車 WOO 115 七期鼓煞 CBS版 2023新車"});

    fetch('http://127.0.0.1:8000/api/v1/grouping/autogrouping/', {
        method: 'POST',
        body: jsonData
    })
    .then(response => response.json())
    .then(data => {console.log(data);})
```

## python
POST
```python
import requests

url = "http://127.0.0.1:8000/api/v1/grouping/autogrouping/"
response = requests.post(url, json={"title": "SYM三陽機車 WOO 115 七期鼓煞 CBS版 2023新車"})
print(response.json())
```