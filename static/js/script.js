// Máscara simples de CEP: 12345-678
function maskCEP(input) {
    input.addEventListener('input', () => {
        let v = input.value.replace(/\D/g, '');
        if (v.length > 5) v = v.slice(0, 5) + '-' + v.slice(5, 8);
        input.value = v;
    });
}

// Formata valor como moeda brasileira: 1.234,56
function maskCurrency(input) {
    input.addEventListener('input', () => {
        let v = input.value.replace(/\D/g, '');
        v = (v / 100).toFixed(2) + '';
        v = v.replace('.', ',');
        v = v.replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1.');
        input.value = v;
    });
}

// Pré-visualização de imagens selecionadas
function previewImages(event) {
    const files = event.target.files;
    const previewContainer = document.getElementById('image-preview-container');
    previewContainer.innerHTML = '';

    if (files.length > 5) {
        alert('Você pode adicionar até 5 imagens.');
        event.target.value = '';  // limpa seleção
        return;
    }

    Array.from(files).forEach(file => {
        const reader = new FileReader();
        reader.onload = e => {
            const img = document.createElement('img');
            img.src = e.target.result;
            img.classList.add('preview-img');
            previewContainer.appendChild(img);
        };
        reader.readAsDataURL(file);
    });
}

function getUrlParams() {
    const parts = window.location.pathname.split('/');
    return { id: parts.pop() };
}

async function carregarDadosImovel() {
    const { id } = getUrlParams();
    if (!id) { alert('ID não fornecido'); return; }

    const resp = await fetch(`/api/imovel/${id}`);
    if (!resp.ok) {
        const err = await resp.json();
        alert(err.erro || 'Falha ao carregar');
        return;
    }

    const imovel = await resp.json();
    document.getElementById('imovelId').value = imovel.id;
    ['tipo', 'endereco', 'bairro', 'numero', 'cep', 'complemento', 'valor', 'quartos', 'banheiros', 'outros', 'descricao']
        .forEach(f => document.getElementById(f).value = imovel[f] || '');

    imovel.inclusos?.forEach(item => {
        const cb = document.querySelector(`input[name="inclusos"][value="${item}"]`);
        if (cb) cb.checked = true;
    });

    const existing = document.getElementById('existing-images-container');
    if (imovel.fotos?.length) {
        existing.innerHTML = '<h3>Imagens atuais:</h3>';
        imovel.fotos.forEach(f => {
            const wrap = document.createElement('div');
            wrap.className = 'existing-img-wrapper';
            const img = document.createElement('img');
            img.src = f;
            img.className = 'existing-img';
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.textContent = 'X';
            btn.onclick = () => wrap.remove();
            wrap.append(img, btn);
            existing.append(wrap);
        });
    }
}

async function enviarFormulario(e) {
    e.preventDefault();

    // Validação: pelo menos uma foto (existente ou nova)
    const existentes = document.querySelectorAll('#existing-images-container img').length;
    const novas = document.getElementById('foto-input').files.length;
    if (existentes + novas === 0) {
        alert('Adicione ao menos uma foto do imóvel.');
        return;
    }

    const id = document.getElementById('imovelId').value;
    const dados = { inclusos: [] };
    new FormData(e.target).forEach((v, k) => {
        if (k === 'inclusos') dados.inclusos.push(v);
        else dados[k] = v;
    });

    const fd = new FormData();
    fd.append('dados', JSON.stringify(dados));
    Array.from(document.getElementById('foto-input').files)
        .forEach(file => fd.append('novas_fotos', file));

    const resp = await fetch(`/api/imoveis/${id}`, { method: 'PUT', body: fd });
    if (!resp.ok) {
        const err = await resp.text();
        alert(err || 'Erro na atualização');
        return;
    }

    alert('Atualizado!');
    window.location.href = "{{ url_for('meus_imoveis') }}";
}

document.addEventListener('DOMContentLoaded', () => {
    maskCEP(document.getElementById('cep'));
    maskCurrency(document.getElementById('valor'));
    carregarDadosImovel();
    document.getElementById('editarImovelForm').onsubmit = enviarFormulario;
});


// filtros
document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('searchInput');
    const cards = document.querySelectorAll('.card');

    // Filtros
    const tipoCheckboxes = document.querySelectorAll('input[name="tipo"]');
    const extrasCheckboxes = document.querySelectorAll('input[name="extras"]');

    function getCheckedValues(inputs) {
        return Array.from(inputs)
            .filter(input => input.checked)
            .map(input => input.value);
    }

    function filtrarCards() {
        const searchText = searchInput.value.toLowerCase();
        const minValor = parseFloat(document.getElementById('minValor').value) || 0;
        const maxValor = parseFloat(document.getElementById('maxValor').value) || Infinity;
        const tiposSelecionados = getCheckedValues(tipoCheckboxes);
        const minQuartos = parseInt(document.getElementById('quartosSlider').value);
        const extrasSelecionados = getCheckedValues(extrasCheckboxes);

        cards.forEach(card => {
            const tipo = card.dataset.tipo;
            const quartos = parseInt(card.dataset.quartos);
            const valor = parseFloat(card.dataset.valor);
            const extras = card.dataset.extras.toLowerCase();
            const endereco = card.dataset.endereco.toLowerCase();

            // Filtro de valor
            let passaValor = (valor >= minValue && valor <= maxValue);

            // Filtro de tipo
            let passaTipo = tiposSelecionados.length === 0 || tiposSelecionados.includes(tipo);

            // Filtro de quartos
            let passaQuartos = quartos >= minQuartos;
            
            // Filtro de extras
            let passaExtras = extrasSelecionados.every(extra => extras.includes(extra));

            // Filtro de busca por endereço
            let passaBusca = endereco.includes(searchText);

            // Mostrar ou ocultar
            if (passaValor && passaTipo && passaQuartos && passaExtras && passaBusca) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    }

    // Eventos
    searchInput.addEventListener('input', filtrarCards);
    document.getElementById('minValor').addEventListener('input', filtrarCards);
    document.getElementById('maxValor').addEventListener('input', filtrarCards);
    tipoCheckboxes.forEach(c => c.addEventListener('change', filtrarCards));

    const quartosSlider = document.getElementById('quartosSlider');
    const quartosValueSpan = document.getElementById('quartosValue');
    quartosSlider.addEventListener('input', () => {
    quartosValueSpan.textContent = quartosSlider.value; // Atualiza o texto do span
    filtrarCards(); // Filtra os cards
    });
    extrasCheckboxes.forEach(c => c.addEventListener('change', filtrarCards));
    filtrarCards()
});