# Hint: Simple Flask Echo API for Question 4

This example Flask app echoes back any JSON data sent to it via POST requests.

### 📄 `app.py`

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/echo', methods=['POST'])
def echo():
    data = request.get_json()
    return jsonify({
        "you_sent": data
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```