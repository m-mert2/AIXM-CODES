let curScenario = null;
let tRun=0, tAccept=0, tReject=0;

// State layout configs for visual PDA
function getStateLayout(feature, states) {
  // Simple linear layout for most, special for complex ones
  const order = ['q0','q1','q2','q3','q_body','q_accept'];
  const rejectStates = states.filter(s => s.includes('reject'));
  const acceptStates = states.filter(s => s.includes('accept'));
  const mainStates = states.filter(s => !s.includes('reject') && !s.includes('accept'));

  // Sort main states in logical order
  const sorted = mainStates.sort((a,b) => {
    const ai = order.indexOf(a) >= 0 ? order.indexOf(a) : 99;
    const bi = order.indexOf(b) >= 0 ? order.indexOf(b) : 99;
    return ai - bi;
  });

  return [...sorted, ...acceptStates, ...rejectStates];
}

async function loadScenario(id) {
  document.querySelectorAll('.sitem').forEach(e=>e.classList.remove('active'));
  document.getElementById('item-'+id).classList.add('active');
  const res = await fetch('/api/scenario/'+id);
  curScenario = await res.json();
  document.getElementById('s-title').textContent = 'Senaryo '+id+': '+curScenario.baslik;
  document.getElementById('s-desc').textContent = curScenario.aciklama;
  document.getElementById('run-btn').disabled = false;
  document.getElementById('prog').style.width = '0%';

  const area = document.getElementById('content');
  area.innerHTML = '';
  curScenario.features.forEach(f => {
    area.appendChild(buildCard(f, null));
  });
}

async function runScenario() {
  if (!curScenario) return;
  const btn = document.getElementById('run-btn');
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span> Doğrulanıyor...';

  const area = document.getElementById('content');
  area.innerHTML = '';
  const total = curScenario.features.length;
  let done = 0;

  let data;
  try {
    const res = await fetch('/api/validate_scenario/'+curScenario.id);
    data = await res.json();
  } catch(e) {
    btn.disabled=false;
    btn.innerHTML='<span>▶</span> Doğrulamayı Çalıştır';
    document.getElementById('content').innerHTML = `<div style="color:#ff6d40;padding:20px">❌ Sunucuya bağlanılamadı: ${e.message}<br><small style="color:#6a8ab0">Flask sunucusu çalışıyor mu? python app.py</small></div>`;
    return;
  }

  for (const r of data.results) {
    const card = buildCard(r, r.result);
    area.appendChild(card);
    done++;
    document.getElementById('prog').style.width = (done/total*100)+'%';
    // Animate PDA flow
    await animatePDA(card, r, r.result);
    await sleep(300);
  }

  await sleep(200);
  const fin = document.createElement('div');
  fin.className = 'final '+(data.all_accepted?'fa':'fr');
  fin.innerHTML = `<div class="fi">${data.all_accepted?'✅':'❌'}</div><div class="ft">${curScenario.sonuc_mesaji}</div>`;
  area.appendChild(fin);
  fin.scrollIntoView({behavior:'smooth'});

  tRun++; if(data.all_accepted) tAccept++; else tReject++;
  document.getElementById('tr').textContent=tRun;
  document.getElementById('ta').textContent=tAccept;
  document.getElementById('tj').textContent=tReject;

  const badge = document.getElementById('badge-'+curScenario.id);
  badge.className = 'sbadge '+(data.all_accepted?'ok':'fail');

  btn.disabled=false;
  btn.innerHTML='<span>▶</span> Tekrar Çalıştır';
}

