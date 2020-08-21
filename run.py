from app import app

@app.route('/')
def home():
	return "home found"

if __name__ == "__main__":
	app.run(host="127.0.0.1",port=5000,debug=True)
