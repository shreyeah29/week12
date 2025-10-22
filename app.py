from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('pwd')

        # Validation checks (with periods at the end to match tests)
        if not username:
            return '''<script>
            alert('Username cannot be empty.');
            window.history.back();
            </script>'''

        if not password:
            return '''<script>
            alert('Password cannot be empty.');
            window.history.back();
            </script>'''

        if len(password) < 6:
            return '''<script>
            alert('Password must be at least 6 characters long.');
            window.history.back();
            </script>'''

        # Successful submission
        return redirect(url_for('submit', username=username))

    return render_template('form.html')


@app.route('/submit')
def submit():
    username = request.args.get('username', '')
    return render_template('greeting.html', name=username)


if __name__ == "__main__":
    # Use host=0.0.0.0 so Jenkins & Docker can access it
    app.run(host='0.0.0.0', port=5000, debug=True)