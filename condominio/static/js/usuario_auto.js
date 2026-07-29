/**
 * usuario_auto.js
 * ===============
 * Geração automática de nome de usuário no formulário de cadastro.
 *
 * Regras:
 *   1. usuario = primeiro.ultimo    → ex: joao.silva
 *   2. Se conflito → primeiro.penultimo → ex: joao.batista
 *   3. Se ambos conflitam → habilita edição manual
 *
 * Requer:
 *   - Input de nome:    id="nome_funcionario"  (ou "nome_morador")
 *   - Input de usuário: id="usuario_gerado"
 *   - Elemento de status: id="usuario_status"
 *   - Variável global: NOME_FIELD = 'nome_funcionario' | 'nome_morador'
 */

(function () {
  'use strict';

  /* ── Helpers de texto ─────────────────────────────────────── */

  function removerAcentos(str) {
    var map = {
      'á':'a','à':'a','â':'a','ã':'a','ä':'a',
      'é':'e','è':'e','ê':'e','ë':'e',
      'í':'i','ì':'i','î':'i','ï':'i',
      'ó':'o','ò':'o','ô':'o','õ':'o','ö':'o',
      'ú':'u','ù':'u','û':'u','ü':'u',
      'ç':'c','ñ':'n',
      'Á':'a','À':'a','Â':'a','Ã':'a','Ä':'a',
      'É':'e','È':'e','Ê':'e','Ë':'e',
      'Í':'i','Ì':'i','Î':'i','Ï':'i',
      'Ó':'o','Ò':'o','Ô':'o','Õ':'o','Ö':'o',
      'Ú':'u','Ù':'u','Û':'u','Ü':'u',
      'Ç':'c','Ñ':'n'
    };
    return str.replace(/[^\u0000-\u007E]/g, function(c){ return map[c] || c; });
  }

  function slugify(texto) {
    return removerAcentos(texto || '')
      .toLowerCase()
      .replace(/[^a-z0-9\s]/g, '')
      .trim();
  }

  function partesNome(nome) {
    return slugify(nome).split(/\s+/).filter(function(p){ return p.length > 0; });
  }

  function gerarCandidatos(nome) {
    var p = partesNome(nome);
    if (!p.length) return [];
    var primeiro = p[0];
    var cands = [];
    if (p.length >= 2) cands.push(primeiro + '.' + p[p.length - 1]);           // primeiro.ultimo
    if (p.length >= 3) cands.push(primeiro + '.' + p[p.length - 2]);           // primeiro.penultimo
    return cands;
  }

  /* ── Estado do módulo ─────────────────────────────────────── */
  var _timer      = null;
  var _editManual = false;  // true = usuário habilitado para edição
  var _ultimo     = '';     // último valor checado

  /* ── Elementos DOM ────────────────────────────────────────── */
  var _nomeInput, _usuarioInput, _statusEl, _lockIcon;

  function init() {
    var nomeField = window.NOME_FIELD || 'nome_funcionario';
    _nomeInput    = document.getElementById(nomeField);
    _usuarioInput = document.getElementById('usuario_gerado');
    _statusEl     = document.getElementById('usuario_status');
    _lockIcon     = document.getElementById('usuario_lock_icon');

    if (!_nomeInput || !_usuarioInput) return;

    /* Ouve mudanças no campo de nome */
    _nomeInput.addEventListener('input', function () {
      clearTimeout(_timer);
      _timer = setTimeout(autoGerar, 400);
    });

    /* Se o usuário editar manualmente (quando habilitado) */
    _usuarioInput.addEventListener('input', function () {
      if (_editManual) {
        clearTimeout(_timer);
        _timer = setTimeout(function () {
          verificarDisponibilidade(_usuarioInput.value.trim().toLowerCase(), null);
        }, 500);
      }
    });
  }

  /* ── Geração automática ───────────────────────────────────── */
  function autoGerar() {
    if (_editManual) return;  // não sobrescreve edição manual

    var nome = (_nomeInput && _nomeInput.value) || '';
    var cands = gerarCandidatos(nome);

    if (!cands.length) {
      _usuarioInput.value = '';
      setStatus('', '');
      return;
    }

    /* Checa os candidatos em sequência */
    checarSequencial(cands, 0);
  }

  function checarSequencial(cands, idx) {
    if (idx >= cands.length) {
      /* Todos os candidatos automáticos conflitam → habilita edição manual */
      habilitarEdicaoManual(cands[cands.length - 1]);
      return;
    }

    var cand = cands[idx];
    verificarDisponibilidade(cand, function (disponivel) {
      if (disponivel) {
        /* Candidato disponível → preenche e trava */
        _usuarioInput.value    = cand;
        _usuarioInput.readOnly = true;
        _editManual            = false;
        if (_lockIcon) _lockIcon.style.display = 'inline';
        setStatus('ok', '<i class="fa-solid fa-circle-check"></i> Disponível');
      } else {
        /* Tenta o próximo candidato */
        checarSequencial(cands, idx + 1);
      }
    });
  }

  function habilitarEdicaoManual(sugestao) {
    _editManual            = true;
    _usuarioInput.readOnly = false;
    _usuarioInput.value    = sugestao;
    _usuarioInput.focus();
    if (_lockIcon) _lockIcon.style.display = 'none';
    setStatus('warn',
      '<i class="fa-solid fa-pen"></i> '
      + 'Nome de usuário já existe. Edite manualmente.'
    );
    _ultimo = '';
  }

  /* ── Verificação de disponibilidade via API ───────────────── */
  function verificarDisponibilidade(usuario, callback) {
    if (!usuario || usuario === _ultimo) return;
    _ultimo = usuario;
    setStatus('loading', '<i class="fa-solid fa-spinner fa-spin"></i> Verificando...');

    fetch('/api/check_usuario?usuario=' + encodeURIComponent(usuario))
      .then(function (res) { return res.json(); })
      .then(function (data) {
        if (callback) {
          callback(data.disponivel);
        } else {
          /* Chamado de edição manual */
          if (data.disponivel) {
            setStatus('ok', '<i class="fa-solid fa-circle-check"></i> Disponível');
          } else {
            setStatus('error', '<i class="fa-solid fa-circle-xmark"></i> Já está em uso');
          }
        }
      })
      .catch(function () {
        if (callback) callback(true); /* Em caso de erro de rede, permite prosseguir */
        setStatus('', '');
      });
  }

  /* ── Status visual ────────────────────────────────────────── */
  function setStatus(tipo, html) {
    if (!_statusEl) return;
    _statusEl.innerHTML = html;
    _statusEl.className = 'usuario-status usuario-status--' + tipo;
  }

  /* ── Init ao carregar ─────────────────────────────────────── */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  /* Expõe para uso externo */
  window.UsuarioAuto = { autoGerar: autoGerar };

})();