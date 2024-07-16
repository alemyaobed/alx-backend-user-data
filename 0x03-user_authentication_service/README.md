# 0x03. User Authentication Service

In the industry, you should not implement your own authentication system and use a module or framework that does it for you (like in Python-Flask: Flask-User). Here, for the learning purpose, we will walk through each step of this mechanism to understand it by doing.

## Resources
Read or watch:
- [Flask documentation](https://flask.palletsprojects.com/en/2.0.x/)
- [Requests module](https://docs.python-requests.org/en/latest/)
- [HTTP status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)

## Learning Objectives
At the end of this project, you are expected to be able to explain to anyone, without the help of Google:
- How to declare API routes in a Flask app
- How to get and set cookies
- How to retrieve request form data
- How to return various HTTP status codes

## How to Declare API Routes in a Flask App

In Flask, you can declare routes (endpoints) for your API using the `@app.route` decorator. Here’s how to do it:

1. **Import Flask and Initialize the App:**

   ```python
   from flask import Flask, jsonify

   app = Flask(__name__)
   ```

2. **Declare Routes:**

   ```python
   @app.route('/hello', methods=['GET'])
   def hello():
       return jsonify({"message": "Hello, World!"})
   ```

3. **Start the Flask App:**

   ```python
   if __name__ == '__main__':
       app.run(debug=True)
   ```

## How to Get and Set Cookies in Flask

### Setting Cookies

You can set cookies in Flask by using the `set_cookie` method of the `Response` object.

```python
from flask import Flask, make_response

app = Flask(__name__)

@app.route('/set-cookie')
def set_cookie():
    response = make_response("Cookie Set")
    response.set_cookie('example', 'value')
    return response
```

### Getting Cookies

You can retrieve cookies from the request object using `request.cookies.get`.

```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/get-cookie')
def get_cookie():
    cookie = request.cookies.get('example')
    return f'The value of the cookie is {cookie}'
```

## How to Retrieve Request Form Data

To retrieve form data sent with a POST request, use `request.form.get`.

```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    return f'Hello, {name}!'
```

## How to Return Various HTTP Status Codes

In Flask, you can return different HTTP status codes by passing the status code as the second argument in the `return` statement.

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/success')
def success():
    return jsonify({"message": "Success"}), 200

@app.route('/not-found')
def not_found():
    return jsonify({"error": "Not Found"}), 404

@app.route('/unauthorized')
def unauthorized():
    return jsonify({"error": "Unauthorized"}), 401
```

## HTTP Status Codes

HTTP status codes are standardized responses from the server to the client indicating the status of the request. Some common ones include:

- **200 OK:** The request was successful.
- **201 Created:** The request was successful, and a new resource was created.
- **400 Bad Request:** The server could not understand the request due to invalid syntax.
- **401 Unauthorized:** The client must authenticate itself to get the requested response.
- **403 Forbidden:** The client does not have access rights to the content.
- **404 Not Found:** The server can not find the requested resource.
- **500 Internal Server Error:** The server has encountered a situation it doesn't know how to handle.

For a more comprehensive list and detailed explanations of HTTP status codes, refer to the [Mozilla Developer Network (MDN) documentation on HTTP response status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status).

## Example Code

Here’s an example that combines all of the above concepts:

```python
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

@app.route('/set-cookie')
def set_cookie():
    response = make_response("Cookie Set")
    response.set_cookie('example', 'value')
    return response

@app.route('/get-cookie')
def get_cookie():
    cookie = request.cookies.get('example')
    if cookie:
        return f'The value of the cookie is {cookie}', 200
    return jsonify({"error": "Cookie not found"}), 404

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    if not name:
        return jsonify({"error": "Name is missing"}), 400
    return f'Hello, {name}!', 200

@app.route('/unauthorized')
def unauthorized():
    return jsonify({"error": "Unauthorized"}), 401

if __name__ == '__main__':
    app.run(debug=True)
```
