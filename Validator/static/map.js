// ── Sıfırdan Canvas Harita — dış kütüphane yok ────────────────────────────

const MapEngine = (() => {
  let canvas, ctx, W, H;
  let features = [];
  let view = { minLon:-33, maxLon:-31, minLat:52.25, maxLat:52.45 };
  let drag = { active:false, sx:0, sy:0, vx0:null };
  let scale = 1;
  let activeGroup = 'all';
  let hiddenTypes = new Set();

  const GROUPS = {
    all:      () => true,
    runway:   f => f.type.startsWith('Runway') || f.type === 'TouchDownLiftOff',
    nav:      f => ['Navaid','VOR','NDB','DME','TACAN','Localizer','Glidepath','MarkerBeacon','DesignatedPoint','HoldingPattern'].includes(f.type),
    taxiway:  f => f.type.startsWith('Taxi') || f.type.startsWith('Guidance'),
    obstacle: f => ['VerticalStructure','ObstacleArea'].includes(f.type),
    light:    f => f.type.includes('Light') || f.type.includes('Lighting') || f.type === 'VisualGlideSlopeIndicator',
    apron:    f => f.type.startsWith('Apron') || f.type === 'AircraftStand' || f.type === 'AirportHeliport',
    airspace: f => f.type === 'Airspace' || f.type === 'GeoBorder' || f.type === 'ObstacleArea' || f.type === 'RouteSegment',
  };

  function lonToX(lon) { return (lon - view.minLon) / (view.maxLon - view.minLon) * W; }
  function latToY(lat) { return (1 - (lat - view.minLat) / (view.maxLat - view.minLat)) * H; }
  function xToLon(x)   { return view.minLon + x / W * (view.maxLon - view.minLon); }
  function yToLat(y)   { return view.minLat + (1 - y / H) * (view.maxLat - view.minLat); }

  function resize() {
    const panel = document.getElementById('panel-map');
    const panelRect = panel.getBoundingClientRect();
    const toolbar = panel.querySelector('div');
    const toolbarH = toolbar ? toolbar.offsetHeight : 44;
    const top  = panelRect.top + toolbarH;
    const left = panelRect.left;
    W = Math.round(panelRect.width);
    H = Math.round(panelRect.height - toolbarH);
    canvas.width  = W;
    canvas.height = Math.max(H, 100);
    canvas.style.width  = W + 'px';
    canvas.style.height = Math.max(H, 100) + 'px';
    canvas.style.top  = top + 'px';
    canvas.style.left = left + 'px';
  }

  function drawGrid() {
    ctx.strokeStyle = 'rgba(30,58,95,0.5)';
    ctx.lineWidth = 0.5;
    const steps = 5;
    for (let i = 0; i <= steps; i++) {
      const x = W * i / steps;
      ctx.beginPath(); ctx.moveTo(x,0); ctx.lineTo(x,H); ctx.stroke();
      const y = H * i / steps;
      ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(W,y); ctx.stroke();
    }
    // Koordinat etiketleri
    ctx.fillStyle = 'rgba(74,158,255,0.4)';
    ctx.font = '10px monospace';
    for (let i = 0; i <= steps; i++) {
      const lon = xToLon(W * i / steps);
      const lat = yToLat(H * i / steps);
      ctx.fillText(lon.toFixed(3), W * i / steps + 2, H - 4);
      ctx.fillText(lat.toFixed(3), 2, H * i / steps + 12);
    }
  }

  function draw() {
    ctx.fillStyle = '#07101e';
    ctx.fillRect(0, 0, W, H);
    drawGrid();


    const filter = GROUPS[activeGroup] || GROUPS.all;
    const visible = features.filter(f => filter(f) && !hiddenTypes.has(f.type));

    // Önce çizgileri, sonra noktaları çiz
    visible.forEach(f => {
      if (f.geometry.type === 'Point' || f.geometry.type === 'MultiPoint') return;
      drawFeature(f);
    });
    visible.forEach(f => {
      if (f.geometry.type === 'Point' || f.geometry.type === 'MultiPoint') drawFeature(f);
    });

    // Bilgi
    const cnt = visible.length;
    document.getElementById('map-feat-count').textContent = `${cnt} feature gösteriliyor`;
  }

  function drawFeature(f) {
    const g = f.geometry;
    ctx.strokeStyle = f.color;
    ctx.fillStyle   = f.color;

    if (g.type === 'Point') {
      const [lon, lat] = g.coordinates;
      const x = lonToX(lon), y = latToY(lat);
      if (x < -5 || x > W+5 || y < -5 || y > H+5) return;
      ctx.beginPath();
      ctx.arc(x, y, 4, 0, Math.PI*2);
      ctx.globalAlpha = 0.9;
      ctx.fill();
      ctx.globalAlpha = 1;
      ctx.lineWidth = 1;
      ctx.stroke();

    } else if (g.type === 'MultiPoint') {
      g.coordinates.forEach(([lon, lat]) => {
        const x = lonToX(lon), y = latToY(lat);
        if (x < -5 || x > W+5 || y < -5 || y > H+5) return;
        ctx.beginPath();
        ctx.arc(x, y, 2, 0, Math.PI*2);
        ctx.globalAlpha = 0.7;
        ctx.fill();
        ctx.globalAlpha = 1;
      });

    } else if (g.type === 'LineString') {
      drawLine(g.coordinates, f.color, 1.5);

    } else if (g.type === 'MultiLineString') {
      g.coordinates.forEach(coords => drawLine(coords, f.color, 1));
    }
  }

  function drawLine(coords, color, width) {
    if (coords.length < 2) return;
    ctx.beginPath();
    ctx.strokeStyle = color;
    ctx.lineWidth = width;
    ctx.globalAlpha = 0.75;
    let first = true;
    coords.forEach(([lon, lat]) => {
      const x = lonToX(lon), y = latToY(lat);
      if (first) { ctx.moveTo(x, y); first = false; }
      else ctx.lineTo(x, y);
    });
    ctx.stroke();
    ctx.globalAlpha = 1;
  }

  function fitBounds() {
    const filter = GROUPS[activeGroup] || GROUPS.all;
    const visible = features.filter(filter);
    if (!visible.length) return;

    // Tüm koordinatları topla
    let allLons = [], allLats = [];
    visible.forEach(f => {
      const g = f.geometry;
      const coords = g.type==='Point' ? [g.coordinates] :
                     g.type==='MultiPoint' ? g.coordinates :
                     g.type==='LineString' ? g.coordinates :
                     g.type==='MultiLineString' ? g.coordinates.reduce((a,c)=>a.concat(c),[]) : [];
      coords.forEach(([lon,lat]) => {
        if (isFinite(lon)&&isFinite(lat)) { allLons.push(lon); allLats.push(lat); }
      });
    });
    if (!allLons.length) return;

    // Outlier filtresi: median ± 3*IQR dışındakileri at
    function robustBounds(arr) {
      const s = [...arr].sort((a,b)=>a-b);
      const q1 = s[Math.floor(s.length*0.25)];
      const q3 = s[Math.floor(s.length*0.75)];
      const iqr = q3 - q1;
      const lo = q1 - 3*iqr, hi = q3 + 3*iqr;
      const filtered = s.filter(v => v>=lo && v<=hi);
      return [filtered[0], filtered[filtered.length-1]];
    }
    const [minLon, maxLon] = robustBounds(allLons);
    const [minLat, maxLat] = robustBounds(allLats);
    if (!isFinite(minLon)) return;

    const padLon = (maxLon-minLon)*0.08 || 0.05;
    const padLat = (maxLat-minLat)*0.08 || 0.05;
    view = { minLon:minLon-padLon, maxLon:maxLon+padLon,
             minLat:minLat-padLat, maxLat:maxLat+padLat };
    // Aspect ratio düzelt
    const mapAspect = W / H;
    const dataAspect = (view.maxLon-view.minLon) / (view.maxLat-view.minLat) * 0.6;
    if (dataAspect < mapAspect) {
      const d = ((view.maxLon-view.minLon) * mapAspect/dataAspect - (view.maxLon-view.minLon)) / 2;
      view.minLon -= d; view.maxLon += d;
    }
  }

  // Hover tooltip
  function onMouseMove(e) {
    const rect = canvas.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;

    if (drag.active) {
      const dLon = (drag.sx - mx) / W * (view.maxLon-view.minLon);
      const dLat = (my - drag.sy) / H * (view.maxLat-view.minLat);
      view = {
        minLon: drag.vx0.minLon + dLon, maxLon: drag.vx0.maxLon + dLon,
        minLat: drag.vx0.minLat + dLat, maxLat: drag.vx0.maxLat + dLat,
      };
      draw();
      return;
    }

    const mLon = xToLon(mx), mLat = yToLat(my);
    const filter = GROUPS[activeGroup] || GROUPS.all;
    let hit = null, minDist = 8;

    features.filter(filter).forEach(f => {
      const g = f.geometry;
      if (g.type === 'Point') {
        const [lon,lat] = g.coordinates;
        const dx = lonToX(lon)-mx, dy = latToY(lat)-my;
        const d = Math.sqrt(dx*dx+dy*dy);
        if (d < minDist) { minDist=d; hit=f; }
      }
    });

    const tip = document.getElementById('map-tooltip');
    if (hit) {
      tip.style.display = 'block';
      tip.style.left = (mx+12)+'px';
      tip.style.top  = (my-10)+'px';
      tip.innerHTML = `<span style="color:${hit.color}">${hit.icon} ${hit.label}</span><br><b>${hit.name}</b>`;
    } else {
      tip.style.display = 'none';
    }
  }

  function onWheel(e) {
    e.preventDefault();
    const rect = canvas.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;
    const factor = e.deltaY > 0 ? 1.15 : 0.87;
    const lon = xToLon(mx), lat = yToLat(my);
    view = {
      minLon: lon + (view.minLon-lon)*factor,
      maxLon: lon + (view.maxLon-lon)*factor,
      minLat: lat + (view.minLat-lat)*factor,
      maxLat: lat + (view.maxLat-lat)*factor,
    };
    draw();
  }

  function init(featureData) {
    canvas = document.getElementById('map-canvas');
    ctx = canvas.getContext('2d');
    features = featureData;
    // Canvas'ı panel içinde görünür yap
    canvas.style.position = 'fixed';
    canvas.style.zIndex = '500';
    resize();
    fitBounds();
    draw();
    buildLegend();

    canvas.addEventListener('mousemove', onMouseMove);
    canvas.addEventListener('wheel', onWheel, {passive:false});
    canvas.addEventListener('mousedown', e => {
      drag.active=true; drag.sx=e.offsetX; drag.sy=e.offsetY;
      drag.vx0 = {...view};
      canvas.style.cursor='grabbing';
    });
    canvas.addEventListener('mouseup',   () => { drag.active=false; canvas.style.cursor='crosshair'; });
    canvas.addEventListener('mouseleave',() => { drag.active=false; });
    window.addEventListener('resize', () => { resize(); fitBounds(); draw(); });
  }

  function buildLegend() {
    const container = document.getElementById('legend-items');
    if (!container) return;
    const seen = new Map();
    features.forEach(f => {
      if (!seen.has(f.type)) seen.set(f.type, {color:f.color, icon:f.icon, label:f.label, count:0});
      seen.get(f.type).count++;
    });
    container.innerHTML = '';
    [...seen.entries()].sort((a,b)=>b[1].count-a[1].count).forEach(([type, info]) => {
      const div = document.createElement('div');
      div.className = 'leg-item';
      div.dataset.type = type;
      div.innerHTML = `<span class="leg-dot" style="background:${info.color}"></span><span>${info.icon} ${info.label} <span style="color:#3a5a7a">(${info.count})</span></span>`;
      div.onclick = () => {
        div.classList.toggle('hidden');
        hiddenTypes[div.classList.contains('hidden') ? 'add' : 'delete'](type);
        draw();
      };
      container.appendChild(div);
    });
  }

  return {
    init,
    setGroup(g) { activeGroup=g; fitBounds(); draw(); buildLegend(); },
    redraw() { resize(); draw(); },
    fitAll() { fitBounds(); draw(); },
  };
})();

// ── Map Tab entegrasyonu ───────────────────────────────────────────────────
let _canvasMapLoaded = false;

async function loadMapFeatures() {
  document.getElementById('map-feat-count').textContent = 'Veriler yükleniyor...';
  let data;
  try {
    const res = await fetch('/api/map/features');
    if (!res.ok) { document.getElementById('map-feat-count').textContent = '❌ Donlon.xml bulunamadı'; return; }
    data = await res.json();
  } catch(e) {
    document.getElementById('map-feat-count').textContent = '❌ Bağlantı hatası'; return;
  }
  MapEngine.init(data);
}

function mapFilterGroup(el, group) {
  document.querySelectorAll('.map-chip').forEach(c => c.classList.remove('active'));
  el.classList.add('active');
  MapEngine.setGroup(group);
}
