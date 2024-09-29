from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

app = Flask(__name__)

# Configurando o banco de dados PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5433/controle_visitantes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definindo o modelo de visitante


class Visitante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), nullable=False, unique=True)
    empresa_ou_particular = db.Column(db.String(50), nullable=False)
    setor = db.Column(db.String(100), nullable=False)
    horario_chegada = db.Column(
        db.DateTime, default=datetime.now().strftime('%d/%m/%Y %H:%M'))
    horario_saida = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<Visitante {self.nome}>'

# Rota principal


@app.route('/')
def index():
    visitantes = Visitante.query.filter(
        db.func.date(Visitante.horario_chegada) == datetime.now().strftime(
            '%Y/%m/%d')
    ).all()
    for visitante in visitantes:
        chegada = visitante.horario_chegada
        chegadaTime = chegada.strftime('%H:%M')
        visitante.horario_chegada = chegadaTime
        if visitante.horario_saida is not None:
            saida = visitante.horario_saida
            saidaTime = saida.strftime('%H:%M')
            visitante.horario_saida = saidaTime

    day = datetime.now().strftime('%d-%m-%Y')
    return render_template('index.html', visitantes=visitantes, data=day)

# Rota para cadastro de visitante


@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar_visitante():
    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        empresa_ou_particular = request.form['empresa_ou_particular']
        setor = request.form['setor']

        novo_visitante = Visitante(
            nome=nome, cpf=cpf, empresa_ou_particular=empresa_ou_particular, setor=setor)
        try:
            db.session.add(novo_visitante)
            db.session.commit()
            return redirect('/')
        except:
            return 'Houve um erro ao cadastrar o visitante.'
    return render_template('visitante.html')

# Rota para registrar a saída do visitante


@app.route('/sair/<int:id>')
def registrar_saida(id):
    visitante = Visitante.query.get_or_404(id)
    visitante.horario_saida = datetime.now().strftime('%d/%m/%Y %H:%M')

    try:
        db.session.commit()
        return redirect('/')
    except:
        return 'Houve um erro ao registrar a saída do visitante.'

# Rota para o relatório diário


@app.route('/relatorio', methods=['GET', 'POST'])
def relatorio_visitantes_por_dia():
    if request.method == 'POST':
        # Recebe a data informada no formulário
        data_relatorio = request.form['data']
        # Converte a string da data para um objeto datetime
        data_formatada = datetime.strptime(data_relatorio, '%Y-%m-%d').date()

        # Filtra os visitantes pela data escolhida
        visitantes_do_dia = Visitante.query.filter(
            db.func.date(Visitante.horario_chegada) == data_formatada
        ).all()
        for visitante in visitantes_do_dia:
            chegada = visitante.horario_chegada
            chegadaTime = chegada.strftime('%H:%M')
            visitante.horario_chegada = chegadaTime

            saida = visitante.horario_saida
            saidaTime = saida.strftime('%H:%M')
            visitante.horario_saida = saidaTime

        day = data_formatada.strftime('%d-%m-%Y')
        return render_template('relatorio.html', visitantes=visitantes_do_dia, data=day)

    return render_template('form_relatorio.html')


# Criar as tabelas no banco de dados
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
