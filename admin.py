# admin.py

from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, session, flash
from database import get_db # Importa a função get_db
from auth import login_required # Importa o decorador de login

# Cria um Blueprint para as rotas de administração
bp = Blueprint('admin', __name__, url_prefix='/admin')

# ----- DECORATOR ADMIN -----
def admin_required(f):
    """
    Decorador que verifica se o usuário logado é um administrador.
    """
    @wraps(f)
    def wrapped(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Você precisa estar logado para acessar esta página.', 'info')
            return redirect(url_for('auth.login'))
        db = get_db()
        user = db.execute('SELECT tipo_usuario FROM usuarios WHERE id = ?',
                          (session['usuario_id'],)).fetchone()
        if not user or user['tipo_usuario'] != 'admin':
            flash('Acesso não autorizado. Apenas administradores podem acessar esta página.', 'danger')
            return redirect(url_for('index')) # Redireciona para a página inicial
        return f(*args, **kwargs)
    return wrapped

# ----- ROTAS DE ADMINISTRAÇÃO -----
@bp.route('/')
@login_required
@admin_required
def admin():
    """
    Página do painel de administração.
    Exibe estatísticas e listas de usuários e imóveis.
    """
    db = get_db()

    # Total de usuários
    usuarios = db.execute(
        'SELECT id, nome, email, telefone, tipo_usuario FROM usuarios'
    ).fetchall()
    total_usuarios = len(usuarios)

    # Total de imóveis, ativos e inativos
    total_imoveis = db.execute('SELECT COUNT(*) FROM imoveis').fetchone()[0]
    ativos = db.execute(
        'SELECT COUNT(*) FROM imoveis WHERE ativo = 1'
    ).fetchone()[0]
    inativos = total_imoveis - ativos

    # Lista completa de imóveis com nome do dono
    imoveis = db.execute(
        '''
        SELECT imoveis.*, usuarios.nome AS dono_nome
        FROM imoveis
        JOIN usuarios ON imoveis.usuario_id = usuarios.id
        '''
    ).fetchall()

    # Acessos (variável global da aplicação principal)
    # Como 'app.acessos' é uma variável da instância da aplicação,
    # precisaremos passá-la de alguma forma. Uma maneira simples é
    # fazer com que o app.py passe essa informação para o template,
    # ou acessar current_app.acessos (se definido no app.py)
    # Por simplicidade, vou assumir que 'acessos' será passado para o template
    # ou que current_app.acessos estará disponível.
    # Para este exemplo, vou usar um valor fictício ou assumir que app.acessos
    # será acessível via current_app.
    from flask import current_app
    acessos = getattr(current_app, 'acessos', 0)


    return render_template(
        'admin.html',
        usuarios=usuarios,
        total_usuarios=total_usuarios,
        total_imoveis=total_imoveis,
        ativos=ativos,
        inativos=inativos,
        acessos=acessos,
        imoveis=imoveis
    )

@bp.route('/toggle_anuncio/<int:id>', methods=['POST'])
@login_required
@admin_required
def admin_toggle_anuncio(id):
    """
    Permite que o administrador ative/desative um anúncio de imóvel.
    """
    db = get_db()
    imovel = db.execute('SELECT ativo FROM imoveis WHERE id = ?', (id,)).fetchone()

    if imovel is None:
        flash('Imóvel não encontrado.', 'danger')
        return redirect(url_for('admin.admin'))

    novo_status = 0 if imovel['ativo'] else 1
    db.execute('UPDATE imoveis SET ativo = ? WHERE id = ?', (novo_status, id))
    db.commit()
    flash(f'Status do anúncio alterado para {"ativo" if novo_status else "inativo"} com sucesso!', 'success')
    return redirect(url_for('admin.admin'))

@bp.route('/excluir_imovel/<int:id>', methods=['POST'])
@login_required
@admin_required
def admin_excluir_imovel(id):
    """
    Permite que o administrador exclua qualquer imóvel.
    """
    db = get_db()
    cursor = db.execute('DELETE FROM imoveis WHERE id = ?', (id,))
    db.commit()
    if cursor.rowcount > 0:
        flash('Imóvel excluído com sucesso pelo administrador.', 'success')
    else:
        flash('Imóvel não encontrado.', 'danger')
    return redirect(url_for('admin.admin'))

@bp.route('/excluir_usuario/<int:id>', methods=['POST'])
@login_required
@admin_required
def excluir_usuario(id):
    """
    Permite que o administrador exclua qualquer usuário.
    Impede que o administrador exclua a si mesmo.
    """
    if id == session['usuario_id']:
        flash("Você não pode excluir seu próprio usuário.", 'warning')
        return redirect(url_for('admin.admin'))

    db = get_db()
    cursor = db.execute('DELETE FROM usuarios WHERE id = ?', (id,))
    db.commit()
    if cursor.rowcount > 0:
        flash("Usuário excluído com sucesso pelo administrador.", 'success')
    else:
        flash("Usuário não encontrado.", 'danger')
    return redirect(url_for('admin.admin'))

