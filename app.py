@app.route('/')
def home():
    try:
        with open('index.html', 'r') as f:
            return f.read()
    except:
        return """
        <h1>First Meta is Live</h1>
        <p>Builder: Andrea Kisumu</p>
        <p>Version: 0.2.3 FINAL FIX</p>
        <p><a href='/api'>View API JSON</a></p>
        """