function buildCard(f, result) {
  const card = document.createElement('div');
  card.className = 'fcard';
  card.id = 'card-'+f.feature+'-'+Math.random().toString(36).slice(2);

  const accepted = result ? result.accepted : null;
  const badgeCls = result ? (accepted?'ba':'br') : 'bw';
  const badgeTxt = result ? (accepted?'✅ KABUL':'❌ RET') : '⏳ Bekliyor';

  // Token HTML
  let toksHtml = f.tokens.map((t,i) =>
    `<span class="tok" id="tok-${card.id}-${i}">${t}</span>`
  ).join('');

  // PDA visual nodes - extract states from result steps
  let pdaHtml = '';
  if (result && result.steps.length > 0) {
    pdaHtml = buildPDAVisual(f.feature, result);
  }

  // Stack display
  let stackHtml = `<div class="stack-display">
    <span class="stack-lbl">Yığın:</span>
    <div class="stack-items" id="stack-${card.id}">
      <span class="stack-empty">[ Z0 ]</span>
    </div>
  </div>`;

  // Step log table
  let logHtml = '';
  if (result && result.steps.length > 0) {
    let rows = result.steps.map((s,i) => {
      const rc = s.to==='q_accept'?'ra':s.to==='q_reject'?'rr':'';
      const tc = s.to==='q_accept'?'a':s.to==='q_reject'?'r':'';
      const opCls = s.stack_op.startsWith('push')?'op-push':s.stack_op==='pop'?'op-pop':'op-none';
      const stk = s.stack.map(x=>`<span class="stack-el">${x}</span>`).join('');
      return `<tr class="${rc}">
        <td style="color:#4a6a8a">${i+1}</td>
        <td><span class="schip">${s.from}</span></td>
        <td style="color:#c0d8f8;font-size:0.72rem">${s.token}</td>
        <td><span class="schip ${tc}">${s.to}</span></td>
        <td class="${opCls}">${s.stack_op}</td>
        <td>${stk}</td>
      </tr>`;
    }).join('');

    logHtml = `<div class="log-section">
      <div class="log-lbl">Durum Geçiş Adımları</div>
      <table class="log-table">
        <thead><tr><th>#</th><th>Durum</th><th>Token</th><th>Sonraki</th><th>Yığın Op.</th><th>Yığın</th></tr></thead>
        <tbody>${rows}</tbody>
      </table>
    </div>`;
  }

  card.innerHTML = `
    <div class="fcard-hdr">
      <span class="fname">&lt;aixm:${f.feature}&gt;</span>
      <span class="fdesc">${f.aciklama}</span>
      <span class="rbadge ${badgeCls}" id="rbadge-${card.id}">${badgeTxt}</span>
    </div>
    <div class="tflow">
      <div class="tlbl">Giriş Token Dizisi</div>
      <div class="tokens" id="toks-${card.id}">${toksHtml}</div>
    </div>
    ${pdaHtml ? `<div class="pda-section"><div class="pda-lbl">PDA Durum Akışı</div><div class="pda-canvas-wrap" id="pda-${card.id}">${pdaHtml}</div></div>` : ''}
    ${stackHtml}
    ${logHtml}
  `;

  // store card id on element for animation
  card.dataset.cardId = card.id;
  card.dataset.feature = f.feature;
  return card;
}

function buildPDAVisual(feature, result) {
  // Collect unique states in order from steps
  const stateOrder = [];
  const seen = new Set();
  // Always start with q0
  stateOrder.push('q0');
  seen.add('q0');

  result.steps.forEach(s => {
    if (!seen.has(s.from)) { stateOrder.push(s.from); seen.add(s.from); }
    if (!seen.has(s.to)) { stateOrder.push(s.to); seen.add(s.to); }
  });

  // Separate main flow from reject
  const rejectStates = stateOrder.filter(s => s.includes('reject'));
  const mainStates = stateOrder.filter(s => !s.includes('reject'));

  // Build main row
  let html = '<div class="pda-row">';

  mainStates.forEach((state, i) => {
    const isAccept = state.includes('accept');
    const isStart = state === 'q0';
    let nodeCls = 'state-node';
    if (isStart) nodeCls += ' start-node';
    if (isAccept) nodeCls += ' accept-node';

    let sublabel = '';
    if (isStart) sublabel = 'başlangıç';
    if (isAccept) sublabel = 'kabul';

    html += `<div class="${nodeCls}" id="sn-${feature}-${state}" data-state="${state}">
      <span class="state-label">${state}</span>
      ${sublabel ? `<span class="state-sublabel">${sublabel}</span>` : ''}
    </div>`;

    // Arrow to next (if not last)
    if (i < mainStates.length - 1) {
      // Find token for this transition
      const step = result.steps.find(s => s.from === state && !s.to.includes('reject'));
      const token = step ? shortToken(step.token) : '→';
      html += `<div class="arrow">
        <span class="arrow-token" id="at-${feature}-${state}">${token}</span>
        <div class="arrow-line" id="al-${feature}-${state}"></div>
      </div>`;
    }
  });

  html += '</div>';

  // Reject branch (below, with downward arrow from where reject happens)
  if (rejectStates.length > 0) {
    const rejectStep = result.steps.find(s => s.to.includes('reject'));
    const fromState = rejectStep ? rejectStep.from : '';
    html += `<div style="display:flex;align-items:center;gap:8px;margin-top:10px;padding-left:20px">
      <span style="font-size:0.65rem;color:#ff6d40">↳ ${fromState} →</span>
      <div class="state-node reject-node" id="sn-${feature}-q_reject" data-state="q_reject" style="width:60px;height:60px">
        <span class="state-label">q_reject</span>
        <span class="state-sublabel">ret</span>
      </div>
    </div>`;
  }

  return html;
}

