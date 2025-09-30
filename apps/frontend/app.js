(function () {
  // Elementos do formulário de classificação de email
  const form = document.getElementById('classify-form');
  const textarea = document.getElementById('email-text');
  const fileInput = document.getElementById('email-file');
  const clearFileBtn = document.getElementById('clear-file-btn');
  const submitBtn = document.getElementById('submit-btn');
  const resultSection = document.getElementById('result');
  const resCategory = document.getElementById('res-category');
  const resReason = document.getElementById('res-reason');
  const resReply = document.getElementById('res-reply');

  // Elementos do formulário de busca de clientes
  const clientForm = document.getElementById('client-search-form');
  const clientSearchInput = document.getElementById('client-search');
  const clientSearchBtn = document.getElementById('client-search-btn');
  const clientResultsSection = document.getElementById('client-results');
  const clientResultsContent = document.getElementById('client-results-content');
  
  // Elementos da resposta editável
  const clientResponseTextarea = document.getElementById('client-response');
  const copyResponseBtn = document.getElementById('copy-response-btn');

  function setLoading(isLoading) {
    submitBtn.disabled = isLoading;
    submitBtn.textContent = isLoading ? 'Classificando com IA...' : 'Classificar com IA';
  }

  function setClientSearchLoading(isLoading) {
    clientSearchBtn.disabled = isLoading;
    clientSearchBtn.textContent = isLoading ? 'Buscando...' : 'Buscar Cliente';
  }

  function formatClientData(client) {
    const statusBadge = client.plano_contratual_em_dia 
      ? '<span class="badge bg-success">Em Dia</span>' 
      : '<span class="badge bg-danger">Em Atraso</span>';
    
    return `
      <div class="card mb-3">
        <div class="card-body">
          <h6 class="card-title text-primary">${client.nome_completo}</h6>
          <div class="client-result-grid">
            <div>
              <small class="text-muted">CPF:</small><br>
              <span class="fw-semibold">${client.cpf}</span>
            </div>
            <div>
              <small class="text-muted">Número:</small><br>
              <span class="fw-semibold">${client.numero_cliente}</span>
            </div>
            <div>
              <small class="text-muted">Email:</small><br>
              <span class="fw-semibold">${client.email}</span>
            </div>
            <div>
              <small class="text-muted">Status:</small><br>
              ${statusBadge}
            </div>
            <div>
              <small class="text-muted">Perfil:</small><br>
              <span class="fw-semibold">${client.perfil_investidor}</span>
            </div>
            <div>
              <small class="text-muted">Nascimento:</small><br>
              <span class="fw-semibold">${new Date(client.data_nascimento).toLocaleDateString('pt-BR')}</span>
            </div>
          </div>
          ${client.ativos_custodiados ? `
            <div class="mt-2">
              <small class="text-muted">Ativos Custodiados:</small><br>
              <span class="fw-semibold">${client.ativos_custodiados}</span>
            </div>
          ` : ''}
        </div>
      </div>
    `;
  }

  form.addEventListener('submit', async (ev) => {
    ev.preventDefault();
    setLoading(true);

    try {
      const data = new FormData();
      const textVal = textarea.value.trim();
      const file = fileInput.files && fileInput.files[0];

      if (!textVal && !file) {
        alert('Informe o texto do email ou selecione um arquivo .txt/.pdf');
        return;
      }

      if (file) {
        console.log('[DEBUG] selected file:', { name: file.name, size: file.size, type: file.type });
        if (!file.size) {
          alert('O arquivo selecionado está vazio (0 bytes). Salve o arquivo com conteúdo e tente novamente.');
          return;
        }
      }

      if (textVal) data.append('text', textVal);
      if (file) data.append('file', file);

      const resp = await fetch(`${window.BACKEND_BASE}/api/classify`, {
        method: 'POST',
        body: data,
      });

      if (!resp.ok) {
        const msg = await resp.text();
        throw new Error(`Falha na classificação: ${resp.status} ${msg}`);
      }

      const payload = await resp.json();
      resCategory.textContent = payload.category || '—';
      resReason.textContent = payload.reason || '—';
      resReply.textContent = payload.suggested_reply || '—';
      resultSection.classList.remove('d-none');
      
      // Sincronizar resposta com a área editável dos clientes
      clientResponseTextarea.value = payload.suggested_reply || '';
    } catch (err) {
      console.error(err);
      alert(err.message || 'Erro inesperado');
    } finally {
      setLoading(false);
    }
  });

  // Event listener para busca de clientes
  clientForm.addEventListener('submit', async (ev) => {
    ev.preventDefault();
    setClientSearchLoading(true);

    try {
      const query = clientSearchInput.value.trim();
      
      if (query.length < 2) {
        alert('Digite pelo menos 2 caracteres para buscar');
        return;
      }

      const resp = await fetch(`${window.BACKEND_BASE}/api/clients/search?q=${encodeURIComponent(query)}`);
      
      if (!resp.ok) {
        const msg = await resp.text();
        throw new Error(`Falha na busca: ${resp.status} ${msg}`);
      }

      const data = await resp.json();
      
      if (data.success && data.clients && data.clients.length > 0) {
        clientResultsContent.innerHTML = data.clients.map(formatClientData).join('');
        clientResultsSection.classList.remove('d-none');
      } else {
        clientResultsContent.innerHTML = '<div class="alert alert-warning">Nenhum cliente encontrado com os critérios de busca.</div>';
        clientResultsSection.classList.remove('d-none');
      }
    } catch (err) {
      console.error(err);
      clientResultsContent.innerHTML = '<div class="alert alert-danger">Erro na busca de clientes. Tente novamente.</div>';
      clientResultsSection.classList.remove('d-none');
    } finally {
      setClientSearchLoading(false);
    }
  });

  // Busca em tempo real conforme o usuário digita (debounced)
  let searchTimeout;
  clientSearchInput.addEventListener('input', (ev) => {
    clearTimeout(searchTimeout);
    const query = ev.target.value.trim();
    
    if (query.length >= 2) {
      searchTimeout = setTimeout(() => {
        clientForm.dispatchEvent(new Event('submit'));
      }, 500); // Aguarda 500ms após parar de digitar
    } else if (query.length === 0) {
      clientResultsSection.classList.add('d-none');
    }
  });

  // Funcionalidade do botão de cópia
  copyResponseBtn.addEventListener('click', async () => {
    try {
      const textToCopy = clientResponseTextarea.value;
      
      if (!textToCopy.trim()) {
        alert('Não há texto para copiar');
        return;
      }

      await navigator.clipboard.writeText(textToCopy);
      
      // Feedback visual do botão
      const originalText = copyResponseBtn.innerHTML;
      copyResponseBtn.innerHTML = `
        <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16" class="me-2">
          <path d="M13.854 3.646a.5.5 0 0 1 0 .708l-7 7a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L6.5 10.293l6.646-6.647a.5.5 0 0 1 .708 0z"/>
        </svg>
        Copiado!
      `;
      copyResponseBtn.classList.remove('btn-outline-secondary');
      copyResponseBtn.classList.add('btn-primary');
      
      // Restaurar botão após 2 segundos
      setTimeout(() => {
        copyResponseBtn.innerHTML = originalText;
        copyResponseBtn.classList.remove('btn-primary');
        copyResponseBtn.classList.add('btn-outline-secondary');
      }, 2000);
      
    } catch (err) {
      console.error('Erro ao copiar texto:', err);
      alert('Erro ao copiar texto. Tente selecionar e copiar manualmente.');
    }
  });

  // Funcionalidade do botão de limpar arquivo
  clearFileBtn.addEventListener('click', () => {
    fileInput.value = '';
    
    // Feedback visual do botão
    const originalContent = clearFileBtn.innerHTML;
    clearFileBtn.innerHTML = `
      <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
        <path d="M13.854 3.646a.5.5 0 0 1 0 .708l-7 7a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L6.5 10.293l6.646-6.647a.5.5 0 0 1 .708 0z"/>
      </svg>
    `;
    clearFileBtn.classList.remove('btn-outline-danger');
    clearFileBtn.classList.add('btn-primary');
    
    // Restaurar botão após 1 segundo
    setTimeout(() => {
      clearFileBtn.innerHTML = originalContent;
      clearFileBtn.classList.remove('btn-primary');
      clearFileBtn.classList.add('btn-outline-danger');
    }, 1000);
  });
})();
