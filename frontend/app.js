'use strict';
/**
 * Justicia Clew — frontend app.js
 * Replaces mock data from MOCKUP.html with real backend API calls.
 * textContent only — never innerHTML. Accessibility preserved from mockup.
 */

const API_BASE = ''; // same origin in production; override for dev if needed

// --- Spanish translations (preserved from mockup) ---
const es = {
  after: 'Compañero independiente de información para jurados',
  title: '¿Recibió una citación?',
  lede: 'Respuestas claras basadas en el sitio web público de su tribunal. Para la noche antes de presentarse.',
  start: 'Comience con su tribunal.',
  which: '¿Qué condado envió su citación?',
  county: 'Condado',
  select: 'Seleccione su condado',
  cant: '¿No encuentra su condado? Use el sitio web de su citación.',
  courtWeb: 'Sitio web del tribunal',
  continue: 'Continuar',
  companion: 'Un compañero, no el tribunal.',
  trust: 'Justicia Clew explica de manera independiente la información de sitios web públicos de los tribunales. No está afiliado ni respaldado por el tribunal. El tribunal sigue siendo la autoridad oficial.',
  checking: 'Consultando la información publicada por el tribunal',
  moment: 'Esto tomará solo un momento.',
  independent: 'Compañero independiente de información judicial',
  source: 'Información obtenida del sitio web público del Tribunal Superior de Santa Bárbara',
  checked: 'Muestra de fuente del prototipo · 10 de julio de 2026 a las 8:14 p. m.',
  whatChecked: 'Acerca de esta fuente',
  checkedExplain: 'El tribunal es propietario de la información original. Justicia Clew la explica de manera independiente. El tribunal no creó, revisó ni aprobó esta explicación. La versión conectada mostrará la página de origen y la hora real de consulta.',
  backCourt: '← Volver a seleccionar tribunal',
  need: '¿Qué necesita saber?',
  ownWords: 'Pregunte con sus propias palabras. No necesita lenguaje legal.',
  nearby: 'Tenga su citación cerca. Puede necesitar su identificación de jurado o fecha de presentación.',
  yourQ: 'Su pregunta sobre el servicio de jurado',
  findAnswer: 'Buscar mi respuesta',
  common: 'O elija una pregunta común',
  backQuestions: '← Volver a las preguntas',
  footerHead: 'Independiente y privado por diseño',
  footer: 'Información de sitios web públicos de tribunales, no asesoramiento legal. No está afiliado ni respaldado por el tribunal. No se requiere una cuenta. Justicia Clew no crea un historial de preguntas.'
};
const en = {};
document.querySelectorAll('[data-t]').forEach(el => { en[el.dataset.t] = el.textContent; });

// --- State ---
let lang = 'en';
let currentCounty = '';
const $ = id => document.getElementById(id);
const screens = ['landing', 'loading', 'questionScreen', 'answer'];

// --- Screen management ---
function show(id) {
  screens.forEach(s => $(s).hidden = s !== id);
  const panel = $(id);
  // Prefer the screen's own heading so screen readers announce it first;
  // headings carry tabindex="-1" in index.html to make this possible.
  const target = panel.querySelector('h1,h2') || panel.querySelector('button,input,select');
  if (target) target.focus();
}

// --- Reset the question input back to empty, disabled-ask state ---
function resetQuestionInput() {
  $('question').value = '';
  $('ask').disabled = true;
}

// --- Render text as separate paragraphs instead of one dense block.
// Still textContent only per node, never innerHTML. ---
function renderParagraphs(container, text) {
  String(text).split('\n').map(s => s.trim()).filter(Boolean).forEach(line => {
    const p = document.createElement('p');
    p.textContent = line;
    container.appendChild(p);
  });
}

// --- Language toggle ---
function translate(next) {
  lang = next;
  document.documentElement.lang = next;
  $('en').setAttribute('aria-pressed', String(next === 'en'));
  $('es').setAttribute('aria-pressed', String(next === 'es'));
  const dict = next === 'es' ? es : en;
  document.querySelectorAll('[data-t]').forEach(el => { el.textContent = dict[el.dataset.t]; });
  $('question').placeholder = $('question').dataset[next === 'es' ? 'placeholderEs' : 'placeholderEn'];
}

