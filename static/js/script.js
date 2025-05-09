document.addEventListener('DOMContentLoaded', () => {
    const loadMoreBtn = document.getElementById('loadMore');
    const cards = document.querySelectorAll('.card');
    const filtros = document.querySelectorAll('input');
    const searchInput = document.getElementById('searchInput');

    if (!cards.length) return; // Se não houver cards, encerra o script

    // Função para filtrar por valor
    function filtrarPorValor(card, valor) {
        const cardValor = parseInt(card.dataset.valor);
        if (valor === '500' && cardValor > 500) return false;
        if (valor === '1000' && (cardValor <= 500 || cardValor > 1000)) return false;
        if (valor === 'acima' && cardValor <= 1000) return false;
        return true;
    }

    // Função para filtrar por tipo
    function filtrarPorTipo(card, tipos) {
        const cardTipo = card.dataset.tipo;
        return tipos.length ? tipos.includes(cardTipo) : true;
    }

    // Função para filtrar por quartos
    function filtrarPorQuartos(card, quartos) {
        const cardQuartos = parseInt(card.dataset.quartos);
        return quartos.length ? quartos.includes(cardQuartos >= 3 ? '3' : String(cardQuartos)) : true;
    }

    // Função para filtrar por extras
    function filtrarPorExtras(card, extras) {
        const cardExtras = card.dataset.extras.split(',');
        return extras.length ? extras.every(extra => cardExtras.includes(extra)) : true;
    }

    // Função para filtrar por endereço (pesquisa)
    function filtrarPorEndereco(card, search) {
        const cardEndereco = card.dataset.endereco.toLowerCase();
        return cardEndereco.includes(search);
    }

    // Função principal de filtro
    function filtrar() {
        const valor = document.querySelector('input[name="valor"]:checked')?.value;
        const tipos = Array.from(document.querySelectorAll('input[name="tipo"]:checked')).map(e => e.value);
        const quartos = Array.from(document.querySelectorAll('input[name="quartos"]:checked')).map(e => e.value);
        const extras = Array.from(document.querySelectorAll('input[name="extras"]:checked')).map(e => e.value);
        const search = searchInput?.value.toLowerCase() || '';

        cards.forEach(card => {
            let show = true;

            // Aplica cada filtro de maneira modularizada
            if (valor && valor !== 'todos' && !filtrarPorValor(card, valor)) show = false;
            if (tipos.length && !filtrarPorTipo(card, tipos)) show = false;
            if (quartos.length && !filtrarPorQuartos(card, quartos)) show = false;
            if (extras.length && !filtrarPorExtras(card, extras)) show = false;
            if (search && !filtrarPorEndereco(card, search)) show = false;

            card.style.display = show ? 'block' : 'none';
        });
    }

    // Inicializa com 6 cards visíveis e esconde os outros
    cards.forEach((card, index) => {
        if (index >= 6) {
            card.classList.add('hidden');
        }
    });

    filtrar(); // Filtro inicial

    // Botão "Carregar mais"
    loadMoreBtn?.addEventListener('click', () => {
        document.querySelectorAll('.card.hidden').forEach(card => {
            card.classList.remove('hidden');
        });
        loadMoreBtn.style.display = 'none';
        filtrar();
    });

    // Filtros e pesquisa
    filtros.forEach(input => {
        input.addEventListener('input', filtrar);
    });

    searchInput?.addEventListener('input', filtrar);
});
