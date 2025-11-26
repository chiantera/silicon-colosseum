from flask import Flask, render_template, jsonify
import arena_judge

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fight', methods=['POST'])
def fight():
    # Esegue il match usando il giudice Python
    results = arena_judge.run_match()
    
    # FIX JSON COMPATIBILITY:
    # Python serializza float('inf') in Infinity, che rompe il JSON.parse() del browser.
    # Sterilizziamo i risultati convertendo Infinity in -1.0.
    # Usiamo -1.0 invece di None/null perché il frontend prova a chiamare .toFixed()
    # e null.toFixed() causa un crash JS. -1.0 è "safe" e indica errore.
    if isinstance(results, dict):
        for key, val in results.items():
            # Gestisce dizionari annidati (es. {'rust': {'time': inf}})
            if isinstance(val, dict):
                for subkey, subval in val.items():
                    if subval == float('inf'):
                        val[subkey] = -1.0
            # Gestisce chiavi piatte (es. {'rust_time': inf})
            elif val == float('inf'):
                results[key] = -1.0

    return jsonify(results)

if __name__ == '__main__':
    # FIX CRITICO PER DOCKER:
    # host='0.0.0.0' dice a Flask di accettare connessioni da fuori il container.
    # Senza questo, il port forwarding di Docker non funziona.
    app.run(host='0.0.0.0', port=5000, debug=True)