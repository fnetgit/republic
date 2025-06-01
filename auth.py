# auth.py

from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, g, flash
import sqlite3
from database import get_db  # Importa a função get_db do novo módulo

# Cria um Blueprint para as rotas de autenticação
bp = Blueprint('auth', __name__, url_prefix='/')

# ----- DECORATOR LOGIN -----


def login_required(f):
    """
    Decorador que verifica se o usuário está logado.
    Se não estiver logado, redireciona para a página de login.
    """
    @wraps(f)
    def wrapped(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Você precisa estar logado para acessar esta página.', 'info')
            # Redireciona para a rota de login do blueprint
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return wrapped

# ----- CONTEXTO GLOBAL (mantido aqui para o exemplo, mas pode ser movido para app.py se for global para toda a aplicação) -----


@bp.context_processor
def inject_usuario():
    """
    Injeta informações do usuário logado em todos os templates.
    """
    usuario_nome = tipo_usuario = None
    user_id = session.get('usuario_id')
    if user_id:
        db = get_db()
        cur = db.execute(
            'SELECT nome, tipo_usuario FROM usuarios WHERE id = ?', (user_id,)
        )
        row = cur.fetchone()
        if row:
            usuario_nome = row['nome']
            tipo_usuario = row['tipo_usuario']
    return dict(usuario_nome=usuario_nome, tipo_usuario=tipo_usuario)

# ----- ROTAS DE AUTENTICAÇÃO E CADASTRO -----


@bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    """
    Rota para cadastro de novos usuários.
    Permite GET para exibir o formulário e POST para processar o cadastro.
    """
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        telefone = request.form['telefone']
        tipo_usuario = request.form['tipo_usuario']
        db = get_db()
        try:
            db.execute(
                'INSERT INTO usuarios (nome, email, senha, telefone, tipo_usuario) VALUES (?, ?, ?, ?, ?)',
                (nome, email, senha, telefone, tipo_usuario)
            )
            db.commit()
            flash('Cadastro realizado com sucesso! Faça login para continuar.', 'success')
            # Redireciona para a página de login após o cadastro
            return redirect(url_for('auth.login'))
        except sqlite3.IntegrityError:
            flash('Email já cadastrado. Tente outro email ou faça login.', 'danger')
    return render_template('cadastro.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Rota para login de usuários existentes.
    Permite GET para exibir o formulário e POST para processar o login.
    """
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        db = get_db()
        user = db.execute(
            'SELECT id FROM usuarios WHERE email = ? AND senha = ?', (
                email, senha)
        ).fetchone()
        if user:
            session['usuario_id'] = user['id']
            flash('Login realizado com sucesso!', 'success')
            # Redireciona para a página inicial
            return redirect(url_for('index'))
        flash('Email ou senha inválidos!', 'danger')
    return render_template('cadastro.html')


@bp.route('/logout')
@login_required
def logout():
    """
    Rota para deslogar o usuário.
    Remove o ID do usuário da sessão.
    """
    session.pop('usuario_id', None)
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('auth.login'))
