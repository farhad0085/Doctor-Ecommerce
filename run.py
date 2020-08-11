from app import app

@app.route('/')
def home():
	return "home found"

if __name__ == "__main__":
	app.run(debug=True)
