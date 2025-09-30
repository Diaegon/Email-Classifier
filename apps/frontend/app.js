(function () {
  const form = document.getElementById('classify-form');
  const textarea = document.getElementById('email-text');
  const fileInput = document.getElementById('email-file');
  const submitBtn = document.getElementById('submit-btn');
  const resultSection = document.getElementById('result');
  const resCategory = document.getElementById('res-category');
  const resReason = document.getElementById('res-reason');
  const resReply = document.getElementById('res-reply');

  function setLoading(isLoading) {
    submitBtn.disabled = isLoading;
    submitBtn.textContent = isLoading ? 'Classificando com IA...' : 'Classificar com IA';
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
    } catch (err) {
      console.error(err);
      alert(err.message || 'Erro inesperado');
    } finally {
      setLoading(false);
    }
  });
})();