function shortToken(token) {
  return token.replace('aixm:','').replace('gml:','').substring(0,14);
}

async function animatePDA(card, f, result) {
  if (!result || !result.steps) return;

  const feature = f.feature;
  // Reset all nodes
  card.querySelectorAll('.state-node').forEach(n => {
    n.classList.remove('ACTIVE','VISITED','REJECTED');
  });

  // Activate q0
  const q0 = card.querySelector(`[data-state="q0"]`);
  if (q0) q0.classList.add('ACTIVE');
  await sleep(300);

  for (let i = 0; i < result.steps.length; i++) {
    const step = result.steps[i];
    const tokEl = card.querySelector(`#tok-${card.id}-${i}`);

    // Highlight token
    if (tokEl) {
      tokEl.classList.add('active');
      await sleep(150);
    }

    // Move from → to
    const fromNode = card.querySelector(`[data-state="${step.from}"]`);
    const toNode = card.querySelector(`[data-state="${step.to}"]`);
    const arrowLine = card.querySelector(`#al-${feature}-${step.from}`);
    const arrowTok = card.querySelector(`#at-${feature}-${step.from}`);

    if (fromNode) {
      fromNode.classList.remove('ACTIVE');
      fromNode.classList.add('VISITED');
    }
    if (arrowLine) {
      arrowLine.classList.add('active-arrow');
      if (arrowTok) arrowTok.classList.add('active-tok');
    }
    if (toNode) {
      toNode.classList.add('ACTIVE');
      if (step.to.includes('reject')) toNode.classList.add('REJECTED');
    }

    // Update stack display
    updateStackDisplay(card, step.stack);

    await sleep(350);

    // Finalize token style
    if (tokEl) {
      tokEl.classList.remove('active');
      tokEl.classList.add(step.to.includes('reject') ? 'err' : 'ok');
    }
    if (arrowLine) {
      arrowLine.classList.remove('active-arrow');
      arrowLine.classList.add('done-arrow');
      if (arrowTok) { arrowTok.classList.remove('active-tok'); arrowTok.classList.add('done-tok'); }
    }
  }

  // Final node state
  const lastStep = result.steps[result.steps.length-1];
  if (lastStep) {
    const finalNode = card.querySelector(`[data-state="${lastStep.to}"]`);
    if (finalNode) {
      finalNode.classList.remove('ACTIVE');
      finalNode.classList.add(lastStep.to.includes('accept') ? 'VISITED' : 'REJECTED');
    }
  }

  // Update badge
  const badge = card.querySelector('[id^="rbadge-"]');
  if (badge) {
    badge.className = 'rbadge '+(result.accepted?'ba':'br');
    badge.textContent = result.accepted ? '✅ KABUL' : '❌ RET';
  }
}

function updateStackDisplay(card, stack) {
  const el = card.querySelector('[id^="stack-"]');
  if (!el) return;
  if (stack.length === 0 || (stack.length === 1 && stack[0] === 'Z0')) {
    el.innerHTML = '<span class="stack-empty">[ Z0 ]</span>';
    return;
  }
  el.innerHTML = stack.map((s,i) =>
    `<span class="stack-el ${i === stack.length-1 ? 'new' : ''}">${s}</span>`
  ).join('<span style="color:#3a5a7a;font-size:0.7rem">←</span>');
}

