from flask import Flask, request, jsonify
from funcao import validar_cpf

app = Flask(__name__)

@app.route('/validar_cpf', methods=['POST'])
def validar():
    data = request.get_json()
    cpf = data.get('cpf', '')
    valido = validar_cpf(cpf)
    return jsonify({'valido': valido})

if __name__ == '__main__':
    app.run(debug=True)

