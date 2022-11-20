from flask import Flask
from flask import send_file
app = Flask(__name__)

@app.route("/")
def main():
  return send_file("html/new.html")

if __name__ == "__main__":
  app.run(debug=True, port=3000,host='0.0.0.0')