// --- Loading transition ---
function loadThen(id) {
  show('loading');
  setTimeout(() => show(id), 650);
}

// --- Render chips from backend ---
async function renderChips(county) {
  const container = $('chipsContainer');
  container.replaceChildren();
  try {
    const resp = await fetch(API_BASE + '/api/chips?county=' + encodeURIComponent(county));
    if (!resp.ok) throw new Error('Chips request failed: ' + resp.status);
    const chips = await resp.json();
    chips.forEach(chip => {
      const btn = document.createElement('button');
      btn.className = 'chip';
      btn.textContent = chip.question;
      btn.addEventListener('click', () => openAnswer(chip.question));
      container.appendChild(btn);
    });
  } catch (err) {
    // Error state: show a message, never a blank screen
    const msg = document.createElement('p');
    msg.className = 'intro';
    msg.textContent = lang === 'es'
      ? 'No se pudieron cargar las preguntas frecuentes. Escriba su pregunta arriba.'
      : 'Could not load common questions. Type your question above.';
    container.appendChild(msg);
  }
}

// --- Ask the backend and render the answer ---
async function openAnswer(question) {
  show('loading');
  $('asked').textContent = question;
  const host = $('result');
  host.replaceChildren();

  try {
    const resp = await fetch(API_BASE + '/api/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ county: currentCounty, question: question })
    });

    if (!resp.ok) {
      const errData = await resp.json().catch(() => null);
      throw new Error(errData?.detail?.message || 'Request failed: ' + resp.status);
    }

    const data = await resp.json();

    if (data.refusal) {
      // Refusal state
      const box = document.createElement('article');
      box.className = 'refusal';
      const state = document.createElement('span');
      state.className = 'state';
      state.textContent = lang === 'es' ? 'Se requiere decisión del tribunal' : 'Court decision required';
      box.appendChild(state);
      renderParagraphs(box, data.message);
      if (data.phone) {
        const call = document.createElement('a');
        call.className = 'call';
        call.href = 'tel:' + data.phone.replace(/[^+\d]/g, '');
        call.textContent = (lang === 'es' ? 'Llamar a Servicios de Jurado: ' : 'Call Jury Services: ') + data.phone;
        box.appendChild(call);
      }
      if (data.hours) {
        const hours = document.createElement('p');
        hours.className = 'hours';
        hours.textContent = data.hours;
        box.appendChild(hours);
      }
      host.appendChild(box);
    } else {
      // Answer state
      const answerBlock = document.createElement('article');
      answerBlock.className = 'answer-block';
      const ansLabel = document.createElement('span');
      ansLabel.className = 'label';
      ansLabel.textContent = lang === 'es' ? 'Lo que necesita saber' : 'What you need to know';
      answerBlock.appendChild(ansLabel);
      renderParagraphs(answerBlock, data.answer);
      host.appendChild(answerBlock);

      // Source quote
      if (data.quote) {
        const source = document.createElement('article');
        source.className = 'source';
        const srcLabel = document.createElement('span');
        srcLabel.className = 'label';
        srcLabel.textContent = data.source_label === 'statewide'
          ? (lang === 'es' ? 'Del Centro de Autoayuda de los Tribunales de California' : 'From the California Courts self-help center')
          : (lang === 'es' ? 'Del sitio web de su tribunal' : 'From your court\'s website');
        const quote = document.createElement('blockquote');
        quote.textContent = data.quote;
        source.append(srcLabel, quote);
        if (data.source_url) {
          const link = document.createElement('a');
          link.href = data.source_url;
          link.target = '_blank';
          link.rel = 'noopener noreferrer';
          link.textContent = lang === 'es' ? 'Ver página de origen' : 'View source page';
          source.appendChild(link);
        }
        host.appendChild(source);
      }

      // Last checked
      if (data.last_checked) {
        const checked = document.createElement('p');
        checked.className = 'intro';
        checked.textContent = (lang === 'es' ? 'Última revisión: ' : 'Last checked: ') + data.last_checked;
        host.appendChild(checked);
      }
    }

    // Announce to screen readers
    $('live').textContent = lang === 'es' ? 'Respuesta cargada.' : 'Answer loaded.';
    show('answer');

  } catch (err) {
    // Error state: meaningful message, never blank
    const errBox = document.createElement('article');
    errBox.className = 'unavailable';
    const state = document.createElement('span');
    state.className = 'state';
    state.textContent = lang === 'es' ? 'Servicio no disponible' : 'Service unavailable';
    const p = document.createElement('p');
    p.textContent = lang === 'es'
      ? 'No se pudo obtener una respuesta en este momento. Intente de nuevo en un momento, o llame a Servicios de Jurado directamente.'
      : 'Could not get an answer right now. Please try again in a moment, or call Jury Services directly.';
    errBox.append(state, p);

    const call = document.createElement('a');
    call.className = 'call';
    call.href = 'tel:+18058824530';
    call.textContent = lang === 'es' ? 'Llamar a Servicios de Jurado: (805) 882-4530' : 'Call Jury Services: (805) 882-4530';
    errBox.appendChild(call);

    const hours = document.createElement('p');
    hours.className = 'hours';
    hours.textContent = lang === 'es'
      ? 'Lunes a viernes, 8am-3pm, excepto días feriados. Línea automática disponible en cualquier momento: 877-544-5094.'
      : 'Mon-Fri, 8am-3pm, excluding holidays. Automated info line answers anytime: 877-544-5094.';
    errBox.appendChild(hours);

    host.appendChild(errBox);

    $('live').textContent = lang === 'es' ? 'Error al cargar respuesta.' : 'Error loading answer.';
    show('answer');
  }
}

