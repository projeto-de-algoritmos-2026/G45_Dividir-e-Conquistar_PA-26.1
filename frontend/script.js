const backendBase = '/api';

async function fetchUsers(){
    try{
        const res = await fetch(`${backendBase}/users`);
        if(!res.ok) throw new Error('Erro ao buscar usuários');
        return await res.json();
    }catch(e){
        console.warn(e);
        return null;
    }
}

function populateUsers(list){
    const selA = document.getElementById('userA');
    const selB = document.getElementById('userB');
    if(!selA || !selB) return;
    selA.innerHTML = '';
    selB.innerHTML = '';
    if(!list || !list.length){
        const opt = document.createElement('option'); opt.textContent = 'Nenhum usuário disponível'; opt.disabled = true; selA.appendChild(opt); selB.appendChild(opt.cloneNode(true)); return;
    }
    list.forEach(u => {
        const optA = document.createElement('option');
        optA.value = u.id; optA.textContent = `${u.name} (#${u.id})`;
        const optB = optA.cloneNode(true);
        selA.appendChild(optA);
        selB.appendChild(optB);
    });
    if(list.length>1){ selA.value = list[0].id; selB.value = list[1].id; }
}

function showResults(title, html){
    const res = document.getElementById('results');
    document.getElementById('resultsTitle').textContent = title;
    document.getElementById('resultsBody').innerHTML = html;
    res.style.display = 'block';
}

function hideResults(){
    document.getElementById('results').style.display = 'none';
}

async function getRecommendations(){
    const sel = document.getElementById('userA');
    const uid = sel.value;
    if(!uid) return alert('Selecione um usuário');
    try{
        const resp = await fetch(`${backendBase}/recommend?user=${encodeURIComponent(uid)}`);
        if(!resp.ok) throw new Error('Resposta inválida do servidor');
        const data = await resp.json();
        if(!data || (!data.recommendations && !data.top)){
            showResults('Sem resultados', '<p>O backend retornou dados inesperados.</p>');
            return;
        }

        if(data.recommendations){
            const html = data.recommendations.map(r =>
                `<div class="recommendation"><div class="rec-title">${escapeHtml(r.title)}</div><div class="rec-rating">★ ${Number(r.rating).toFixed(1)}</div></div>`
            ).join('');
            showResults('Recomendações', html);
        } else if(data.top){
            const html = `<p>Top compatíveis:</p>` + data.top.map(t => `<div class="recommendation"><div>${t.name} (#${t.id})</div><div class="rec-rating">${t.compat}%</div></div>`).join('');
            showResults('Top compatíveis', html);
        }

    }catch(e){
        console.error(e);
        showResults('Erro', `<p>Não foi possível conectar ao backend. Verifique se existe um endpoint em <strong>/api</strong>.</p>`);
    }
}

async function getTop(){
    const sel = document.getElementById('userA');
    const uid = sel.value;
    if(!uid) return alert('Selecione um usuário');
    try{
        const resp = await fetch(`${backendBase}/top?user=${encodeURIComponent(uid)}`);
        if(!resp.ok) throw new Error('Resposta inválida do servidor');
        const data = await resp.json();
        if(!data || !data.top) { showResults('Sem resultados', '<p>Sem dados.</p>'); return; }
        const html = data.top.map(t => `<div class="recommendation"><div>${t.name} (#${t.id})</div><div class="rec-rating">${t.compat}%</div></div>`).join('');
        showResults('Top compatíveis', html);
    }catch(e){
        console.error(e);
        showResults('Erro', `<p>Falha ao buscar top compatíveis.</p>`);
    }
}

async function getCompare(){
    const a = document.getElementById('userA').value;
    const b = document.getElementById('userB').value;
    if(!a || !b) return alert('Selecione os dois usuários para comparar');
    if(a === b) return alert('Escolha dois usuários diferentes para comparar');
    try{
        const resp = await fetch(`${backendBase}/compare?user_a=${encodeURIComponent(a)}&user_b=${encodeURIComponent(b)}`);
        if(!resp.ok) throw new Error('Resposta inválida do servidor');
        const data = await resp.json();
        if(data.error){ showResults('Erro', `<p>${escapeHtml(data.error)}</p>`); return; }

        let html = '';
        if(data.inversions === -1){
            html += `<p>Filmes em comum: ${data.common} — insuficiente para comparar (mínimo 5).</p>`;
        } else {
            html += `<p>Filmes em comum: <strong>${data.common}</strong></p>`;
            html += `<p>Inversões: <strong>${data.inversions}</strong></p>`;
            html += `<p>Compatibilidade: <strong>${data.compat}%</strong></p>`;
            if(data.shared && data.shared.length){
                html += '<h4>Filmes em comum</h4>';
                html += '<div>' + data.shared.slice(0,50).map(s =>
                    `<div class="recommendation"><div>${escapeHtml(s.title)}</div><div class="rec-rating">A: ${s.rating_a.toFixed(1)} — B: ${s.rating_b.toFixed(1)}</div></div>`
                ).join('') + '</div>';
            }
        }
        showResults('Comparação entre usuários', html);
    }catch(e){
        console.error(e);
        showResults('Erro', `<p>Falha ao buscar comparação.</p>`);
    }
}

function escapeHtml(s){
    return String(s).replace(/[&<>"]+/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
}

document.addEventListener('DOMContentLoaded', async ()=>{
    const users = await fetchUsers();
    if(users) populateUsers(users);
    else populateUsers([]);

    document.getElementById('btnRecommend').addEventListener('click', getRecommendations);
    document.getElementById('btnTop').addEventListener('click', getTop);
    const btnToggle = document.getElementById('btnToggleCompare');
    const btnRun = document.getElementById('btnRunCompare');
    const selB = document.getElementById('userB');
    // hide second select initially
    if(selB) selB.style.display = 'none';

    if(btnToggle){
        btnToggle.addEventListener('click', ()=>{
            if(!selB) return;
            const showing = selB.style.display !== 'none';
            if(showing){
                selB.style.display = 'none';
                btnRun.style.display = 'none';
                btnToggle.textContent = 'Comparar duas pessoas';
            } else {
                selB.style.display = 'inline-block';
                btnRun.style.display = 'inline-block';
                btnToggle.textContent = 'Cancelar comparação';
            }
        });
    }
    if(btnRun) btnRun.addEventListener('click', getCompare);
    document.getElementById('btnCloseResults').addEventListener('click', hideResults);
});
