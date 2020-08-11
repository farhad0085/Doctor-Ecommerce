from app import app


@app.route('/')
def home():
	return "home found"

if __name__ == "__main__":
<<<<<<< HEAD
	app.run(debug=True,host="127.0.0.1", port=5000)
=======
	app.run(debug=True)
>>>>>>> 8e6099b463d88607eaca1bcffe6ec56ddcc20bd8