function switchTab(tab) {
  ['scenario','xml','gen','map'].forEach(t => {
    document.getElementById(`tab-${t}`).classList.toggle('active', t===tab);
    document.getElementById(`panel-${t}`).style.display = t===tab ? 'flex' : 'none';
  });
  const container = document.getElementById('main-container');
  container.classList.toggle('map-mode', tab==='map');
  document.getElementById('sidebar-scenarios').style.display = (tab==='map' || tab==='gen') ? 'none' : '';
  document.getElementById('sidebar-gen').style.display = tab==='gen' ? '' : 'none';
  // Canvas'ı sadece harita sekmesinde göster
  const canvas = document.getElementById('map-canvas');
  if (canvas) canvas.style.display = tab === 'map' ? 'block' : 'none';
  if (tab==='map') {
    // İki frame bekle: ilki display değişimi, ikincisi layout reflow
    requestAnimationFrame(() => requestAnimationFrame(() => {
      if (!_canvasMapLoaded) { _canvasMapLoaded = true; loadMapFeatures(); }
      else MapEngine.redraw();
    }));
  }
  if (tab==='gen') loadGeneratorScenarios();
}

const XML_EXAMPLES = {
  airspace_ok: `<aixm:Airspace>
  <gml:identifier>d6edcaf5-929e-4a8b-8b84-donlon</gml:identifier>
  <gml:boundedBy>
    <gml:Envelope srsName="urn:ogc:def:crs:EPSG::4326">
      <gml:lowerCorner>48.5 11.0</gml:lowerCorner>
      <gml:upperCorner>49.5 12.5</gml:upperCorner>
    </gml:Envelope>
  </gml:boundedBy>
  <aixm:timeSlice>
    <aixm:AirspaceTimeSlice>
      <gml:validTime/>
      <aixm:interpretation>BASELINE</aixm:interpretation>
    </aixm:AirspaceTimeSlice>
  </aixm:timeSlice>
</aixm:Airspace>`,

  airspace_err: `<aixm:Airspace>
  <aixm:timeSlice>
    <aixm:AirspaceTimeSlice>
      <gml:validTime/>
    </aixm:AirspaceTimeSlice>
  </aixm:timeSlice>
</aixm:Airspace>`,

  runway_ok: `<aixm:Runway>
  <gml:identifier>rwy-donlon-09L</gml:identifier>
  <aixm:timeSlice>
    <aixm:RunwayTimeSlice>
      <gml:validTime/>
      <aixm:interpretation>BASELINE</aixm:interpretation>
    </aixm:RunwayTimeSlice>
  </aixm:timeSlice>
  <aixm:designator>09L/27R</aixm:designator>
  <aixm:type>RWY</aixm:type>
  <aixm:nominalLength uom="M">3200</aixm:nominalLength>
  <aixm:nominalWidth uom="M">45</aixm:nominalWidth>
  <aixm:surfaceProperties>
    <aixm:SurfaceCharacteristics>
      <aixm:composition>ASPH</aixm:composition>
    </aixm:SurfaceCharacteristics>
  </aixm:surfaceProperties>
  <aixm:associatedAirportHeliport xlink:href="donlon-airport"/>
</aixm:Runway>`,

  runway_err: `<aixm:Runway>
  <gml:identifier>rwy-donlon-09L</gml:identifier>
  <aixm:nominalLength uom="M">3200</aixm:nominalLength>
  <aixm:nominalWidth uom="M">45</aixm:nominalWidth>
</aixm:Runway>`,

  ils_ok: `<aixm:Localizer>
  <gml:identifier>loc-donlon-ils09L</gml:identifier>
  <aixm:timeSlice>
    <aixm:LocalizerTimeSlice>
      <gml:validTime/>
      <aixm:interpretation>BASELINE</aixm:interpretation>
    </aixm:LocalizerTimeSlice>
  </aixm:timeSlice>
  <aixm:frequency uom="MHZ">110.1</aixm:frequency>
  <aixm:course uom="DEG">091</aixm:course>
  <aixm:location>
    <aixm:ElevatedPoint srsName="urn:ogc:def:crs:EPSG::4326">
      <gml:pos>52.3721 -031.9310</gml:pos>
    </aixm:ElevatedPoint>
  </aixm:location>
  <aixm:servedRunwayDirection xlink:href="donlon-rwy09L"/>
</aixm:Localizer>`,

  navaid_err: `<aixm:Navaid>
  <gml:identifier>nav-don-vor</gml:identifier>
  <aixm:designator>DON</aixm:designator>
  <aixm:name>DONLON VOR</aixm:name>
</aixm:Navaid>`,

  vtx_ok: `<aixm:VerticalStructure>
  <gml:identifier>vs-donlon-tower</gml:identifier>
  <aixm:timeSlice>
    <aixm:VerticalStructureTimeSlice>
      <gml:validTime/>
      <aixm:interpretation>BASELINE</aixm:interpretation>
    </aixm:VerticalStructureTimeSlice>
  </aixm:timeSlice>
  <aixm:name>DONLON CONTROL TOWER</aixm:name>
  <aixm:type>BUILDING</aixm:type>
  <aixm:lighted>YES</aixm:lighted>
  <aixm:group>NO</aixm:group>
  <aixm:length uom="M">25</aixm:length>
  <aixm:width uom="M">25</aixm:width>
  <aixm:radius uom="M">15</aixm:radius>
  <aixm:part>
    <aixm:VerticalStructurePart>
      <aixm:type>BUILDING</aixm:type>
    </aixm:VerticalStructurePart>
  </aixm:part>
  <aixm:annotation>
    <aixm:Note>
      <aixm:purpose>REMARK</aixm:purpose>
    </aixm:Note>
  </aixm:annotation>
</aixm:VerticalStructure>`
};

