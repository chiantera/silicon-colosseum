from flask import Flask, render_template, jsonify
import arena_judge

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fight', methods=['POST'])
def fight():
    results = arena_judge.run_match()
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