// --- Event wiring ---
function ready() {
  $('continue').disabled = !($('county').value || $('url').value.trim());
}

$('county').addEventListener('change', ready);
$('url').addEventListener('input', ready);
$('question').addEventListener('input', () => {
  $('ask').disabled = !$('question').value.trim();
});
$('question').addEventListener('keydown', e => {
  if (e.key === 'Enter' && $('question').value.trim()) openAnswer($('question').value);
});
$('ask').addEventListener('click', () => openAnswer($('question').value));
$('reveal').addEventListener('click', () => {
  const open = $('urlField').hidden;
  $('urlField').hidden = !open;
  $('reveal').setAttribute('aria-expanded', String(open));
  if (open) $('url').focus();
});
$('continue').addEventListener('click', async () => {
  // Determine county from dropdown or URL
  if ($('county').value) {
    currentCounty = $('county').value;
  } else if ($('url').value.trim()) {
    // Resolve URL via backend
    try {
      const resp = await fetch(API_BASE + '/api/resolve-county', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: $('url').value.trim() })
      });
      if (!resp.ok) {
        const errData = await resp.json().catch(() => null);
        alert(errData?.detail?.message || 'Could not identify a county from that URL.');
        return;
      }
      const data = await resp.json();
      currentCounty = data.county;
    } catch (err) {
      alert('Could not reach the server. Please check your connection.');
      return;
    }
  }
  renderChips(currentCounty);
  loadThen('questionScreen');
});
$('homeBtn').addEventListener('click', () => {
  resetQuestionInput();
  show('landing');
});
document.querySelectorAll('.toLanding').forEach(b => b.addEventListener('click', () => {
  resetQuestionInput();
  show('landing');
}));
$('answerBack').addEventListener('click', () => {
  resetQuestionInput();
  show('questionScreen');
});
document.querySelectorAll('.sourceInfo').forEach(b => b.addEventListener('click', () => {
  const p = b.nextElementSibling;
  p.hidden = !p.hidden;
  b.setAttribute('aria-expanded', String(!p.hidden));
}));
$('en').addEventListener('click', () => translate('en'));
$('es').addEventListener('click', () => translate('es'));