function loadExample() {
  const sel = document.getElementById('xml-example').value;
  if (sel && XML_EXAMPLES[sel]) {
    document.getElementById('xml-input').value = XML_EXAMPLES[sel];
  }
}

async function validateXML() {
  const xml = document.getElementById('xml-input').value.trim();
  if (!xml) return;

  const resultDiv = document.getElementById('xml-result');
  resultDiv.innerHTML = '<div style="text-align:center;padding:40px"><span class="spinner"></span><br><span style="font-size:0.8rem;color:#4a9eff;margin-top:10px;display:block">XML ayrıştırılıyor...</span></div>';

  let res, data;
  try {
    res = await fetch('/api/validate_xml', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({xml})
    });
    data = await res.json();
  } catch(e) {
    resultDiv.innerHTML = `<div style="color:#ff6d40;padding:20px">❌ Sunucuya bağlanılamadı: ${e.message}<br><small style="color:#6a8ab0">Flask sunucusu çalışıyor mu? python run.py</small></div>`;
    return;
  }

  if (!res.ok) {
    resultDiv.innerHTML = `<div style="color:#ff6d40;padding:20px">❌ ${data.error || 'Bilinmeyen hata'}</div>`;
    return;
  }

  // ── BULK MODE (AIXMBasicMessage) ─────────────────────────────────────────
  if (data.mode === 'bulk') {
    const s = data.stats;
    const allOk = s.rejected === 0;

    // Özet banner
    let html = `
      <div class="final ${allOk?'fa':'fr'}" style="margin-bottom:16px">
        <div class="fi">${allOk?'✅':'❌'}</div>
        <div class="ft">
          <strong>AIXMBasicMessage</strong> — ${s.total} feature member<br>
          <span style="color:#4aff91">✅ ${s.accepted} kabul</span> &nbsp;
          <span style="color:#ff6d40">❌ ${s.rejected} ret</span> &nbsp;
          <span style="color:#6a8ab0">⏭ ${s.skipped} atlandı (kural yok)</span>
        </div>
      </div>
      <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px;font-size:0.72rem">
        <button onclick="bulkFilterAll()" style="background:#1a3a5c;border:1px solid #2a5a8c;color:#c0d8f8;padding:4px 10px;border-radius:6px;cursor:pointer">Tümü</button>
        <button onclick="bulkFilterRej()" style="background:#3a1a1a;border:1px solid #8c2a2a;color:#ff9a7a;padding:4px 10px;border-radius:6px;cursor:pointer">❌ Sadece Hatalar</button>
        <button onclick="bulkFilterSkip()" style="background:#1a2a3a;border:1px solid #3a5a7a;color:#6a9ab0;padding:4px 10px;border-radius:6px;cursor:pointer">⏭ Sadece Atlanmış</button>
      </div>
      <div id="bulk-list">`;

    // Feature grupla: aynı feature adı → kaç tane var
    const grouped = {};
    data.results.forEach(r => {
      if (!grouped[r.feature]) grouped[r.feature] = {ok:0, fail:0, skip:0, errors:[]};
      if (r.skipped) grouped[r.feature].skip++;
      else if (r.result.accepted) grouped[r.feature].ok++;
      else { grouped[r.feature].fail++; grouped[r.feature].errors.push(r); }
    });

    for (const [feat, g] of Object.entries(grouped)) {
      const total = g.ok + g.fail + g.skip;
      const cls = g.fail > 0 ? 'fr' : g.skip === total ? 'skip' : 'fa';
      const icon = g.fail > 0 ? '❌' : g.skip === total ? '⏭' : '✅';
      const clsMap = {fa:'bulk-ok', fr:'bulk-fail', skip:'bulk-skip'};
      html += `<div class="bulk-row ${clsMap[cls]||''}" data-type="${cls}">
        <div class="bulk-feat">${icon} <strong>aixm:${feat}</strong></div>
        <div class="bulk-counts">
          <span style="color:#4aff91">${g.ok} ✓</span>
          ${g.fail > 0 ? `<span style="color:#ff6d40">${g.fail} ✗</span>` : ''}
          ${g.skip > 0 ? `<span style="color:#6a8ab0">${g.skip} atl.</span>` : ''}
          <span style="color:#4a6a8a">/ ${total}</span>
        </div>`;
      if (g.errors.length > 0) {
        html += `<div class="bulk-errors">`;
        g.errors.slice(0,3).forEach(r => {
          const errTok = r.result.error_token || '?';
          html += `<div style="font-size:0.68rem;color:#ff9a7a;margin-top:4px">⚠ <code>${errTok}</code> etiketi beklenmiyor</div>`;
        });
        if (g.errors.length > 3) html += `<div style="font-size:0.65rem;color:#6a8ab0">+${g.errors.length-3} daha...</div>`;
        html += `</div>`;
      }
      html += `</div>`;
    }
    html += `</div>`;
    resultDiv.innerHTML = html;

    // İstatistik güncelle
    tRun++;
    if (allOk) tAccept++; else tReject++;
    document.getElementById('tr').textContent = tRun;
    document.getElementById('ta').textContent = tAccept;
    document.getElementById('tj').textContent = tReject;
    return;
  }

  // ── SINGLE MODE ──────────────────────────────────────────────────────────
  const result = data.result;
  const accepted = result.accepted;

  let toksHtml = data.tokens.map((t,i) => {
    let cls = 'tok';
    if (t === result.error_token) cls += ' err';
    else if (accepted || data.tokens.indexOf(t) < data.tokens.indexOf(result.error_token || '~~~')) cls += ' ok';
    return `<span class="${cls}">${t}</span>`;
  }).join('');

  let stepsHtml = result.steps.map((s,i) => {
    const rc = s.to==='q_accept'?'ra':s.to==='q_reject'?'rr':'';
    const tc = s.to==='q_accept'?'a':s.to==='q_reject'?'r':'';
    const opCls = s.stack_op.startsWith('push')?'op-push':s.stack_op==='pop'?'op-pop':'op-none';
    const stk = s.stack.map(x=>`<span class="stack-el">${x}</span>`).join('');
    return `<tr class="${rc}">
      <td style="color:#4a6a8a">${i+1}</td>
      <td><span class="schip">${s.from}</span></td>
      <td style="color:#c0d8f8;font-size:0.72rem">${s.token}</td>
      <td><span class="schip ${tc}">${s.to}</span></td>
      <td class="${opCls}">${s.stack_op}</td>
      <td>${stk}</td>
    </tr>`;
  }).join('');

  resultDiv.innerHTML = `
    <div class="final ${accepted?'fa':'fr'}" style="margin-bottom:16px">
      <div class="fi">${accepted?'✅':'❌'}</div>
      <div class="ft">Feature: <strong style="color:#4a9eff">${data.feature}</strong><br>
      ${accepted ? 'XML sözdizimi geçerli, PDA kabul etti.' : `Hata: <span style="color:#ff6d40;font-family:monospace">${result.error_token || 'Beklenmeyen sıra'}</span> etiketi beklenmiyor.`}</div>
    </div>
    <div class="tflow" style="background:#0d1b2a;border:1px solid #1e3a5f;border-radius:8px;margin-bottom:12px">
      <div class="tlbl">Çıkarılan Token Dizisi</div>
      <div class="tokens">${toksHtml}</div>
    </div>
    <div class="log-section" style="background:#0d1b2a;border:1px solid #1e3a5f;border-radius:8px">
      <div class="log-lbl">PDA Durum Geçişleri</div>
      <table class="log-table">
        <thead><tr><th>#</th><th>Durum</th><th>Token</th><th>Sonraki</th><th>Yığın Op.</th><th>Yığın</th></tr></thead>
        <tbody>${stepsHtml}</tbody>
      </table>
    </div>
  `;

  tRun++;
  if (accepted) tAccept++; else tReject++;
  document.getElementById('tr').textContent = tRun;
  document.getElementById('ta').textContent = tAccept;
  document.getElementById('tj').textContent = tReject;
}

