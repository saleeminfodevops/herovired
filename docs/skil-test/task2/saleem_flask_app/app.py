from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<p>Saleem Shaikh</p>"

@app.route("/about")
def about():
    return "<p>This application has been created for the Hearovired Task3</p>"

@app.route("/contact")
def contact():
    return "<p>Contact me @ falcontechguru@gmail.com </p>"

@app.route('/status', methods=['GET'])
def status():
    """application is live."""
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
