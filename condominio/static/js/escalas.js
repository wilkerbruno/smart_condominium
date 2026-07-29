/**
 * escalas.js — Lógica da página de Escalas de Trabalho
 * Lê configuração de sessão do elemento #escala-config via data attributes.
 * Arquivo JS 100% puro — sem nenhuma sintaxe Jinja.
 */

(function () {
  'use strict';

  /* ── Configuração vinda do template via data attributes ─────── */
  var _cfg       = document.getElementById('escala-config');
  var IS_SINDICO = _cfg ? _cfg.dataset.isSindico === 'true' : false;
  var USER_CARGO = _cfg ? (_cfg.dataset.userCargo || '')    : '';
  var USER_NOME  = _cfg ? (_cfg.dataset.userNome  || '')    : '';

  /* ── Dados dos funcionários ──────────────────────────────────── */
  var FUNCIONARIOS = [
    { id: 1, nome: 'Maria Santos',   cargo: 'Síndico',   cor: '#2563eb' },
    { id: 2, nome: 'José Silva',     cargo: 'Porteiro',  cor: '#7c3aed' },
    { id: 3, nome: 'Ana Oliveira',   cargo: 'Zelador',   cor: '#059669' },
    { id: 4, nome: 'Carlos Pereira', cargo: 'Segurança', cor: '#dc2626' },
    { id: 5, nome: 'Fernanda Lima',  cargo: 'Limpeza',   cor: '#d97706' },
  ];

  var DIAS_SEMANA = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'];
  var DIAS_LONG   = [
    'Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira',
    'Quinta-feira', 'Sexta-feira', 'Sábado'
  ];

  /* ── Estado ─────────────────────────────────────────────────── */
  var escalaData    = {};
  var semanaOffset  = 0;
  var searchQuery   = '';
  var modalFunc     = null;
  var modalDia      = null;
  var modalTurnoSel = '';

  /* ══════════════════════════════════════════════════════════════
     HELPERS
  ══════════════════════════════════════════════════════════════ */

  function getSemana() {
    var hoje = new Date();
    var dow  = hoje.getDay();
    var seg  = new Date(hoje);
    seg.setDate(hoje.getDate() - (dow === 0 ? 6 : dow - 1) + semanaOffset * 7);
    seg.setHours(0, 0, 0, 0);
    var dias = [];
    for (var i = 0; i < 7; i++) {
      var d = new Date(seg);
      d.setDate(seg.getDate() + i);
      dias.push(d);
    }
    return dias;
  }

  function fmtDate(d) {
    return d.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' });
  }

  function initials(nome) {
    return nome.split(' ').slice(0, 2).map(function (p) { return p[0]; }).join('').toUpperCase();
  }

  function key(funcId, diaIdx) { return funcId + '_' + diaIdx; }

  function turnoInfo(t) {
    var map = {
      manha:  { label: 'Manhã',  cls: 'turno-manha',  icon: '☀️'  },
      tarde:  { label: 'Tarde',  cls: 'turno-tarde',  icon: '🌤️' },
      noite:  { label: 'Noite',  cls: 'turno-noite',  icon: '🌙'  },
      folga:  { label: 'Folga',  cls: 'turno-folga',  icon: '🏖️' },
      ferias: { label: 'Férias', cls: 'turno-ferias', icon: '🌴'  },
    };
    return map[t] || null;
  }

  /* ══════════════════════════════════════════════════════════════
     ESCALA PADRÃO
  ══════════════════════════════════════════════════════════════ */

  function initEscala() {
    var def = {
      1: ['manha', 'manha', 'manha', 'manha', 'manha', '',      ''      ],
      2: ['tarde', 'tarde', 'tarde', 'tarde', 'tarde', '',      ''      ],
      3: ['manha', 'manha', 'manha', 'manha', 'manha', 'folga', ''      ],
      4: ['noite', 'noite', 'noite', 'noite', 'noite', '',      'folga' ],
      5: ['manha', 'manha', 'manha', 'manha', '',      '',      ''      ],
    };
    var horas = {
      manha:  ['08:00', '17:00'],
      tarde:  ['13:00', '22:00'],
      noite:  ['22:00', '06:00'],
      folga:  ['–', '–'],
      ferias: ['–', '–'],
    };
    FUNCIONARIOS.forEach(function (f) {
      def[f.id].forEach(function (t, d) {
        if (t) {
          escalaData[key(f.id, d)] = {
            turno: t, entrada: horas[t][0], saida: horas[t][1], obs: '',
          };
        }
      });
    });
  }

  /* ══════════════════════════════════════════════════════════════
     GRADE SEMANAL
  ══════════════════════════════════════════════════════════════ */

  function renderEscalaTable() {
    var dias  = getSemana();
    var hoje  = new Date();
    hoje.setHours(0, 0, 0, 0);
    var q = searchQuery.toLowerCase().trim();

    /* Cabeçalho */
    var headHtml = '<tr><th>Funcionário</th>';
    dias.forEach(function (d, i) {
      var isHoje = d.getTime() === hoje.getTime();
      headHtml += '<th' + (isHoje ? ' style="background:#1d4ed8"' : '') + '>'
        + DIAS_SEMANA[(i + 1) % 7]
        + '<br><small style="font-weight:400;opacity:.7">' + fmtDate(d) + '</small></th>';
    });
    headHtml += '</tr>';
    document.getElementById('escalaHead').innerHTML = headHtml;

    /* Filtra funcionários pela busca */
    var filtered = q
      ? FUNCIONARIOS.filter(function (f) {
          return f.nome.toLowerCase().indexOf(q) !== -1
              || f.cargo.toLowerCase().indexOf(q) !== -1;
        })
      : FUNCIONARIOS;

    /* Corpo */
    var bodyHtml = '';
    if (filtered.length === 0) {
      bodyHtml = '<tr><td colspan="8" style="text-align:center;padding:40px;color:var(--text-muted)">'
        + '<i class="fa-solid fa-magnifying-glass" style="font-size:1.4rem;display:block;margin-bottom:8px;opacity:.4"></i>'
        + 'Nenhum funcionário encontrado para "<strong>' + q + '</strong>"'
        + '</td></tr>';
    } else {
      filtered.forEach(function (f) {
        var isMe = USER_NOME && USER_NOME === f.nome;
        bodyHtml += '<tr' + (isMe ? ' class="minha-linha"' : '') + '>'
          + '<td><div class="escala-func-cell">'
            + '<div class="func-avatar" style="background:' + f.cor + ';width:28px;height:28px;font-size:.6rem">'
              + initials(f.nome)
            + '</div>'
            + '<div>'
              + '<div style="font-size:.82rem;font-weight:600">' + f.nome
                + (isMe ? ' <span class="eu-tag">Você</span>' : '')
              + '</div>'
              + '<div style="font-size:.68rem;color:var(--text-muted)">' + f.cargo + '</div>'
            + '</div>'
          + '</div></td>';

        dias.forEach(function (d, i) {
          var diaIdx = (i + 1) % 7;
          var k      = key(f.id, diaIdx);
          var entry  = escalaData[k];
          var info   = entry ? turnoInfo(entry.turno) : null;

          bodyHtml += '<td class="turno-cell">';

          if (IS_SINDICO) {
            if (info) {
              bodyHtml += '<span class="turno-badge ' + info.cls + '"'
                + ' onclick="EscalaApp.openModal(' + f.id + ',' + diaIdx + ',\'' + fmtDate(d) + '\')"'
                + ' title="Clique para editar">'
                + info.icon + ' ' + info.label
                + (entry.entrada !== '–'
                    ? '<br><small style="font-weight:400;font-size:.65rem">' + entry.entrada + '–' + entry.saida + '</small>'
                    : '')
                + '</span>';
            } else {
              bodyHtml += '<button class="add-turno-btn"'
                + ' onclick="EscalaApp.openModal(' + f.id + ',' + diaIdx + ',\'' + fmtDate(d) + '\')"'
                + ' title="Adicionar turno"><i class="fa-solid fa-plus"></i></button>';
            }
          } else {
            if (info) {
              bodyHtml += '<span class="turno-badge ' + info.cls + ' turno-readonly">'
                + info.icon + ' ' + info.label
                + (entry.entrada !== '–'
                    ? '<br><small style="font-weight:400;font-size:.65rem">' + entry.entrada + '–' + entry.saida + '</small>'
                    : '')
                + '</span>';
            } else {
              bodyHtml += '<span class="turno-badge turno-vazio turno-readonly">–</span>';
            }
          }

          bodyHtml += '</td>';
        });

        bodyHtml += '</tr>';
      });
    }

    document.getElementById('escalaBody').innerHTML = bodyHtml;

    /* Labels e stats */
    var tituloEl = document.getElementById('semanaTitle');
    if (tituloEl) { tituloEl.textContent = fmtDate(dias[0]) + ' – ' + fmtDate(dias[6]); }

    var semanaEl = document.getElementById('statSemana');
    if (semanaEl) {
      semanaEl.textContent = dias[0].toLocaleDateString('pt-BR', { month: 'short', year: 'numeric' });
    }

    var dow  = hoje.getDay();
    var trab = FUNCIONARIOS.filter(function (f) {
      var e = escalaData[key(f.id, dow)];
      return e && e.turno !== 'folga' && e.turno !== 'ferias' && e.turno;
    }).length;
    var ativosEl = document.getElementById('statAtivos');
    var folgaEl  = document.getElementById('statFolga');
    if (ativosEl) { ativosEl.textContent = trab; }
    if (folgaEl)  { folgaEl.textContent  = FUNCIONARIOS.length - trab; }

    /* Footer da tabela */
    var footerEl = document.getElementById('tableFooterInfo');
    if (footerEl) {
      footerEl.textContent = q
        ? 'Exibindo ' + filtered.length + ' de ' + FUNCIONARIOS.length + ' funcionários'
        : FUNCIONARIOS.length + ' funcionários';
    }

    /* Botão limpar busca */
    var clearBtn = document.getElementById('btnClearSearch');
    if (clearBtn) { clearBtn.style.display = q ? 'flex' : 'none'; }

    /* Barra de resultado da busca */
    var resultBar = document.getElementById('searchResultBar');
    if (resultBar) {
      if (q) {
        resultBar.style.display = 'flex';
        var strong = resultBar.querySelector('strong');
        if (strong) { strong.textContent = q; }
      } else {
        resultBar.style.display = 'none';
      }
    }
  }

  /* ══════════════════════════════════════════════════════════════
     MINHA ESCALA (funcionário logado)
  ══════════════════════════════════════════════════════════════ */

  function renderMinhaEscala() {
    var box = document.getElementById('minhaEscalaList');
    if (!box) { return; }

    var f = null;
    for (var i = 0; i < FUNCIONARIOS.length; i++) {
      if (FUNCIONARIOS[i].nome === USER_NOME) { f = FUNCIONARIOS[i]; break; }
    }
    if (!f) {
      box.innerHTML = '<p style="padding:16px;color:var(--text-muted)">Funcionário não identificado.</p>';
      return;
    }

    var nomeEl = document.getElementById('minhaEscalaNome');
    if (nomeEl) {
      nomeEl.innerHTML = '<div class="func-avatar" style="background:' + f.cor
        + ';width:28px;height:28px;font-size:.6rem;display:inline-flex;vertical-align:middle;margin-right:8px">'
        + initials(f.nome) + '</div>'
        + f.nome + ' <span style="font-size:.78rem;color:var(--text-muted);font-weight:400">— ' + f.cargo + '</span>';
    }

    var dias  = getSemana();
    var hoje  = new Date(); hoje.setHours(0, 0, 0, 0);
    var html  = '';

    dias.forEach(function (d, i) {
      var diaIdx = (i + 1) % 7;
      var entry  = escalaData[key(f.id, diaIdx)];
      var info   = entry ? turnoInfo(entry.turno) : null;
      var isHoje = d.getTime() === hoje.getTime();

      html += '<div class="escala-dia-row' + (isHoje ? ' hoje' : '') + '">'
        + '<div class="dia-label' + (isHoje ? ' hoje-label' : '') + '">' + DIAS_SEMANA[diaIdx] + '</div>'
        + '<div class="dia-data'  + (isHoje ? ' hoje-data'  : '') + '">' + d.getDate() + '</div>'
        + '<div class="dia-info">';

      if (info) {
        html += '<div class="dia-turno-text">' + info.icon + ' ' + info.label + '</div>'
          + (entry.entrada !== '–'
              ? '<div class="dia-horario-text"><i class="fa-regular fa-clock"></i>' + entry.entrada + ' – ' + entry.saida + '</div>'
              : '<div class="dia-horario-text" style="color:var(--text-muted)">Dia livre</div>');
        if (entry.obs) {
          html += '<div style="font-size:.7rem;color:var(--brand);margin-top:2px">'
            + '<i class="fa-solid fa-note-sticky"></i> ' + entry.obs + '</div>';
        }
      } else {
        html += '<div class="dia-turno-text" style="color:var(--text-muted)">– Não definido</div>';
      }

      html += '</div></div>';
    });

    box.innerHTML = html;
  }

  /* ══════════════════════════════════════════════════════════════
     MODAL DE EDIÇÃO (síndico)
  ══════════════════════════════════════════════════════════════ */

  function openModal(funcId, diaIdx, dataStr) {
    if (!IS_SINDICO) { return; }
    var f = null;
    for (var i = 0; i < FUNCIONARIOS.length; i++) {
      if (FUNCIONARIOS[i].id === funcId) { f = FUNCIONARIOS[i]; break; }
    }
    if (!f) { return; }

    modalFunc = funcId; modalDia = diaIdx; modalTurnoSel = '';
    document.getElementById('modalTitle').textContent    = 'Definir Turno — ' + f.nome;
    document.getElementById('modalSubtitle').textContent = DIAS_LONG[diaIdx] + ' · ' + dataStr;

    var entry = escalaData[key(funcId, diaIdx)];
    if (entry) {
      modalTurnoSel = entry.turno;
      document.getElementById('modalEntrada').value = entry.entrada !== '–' ? entry.entrada : '08:00';
      document.getElementById('modalSaida').value   = entry.saida   !== '–' ? entry.saida   : '17:00';
      document.getElementById('modalObs').value     = entry.obs || '';
    } else {
      document.getElementById('modalEntrada').value = '08:00';
      document.getElementById('modalSaida').value   = '17:00';
      document.getElementById('modalObs').value     = '';
    }

    document.querySelectorAll('.turno-opt').forEach(function (o) {
      o.classList.toggle('selected', o.dataset.turno === modalTurnoSel);
    });
    toggleHorarioFields(modalTurnoSel);
    document.getElementById('turnoModal').classList.add('open');
  }

  function closeModal() {
    var modal = document.getElementById('turnoModal');
    if (modal) { modal.classList.remove('open'); }
  }

  function selectTurno(t) {
    if (!IS_SINDICO) { return; }
    modalTurnoSel = t;
    document.querySelectorAll('.turno-opt').forEach(function (o) {
      o.classList.toggle('selected', o.dataset.turno === t);
    });
    toggleHorarioFields(t);
  }

  function toggleHorarioFields(t) {
    var el = document.getElementById('horarioFields');
    if (!el) { return; }
    el.style.display = (t !== 'folga' && t !== 'ferias' && t !== '') ? 'grid' : 'none';
  }

  function confirmarTurno() {
    if (!IS_SINDICO || modalFunc === null) { return; }
    var k = key(modalFunc, modalDia);
    if (modalTurnoSel === '') {
      delete escalaData[k];
    } else {
      var livre = (modalTurnoSel === 'folga' || modalTurnoSel === 'ferias');
      escalaData[k] = {
        turno:   modalTurnoSel,
        entrada: livre ? '–' : document.getElementById('modalEntrada').value,
        saida:   livre ? '–' : document.getElementById('modalSaida').value,
        obs:     document.getElementById('modalObs').value,
      };
    }
    closeModal();
    renderEscalaTable();
    renderMinhaEscala();
    showToast('Turno salvo com sucesso!', 'success');
  }

  /* ══════════════════════════════════════════════════════════════
     DOWNLOAD PDF — minha escala
  ══════════════════════════════════════════════════════════════ */

  function downloadMinhaEscalaPDF() {
    /* Abre a página de visualização já filtrada pelo nome do funcionário */
    var url = '/escalas/visualizacao?nome=' + encodeURIComponent(USER_NOME)
            + '&cargo=' + encodeURIComponent(USER_CARGO);
    var win = window.open(url, '_blank');
    /* Após carregar, aciona o print nativo (browser salva como PDF) */
    if (win) {
      win.addEventListener('load', function () {
        setTimeout(function () { win.print(); }, 600);
      });
    }
  }

  function downloadEscalaPDF() {
    /* Abre a visualização com toda a equipe */
    var url = '/escalas/visualizacao';
    window.open(url, '_blank');
  }

  /* ══════════════════════════════════════════════════════════════
     ABRIR VISUALIZAÇÃO
  ══════════════════════════════════════════════════════════════ */

  function abrirVisualizacao() {
    var url = '/escalas/visualizacao';
    if (USER_NOME) { url += '?nome=' + encodeURIComponent(USER_NOME); }
    window.open(url, '_blank');
  }

  /* ══════════════════════════════════════════════════════════════
     TOAST
  ══════════════════════════════════════════════════════════════ */

  function showToast(msg, type) {
    var toast = document.getElementById('toast');
    if (!toast) { return; }
    toast.className = 'toast toast-' + (type || 'success');
    document.getElementById('toastMsg').textContent = msg;
    var icon = toast.querySelector('i');
    if (icon) {
      icon.className = type === 'error' ? 'fa-solid fa-circle-xmark' : 'fa-solid fa-circle-check';
    }
    toast.classList.add('show');
    setTimeout(function () { toast.classList.remove('show'); }, 3000);
  }

  /* ══════════════════════════════════════════════════════════════
     EVENTOS DOM
  ══════════════════════════════════════════════════════════════ */

  document.addEventListener('DOMContentLoaded', function () {
    /* Modal: fechar clicando fora */
    var modal = document.getElementById('turnoModal');
    if (modal) {
      modal.addEventListener('click', function (e) {
        if (e.target === modal) { closeModal(); }
      });
    }

    /* Botão salvar escala */
    var btnSalvar = document.getElementById('btnSalvarEscala');
    if (btnSalvar) {
      btnSalvar.addEventListener('click', function () {
        showToast('Escala salva com sucesso! ✓', 'success');
      });
    }

    /* Botão download PDF da escala inteira */
    var btnPdfEscala = document.getElementById('btnDownloadEscalaPdf');
    if (btnPdfEscala) {
      btnPdfEscala.addEventListener('click', downloadEscalaPDF);
    }

    /* Botão download PDF da minha escala */
    var btnPdfMinha = document.getElementById('btnDownloadPdf');
    if (btnPdfMinha) {
      btnPdfMinha.addEventListener('click', downloadMinhaEscalaPDF);
    }
  });

  /* ══════════════════════════════════════════════════════════════
     API PÚBLICA
  ══════════════════════════════════════════════════════════════ */

  window.EscalaApp = {
    prevSemana:      function ()   { semanaOffset--; renderEscalaTable(); renderMinhaEscala(); },
    nextSemana:      function ()   { semanaOffset++; renderEscalaTable(); renderMinhaEscala(); },
    setView:         function (v, btn) {
      document.querySelectorAll('.view-tab').forEach(function (b) { b.classList.remove('active'); });
      btn.classList.add('active');
    },
    abrirVisualizacao: abrirVisualizacao,
    filterTabela:    function (q) { searchQuery = q; renderEscalaTable(); },
    clearSearch:     function ()  {
      searchQuery = '';
      var input = document.getElementById('funcSearchInput');
      if (input) { input.value = ''; }
      renderEscalaTable();
    },
    openModal:      openModal,
    closeModal:     closeModal,
    selectTurno:    selectTurno,
    confirmarTurno: confirmarTurno,
  };

  /* ══════════════════════════════════════════════════════════════
     INIT
  ══════════════════════════════════════════════════════════════ */

  initEscala();
  renderEscalaTable();
  renderMinhaEscala();

  var totalEl = document.getElementById('statTotal');
  if (totalEl) { totalEl.textContent = FUNCIONARIOS.length; }

})();