function bulkFilterAll()  { document.querySelectorAll('.bulk-row').forEach(r=>r.style.display=''); }
function bulkFilterRej()  { document.querySelectorAll('.bulk-row').forEach(r=>r.style.display = r.dataset.type==='fr'?'':'none'); }
function bulkFilterSkip() { document.querySelectorAll('.bulk-row').forEach(r=>r.style.display = r.dataset.type==='skip'?'':'none'); }

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

// ── GENERATOR ──────────────────────────────────────────────────────────────

let genScenarios = [];
let activeGenScenario = null;
let lastGeneratedXML = '';

async function loadGeneratorScenarios() {
  if (genScenarios.length) return;
  const res = await fetch('/api/generator/scenarios');
  genScenarios = await res.json();
  renderGenList();
}

function renderGenList() {
  const list = document.getElementById('gen-scenario-list');
  if (!list) return;
  list.innerHTML = '';
  genScenarios.forEach(s => {
    const btn = document.createElement('div');
    btn.className = 'sitem gen-item';
    btn.dataset.id = s.id;
    btn.style.cssText = 'display:flex;align-items:flex-start;gap:10px;padding:10px 14px 10px 18px';
    btn.innerHTML = `<span style="font-size:1.2rem;line-height:1">${s.icon}</span>
      <div>
        <div style="font-size:0.8rem;color:#c0d8f8;font-weight:600">${s.baslik}</div>
        <div style="font-size:0.68rem;color:#5a7a9a;margin-top:2px">${s.aciklama}</div>
      </div>`;
    btn.onclick = () => selectGenScenario(s);
    list.appendChild(btn);
  });
}

function selectGenScenario(s) {
  activeGenScenario = s;
  document.querySelectorAll('.gen-item').forEach(el => el.classList.remove('active'));
  document.querySelector(`.gen-item[data-id="${s.id}"]`).classList.add('active');
  document.getElementById('gen-btn').disabled = false;

  const container = document.getElementById('gen-params');
  container.innerHTML = `<div style="font-size:0.9rem;color:#e8f4ff;font-weight:600;margin-bottom:16px">${s.icon} ${s.baslik}</div>`;

  s.params.forEach(param => {
    const wrap = document.createElement('div');
    wrap.style.cssText = 'margin-bottom:14px';
    let input;
    if (param.type === 'select') {
      input = `<select id="gp-${param.key}" style="width:100%;background:#0d1b2a;border:1px solid #2a4a7a;color:#c8d8f0;padding:7px 10px;border-radius:6px;font-size:0.82rem">
        ${param.options.map(o => `<option value="${o}" ${o===param.default?'selected':''}>${o}</option>`).join('')}
      </select>`;
    } else {
      input = `<input id="gp-${param.key}" type="${param.type==='number'?'text':'text'}" value="${param.default}"
        style="width:100%;box-sizing:border-box;background:#0d1b2a;border:1px solid #2a4a7a;color:#c8d8f0;padding:7px 10px;border-radius:6px;font-size:0.82rem;outline:none">`;
    }
    wrap.innerHTML = `<label style="font-size:0.72rem;color:#6a9ab0;display:block;margin-bottom:5px">${param.label}</label>${input}`;
    container.appendChild(wrap);
  });
}

async function generateXML() {
  if (!activeGenScenario) return;

  const params = {};
  activeGenScenario.params.forEach(p => {
    const el = document.getElementById(`gp-${p.key}`);
    if (el) params[p.key] = el.value;
  });

  const resultDiv = document.getElementById('gen-result');
  resultDiv.innerHTML = '<div style="text-align:center;padding:40px"><span class="spinner"></span></div>';

  let res, data;
  try {
    res = await fetch('/api/generator/generate', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({scenario_id: activeGenScenario.id, params})
    });
    data = await res.json();
  } catch(e) {
    resultDiv.innerHTML = `<div style="color:#ff6d40;padding:20px">❌ Sunucuya bağlanılamadı: ${e.message}</div>`;
    return;
  }

  if (!res.ok) {
    resultDiv.innerHTML = `<div style="color:#ff6d40;padding:20px">❌ ${data.error}</div>`;
    return;
  }

  lastGeneratedXML = data.xml;
  document.getElementById('gen-send-btn').style.display = '';

  const accepted = data.result.accepted;
  const tokens   = data.tokens;

  let toksHtml = tokens.map(t => {
    let cls = 'tok';
    if (t === data.result.error_token) cls += ' err';
    else cls += ' ok';
    return `<span class="${cls}">${t}</span>`;
  }).join('');

  resultDiv.innerHTML = `
    <div class="final ${accepted?'fa':'fr'}" style="margin-bottom:14px">
      <div class="fi">${accepted?'✅':'❌'}</div>
      <div class="ft">
        Feature: <strong style="color:#4a9eff">${data.feature}</strong><br>
        ${accepted ? 'PDA kabul etti — XML geçerli.' : `Hata: <code style="color:#ff6d40">${data.result.error_token}</code> beklenmiyor.`}
      </div>
    </div>
    <div style="background:#080d18;border:1px solid #1e3a5f;border-radius:8px;margin-bottom:12px">
      <div style="padding:8px 14px;border-bottom:1px solid #1e3a5f;font-size:0.68rem;color:#4a9eff;text-transform:uppercase;letter-spacing:1px;display:flex;justify-content:space-between;align-items:center">
        Üretilen XML
        <button onclick="copyGenXML()" style="background:#1a3a5c;border:1px solid #2a5a8c;color:#c0d8f8;padding:2px 10px;border-radius:5px;cursor:pointer;font-size:0.7rem">Kopyala</button>
      </div>
      <pre id="gen-xml-out" style="margin:0;padding:14px 16px;color:#7ac8f8;font-size:0.75rem;overflow-x:auto;white-space:pre-wrap">${escapeHtml(data.xml)}</pre>
    </div>
    <div style="background:#0d1b2a;border:1px solid #1e3a5f;border-radius:8px">
      <div style="padding:8px 14px;border-bottom:1px solid #1e3a5f;font-size:0.68rem;color:#4a9eff;text-transform:uppercase;letter-spacing:1px">Token Dizisi</div>
      <div class="tokens" style="padding:10px 14px">${toksHtml}</div>
    </div>
  `;
}

function copyGenXML() {
  navigator.clipboard.writeText(lastGeneratedXML).then(() => {
    const btn = event.target;
    btn.textContent = '✅ Kopyalandı';
    setTimeout(() => btn.textContent = 'Kopyala', 1500);
  });
}

function sendToValidator() {
  if (!lastGeneratedXML) return;
  document.getElementById('xml-input').value = lastGeneratedXML;
  switchTab('xml');
}

function escapeHtml(s) {
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

// Map fonksiyonları map.js dosyasında