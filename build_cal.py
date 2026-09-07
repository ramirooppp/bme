import os

file_path = "c:/Users/nahue/Desktop/segundo cuatrimestre/calendario.html"

with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. CSS
css_to_add = r'''
        /* --- NEW FEATURES CSS --- */
        .tracker-btn { background: var(--bg-tertiary); border: 1px solid var(--border-light); color: white; border-radius: 4px; padding: 4px 8px; font-size: 0.75rem; cursor: pointer; z-index: 10; margin-top: 5px; display: flex; align-items: center; justify-content: center; width: fit-content; transition: 0.2s; }
        .tracker-btn:hover { background: var(--accent); }
        .tracker-btn.stop { background: #ef4444; border-color: #dc2626; }
        .tracker-btn.stop:hover { background: #b91c1c; }

        .xp-bar-container { display: flex; align-items: center; gap: 10px; margin-left: 2rem; background: var(--bg-tertiary); padding: 5px 15px; border-radius: 20px; border: 1px solid var(--border-light); }
        .xp-bar { width: 120px; height: 8px; background: var(--bg-main); border-radius: 4px; overflow: hidden; border: 1px solid var(--border-dark); }
        .xp-fill { height: 100%; background: var(--accent); transition: width 0.5s ease; }
        .streak-badge { font-weight: 700; color: #f59e0b; font-size: 1rem; display: flex; align-items: center; gap: 5px; background: var(--bg-tertiary); padding: 5px 15px; border-radius: 20px; border: 1px solid var(--border-light); }
        .level-text { font-weight: 700; color: var(--accent); font-size: 0.9rem; }
        
        .modal-overlay { position: fixed; top:0; left:0; right:0; bottom:0; background: rgba(0,0,0,0.7); z-index: 2000; display: none; justify-content: center; align-items: center; backdrop-filter: blur(4px); }
        .modal { background: var(--bg-secondary); padding: 2rem; border-radius: 12px; border: 1px solid var(--border-light); width: 400px; max-width: 90%; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        .modal h3 { margin-bottom: 1rem; color: var(--text-main); }
        .modal input, .modal textarea { width: 100%; padding: 0.75rem; margin-bottom: 1rem; background: var(--bg-tertiary); border: 1px solid var(--border-dark); color: white; border-radius: 6px; font-family: inherit; }
        .modal input:focus, .modal textarea:focus { outline: none; border-color: var(--accent); }
        .star-rating { display: flex; gap: 8px; margin-bottom: 1.5rem; font-size: 1.8rem; cursor: pointer; }
        .star-rating span { color: var(--border-light); transition: 0.2s; }
        .star-rating span.active { color: #f59e0b; }
        .star-rating span:hover { transform: scale(1.1); }

        .toast-container { position: fixed; top: 20px; right: 20px; z-index: 3000; display: flex; flex-direction: column; gap: 10px; }
        .toast { background: var(--bg-tertiary); border-left: 4px solid var(--accent); padding: 1rem 1.5rem; border-radius: 6px; box-shadow: 0 5px 15px rgba(0,0,0,0.3); animation: slideIn 0.3s ease, fadeOut 0.3s ease 3.7s forwards; display: flex; align-items: center; gap: 10px; color: var(--text-main); font-weight: 500; }
        @keyframes slideIn { from { transform: translateX(120%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
        @keyframes fadeOut { from { opacity: 1; } to { opacity: 0; } }

        .dashboard-grid { display: grid; grid-template-columns: 1fr 1.5fr; gap: 1.5rem; width: 100%; }
        .dashboard-card { background-color: var(--bg-main); border: 1px solid var(--border-dark); border-radius: 12px; padding: 1.5rem; display: flex; flex-direction: column; gap: 1rem; }

        .heat-container { display: flex; flex-direction: column; gap: 10px; }
        .heat-days { display: flex; gap: 5px; justify-content: space-between; }
        .heat-box { flex: 1; aspect-ratio: 1; border-radius: 4px; background: var(--bg-tertiary); border: 1px solid var(--border-dark); display: flex; align-items: center; justify-content: center; font-size: 0.7rem; color: rgba(255,255,255,0.3); transition: 0.3s; position: relative; }
        .heat-box.lvl-1 { background: #064e3b; border-color: #065f46; color: rgba(255,255,255,0.7); }
        .heat-box.lvl-2 { background: #059669; border-color: #10b981; color: #fff; }
        .heat-box.lvl-3 { background: #10b981; border-color: #34d399; color: #fff; box-shadow: 0 0 10px rgba(16, 185, 129, 0.4); }
        .heat-box.lvl-4 { background: #34d399; border-color: #6ee7b7; color: #000; font-weight: bold; box-shadow: 0 0 15px rgba(52, 211, 153, 0.6); }

        .mini-cal { display: grid; grid-template-columns: repeat(7, 1fr); gap: 4px; text-align: center; font-size: 0.8rem; }
        .mini-cal-header { display: grid; grid-template-columns: repeat(7, 1fr); gap: 4px; text-align: center; font-size: 0.7rem; color: var(--text-muted); margin-bottom: 5px; font-weight: bold; }
        .mini-day { padding: 6px 0; border-radius: 4px; cursor: pointer; transition: 0.2s; background: var(--bg-tertiary); border: 1px solid transparent; }
        .mini-day:hover { background: var(--border-dark); }
        .mini-day.empty { background: transparent; cursor: default; }
        .mini-day.today { border-color: var(--accent); color: var(--accent); font-weight: bold; }
        .mini-day.has-exam { border-bottom: 3px solid #ef4444; }
        .mini-day.has-study { position: relative; overflow: hidden; }
        .mini-day.has-study::before { content:''; position:absolute; top:0;left:0;right:0;bottom:0; background: rgba(16, 185, 129, 0.15); pointer-events: none; }

        .donut-container { position: relative; width: 140px; height: 140px; border-radius: 50%; background: conic-gradient(var(--bg-tertiary) 100%); display: flex; justify-content: center; align-items: center; margin: 0 auto; box-shadow: inset 0 0 20px rgba(0,0,0,0.5); }
        .donut-inner { width: 90px; height: 90px; background: var(--bg-main); border-radius: 50%; display: flex; flex-direction: column; justify-content: center; align-items: center; font-weight: bold; color: var(--text-main); font-size: 1.1rem; box-shadow: 0 0 15px rgba(0,0,0,0.5); }
        .donut-inner span { font-size: 0.7rem; color: var(--text-muted); font-weight: normal; }
        .donut-legend { margin-top: 1.5rem; font-size: 0.8rem; display: flex; flex-direction: column; gap: 8px; }
        .legend-item { display: flex; align-items: center; justify-content: space-between; }
        .legend-left { display: flex; align-items: center; gap: 8px; }

        .badges-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(80px, 1fr)); gap: 15px; }
        .badge { display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; font-size: 0.75rem; padding: 10px; border-radius: 8px; background: var(--bg-tertiary); border: 1px solid var(--border-dark); opacity: 0.5; filter: grayscale(100%); transition: 0.3s; position: relative; cursor: help; }
        .badge.unlocked { opacity: 1; filter: grayscale(0%); border-color: var(--border-light); background: linear-gradient(145deg, var(--bg-tertiary), rgba(255,255,255,0.05)); box-shadow: 0 4px 10px rgba(0,0,0,0.2); }
        .badge.unlocked:hover { transform: translateY(-3px); box-shadow: 0 6px 15px rgba(0,0,0,0.3); }
        .badge-icon { font-size: 2rem; margin-bottom: 5px; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.5)); }
        .badge-title { font-weight: 600; color: var(--text-main); line-height: 1.2; margin-bottom: 3px; }
        .badge-date { font-size: 0.6rem; color: var(--accent); }
        .badge-tooltip { position: absolute; bottom: 100%; left: 50%; transform: translateX(-50%); background: #000; color: #fff; padding: 5px 10px; border-radius: 4px; font-size: 0.75rem; white-space: nowrap; pointer-events: none; opacity: 0; transition: 0.2s; margin-bottom: 5px; z-index: 10; width: 120px; }
        .badge:hover .badge-tooltip { opacity: 1; }

        .xp-flash { animation: flashXP 0.5s ease; }
        @keyframes flashXP { 0% { box-shadow: 0 0 0 rgba(59, 130, 246, 0); } 50% { box-shadow: 0 0 20px rgba(59, 130, 246, 0.8); } 100% { box-shadow: 0 0 0 rgba(59, 130, 246, 0); } }

        .session-indicator { position: absolute; bottom: 4px; right: 4px; font-size: 0.7rem; color: #10b981; font-weight: bold; }
'''
text = text.replace('</style>', css_to_add + '\n    </style>')

# 2. HEADER
header_old = r'''        <div class="header-title">
            <h1>UTN Ing. Química - 2do Cuatrimestre</h1>
            <p>Calendario de Estudio y Clases</p>
        </div>'''
header_new = r'''        <div class="header-title" style="display:flex; align-items:center;">
            <div>
                <h1>UTN Ing. Química - 2do Cuatrimestre</h1>
                <p>Calendario de Estudio y Clases</p>
            </div>
            <div class="streak-badge" id="streakBadge" title="Días seguidos de estudio">🔥 0</div>
            <div class="xp-bar-container" id="xpContainer" title="Nivel y XP">
                <span class="level-text" id="levelBadge">Nvl 1</span>
                <div class="xp-bar">
                    <div class="xp-fill" id="xpFill" style="width: 0%;"></div>
                </div>
                <span id="xpText" style="font-size:0.75rem; color:var(--text-muted); font-variant-numeric:tabular-nums;">0 XP</span>
            </div>
        </div>'''
text = text.replace(header_old, header_new)

# 3. MODALS
toasts_and_modals = r'''
    <!-- Toasts & Modals -->
    <div class="toast-container" id="toastContainer"></div>
    <div class="modal-overlay" id="logModalOverlay">
        <div class="modal">
            <h3>📝 Registro de Sesión</h3>
            <p style="margin-bottom:1rem; font-size:0.9rem; color:var(--text-secondary);">Tiempo real: <span id="logTimeTxt" style="color:var(--text-main); font-weight:bold;">0</span> min</p>
            <input type="text" id="logTema" placeholder="¿Qué tema o ejercicios viste? (Ej: Unidad 3, Guía 2)">
            <div style="margin-bottom: 0.5rem; font-size:0.9rem; color:var(--text-secondary);">Nivel de dificultad percibida:</div>
            <div class="star-rating" id="logStars">
                <span data-val="1">★</span><span data-val="2">★</span><span data-val="3">★</span><span data-val="4">★</span><span data-val="5">★</span>
            </div>
            <textarea id="logDudas" rows="2" placeholder="¿Dudas pendientes o algo para repasar?"></textarea>
            <div style="display:flex; gap:1rem; justify-content:flex-end;">
                <button class="btn" id="btnLogCancel">Descartar</button>
                <button class="btn" style="background:var(--accent); color:white; border-color:var(--accent);" id="btnLogSave">Guardar y Sumar XP</button>
            </div>
        </div>
    </div>
'''
text = text.replace('<!-- Main Content -->', toasts_and_modals + '\n    <!-- Main Content -->')

# 4. BOTTOM SECTION
bottom_old = r'''    <!-- Bottom Section: Progress & Stats -->
    <div class="bottom-section">
        <div class="progress-container">
            <div class="section-header">
                <span>Progreso por Materia</span>
                <span style="font-size: 0.8rem; font-weight: normal; color: var(--text-muted);">Clic en la materia para expandir. Clic en unidad para cambiar estado.</span>
            </div>
            <div id="subjectsProgress"></div>
        </div>

        <div class="stats-container">
            <div class="section-header">Estadísticas Semanales</div>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value" id="statClassHrs">0</div>
                    <div class="stat-label">Horas de Clase</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="statStudyHrs">0</div>
                    <div class="stat-label">Horas de Estudio</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="statPomodoros">0</div>
                    <div class="stat-label">Pomodoros Hoy</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="statTotalHrs">0</div>
                    <div class="stat-label">Horas Totales</div>
                </div>
            </div>
        </div>
    </div>'''

bottom_new = r'''    <!-- Bottom Section: Dashboard -->
    <div class="bottom-section" style="flex-direction: column;">
        <div class="dashboard-grid">
            
            <div class="dashboard-card">
                <div class="section-header">
                    <span>Progreso por Materia</span>
                    <span style="font-size: 0.75rem; font-weight: normal; color: var(--text-muted);">Clic unidad para estado</span>
                </div>
                <div id="subjectsProgress"></div>
            </div>

            <div class="dashboard-card" style="gap: 2rem;">
                <div>
                    <div class="section-header">Estadísticas Semanales</div>
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-value" id="statRealHrs" style="color:var(--accent);">0.0</div>
                            <div class="stat-label">Horas Reales</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value" id="statPlanHrs">0.0</div>
                            <div class="stat-label">Horas Planeadas</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value" id="statClassHrs">0.0</div>
                            <div class="stat-label">Horas Clase</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value" id="statPomodoros">0</div>
                            <div class="stat-label">Pomodoros Hoy</div>
                        </div>
                    </div>
                </div>

                <div style="display:flex; gap: 2rem; flex-wrap: wrap;">
                    <div style="flex:1; min-width:180px;">
                        <div class="section-header" style="font-size:0.9rem;">Distribución de Estudio (Real)</div>
                        <div class="donut-container" id="donutChart">
                            <div class="donut-inner"><span style="margin-top:-5px;">Total</span><div id="donutTotal" style="margin-top:2px;">0h</div></div>
                        </div>
                        <div class="donut-legend" id="donutLegend"></div>
                    </div>
                    
                    <div style="flex:1.5; min-width:220px; display:flex; flex-direction:column; gap:1.5rem;">
                        <div>
                            <div class="section-header" style="font-size:0.9rem; margin-bottom:0.5rem;">Mapa de Calor (Semana)</div>
                            <div class="heat-container">
                                <div class="heat-days" id="weeklyHeatmap"></div>
                            </div>
                        </div>
                        <div>
                            <div class="section-header" style="font-size:0.9rem; margin-bottom:0.5rem; display:flex; justify-content:space-between;">
                                <span>Mini Calendario</span>
                                <span id="miniCalMonth" style="color:var(--accent);"></span>
                            </div>
                            <div class="mini-cal-header">
                                <div>D</div><div>L</div><div>M</div><div>M</div><div>J</div><div>V</div><div>S</div>
                            </div>
                            <div class="mini-cal" id="miniCalendar"></div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="dashboard-card" style="grid-column: 1 / -1;">
                <div class="section-header">Logros y Medallas</div>
                <div class="badges-grid" id="badgesGrid"></div>
            </div>
            
        </div>
    </div>'''
text = text.replace(bottom_old, bottom_new)

# 5. JS LOGIC
js_replacements = []

js_replacements.append((
    r"let draggedEvent = null;",
    r'''let draggedEvent = null;

        // --- NEW DATA MODELS ---
        const BADGES_DEFS = [
            { id: 'first_pomo', title: 'Primer Pomodoro', icon: '🍅', desc: 'Completaste tu primer pomodoro.' },
            { id: 'marathon', title: 'Maratonista', icon: '🏃', desc: 'Estudiaste más de 10 horas reales en una semana.' },
            { id: 'streak_7', title: 'Racha de 7', icon: '🔥', desc: '7 días seguidos de estudio.' },
            { id: 'streak_30', title: 'Racha de 30', icon: '🌟', desc: '30 días seguidos de estudio. ¡Imparable!' },
            { id: 'fq_master', title: 'Fisicoquímico', icon: '⚗️', desc: 'Completaste todas las unidades de Fisicoquímica.' },
            { id: 'leg_master', title: 'Legislador', icon: '⚖️', desc: 'Completaste todas las unidades de Legislación.' },
            { id: 'all_subjects', title: 'Cinco materias', icon: '📚', desc: 'Estudiaste las 5 materias principales en una misma semana.' },
            { id: 'night_owl', title: 'Noche de estudio', icon: '🦉', desc: 'Registraste una sesión de estudio después de las 22:00.' },
            { id: 'early_bird', title: 'Madrugador', icon: '🌅', desc: 'Registraste una sesión de estudio antes de las 09:00.' },
            { id: 'pomo_100', title: '100 Pomodoros', icon: '💯', desc: 'Completaste 100 pomodoros en total.' },
            { id: 'first_week', title: 'Primera semana', icon: '📅', desc: 'Estudiaste 5 días en la primera semana (simulado).' },
            { id: 'balance', title: 'Balance perfecto', icon: '⚖️', desc: 'Estudiaste todas las materias de manera balanceada.' }
        ];

        let activeTracker = null; // { id, startTime, element }
        let currentRating = 0;
        let sessionToLog = null;
    '''
))

js_replacements.append((
    r"function saveProgress(data) {",
    r'''function saveProgress(data) {
            localStorage.setItem('cal-progress', JSON.stringify(data));
        }

        // Feature: Streaks & XP Storage
        function getStreakData() {
            return JSON.parse(localStorage.getItem('streak-data')) || { currentStreak: 0, longestStreak: 0, lastStudyDate: null };
        }
        function saveStreakData(d) { localStorage.setItem('streak-data', JSON.stringify(d)); }
        
        function getXpData() {
            return JSON.parse(localStorage.getItem('xp-data')) || { totalXP: 0 };
        }
        function saveXpData(d) { localStorage.setItem('xp-data', JSON.stringify(d)); }
        
        function getBadgesData() {
            return JSON.parse(localStorage.getItem('badges-data')) || {};
        }
        function saveBadgesData(d) { localStorage.setItem('badges-data', JSON.stringify(d)); }
        
        function getTrackerData(dateStr) {
            return JSON.parse(localStorage.getItem(`tracker-${dateStr}`)) || {};
        }
        function saveTrackerData(dateStr, d) { localStorage.setItem(`tracker-${dateStr}`, JSON.stringify(d)); }
        function getAllTrackerData() {
            let all = [];
            for (let i = 0; i < localStorage.length; i++) {
                let key = localStorage.key(i);
                if (key.startsWith('tracker-')) {
                    let dateStr = key.replace('tracker-', '');
                    let data = JSON.parse(localStorage.getItem(key));
                    all.push({ date: dateStr, data: data });
                }
            }
            return all;
        }

        function showToast(msg, icon="🔔") {
            const container = document.getElementById('toastContainer');
            const toast = document.createElement('div');
            toast.className = 'toast';
            toast.innerHTML = `<span style="font-size:1.5rem;">${icon}</span> <span>${msg}</span>`;
            container.appendChild(toast);
            setTimeout(() => toast.remove(), 4000);
        }

        function addXP(amount, reason) {
            let xp = getXpData();
            let oldLevel = Math.floor(Math.sqrt(xp.totalXP / 100)) + 1;
            xp.totalXP += amount;
            saveXpData(xp);
            let newLevel = Math.floor(Math.sqrt(xp.totalXP / 100)) + 1;
            
            showToast(`+${amount} XP (${reason})`, "✨");
            
            if (newLevel > oldLevel) {
                setTimeout(() => showToast(`¡Subiste al Nivel ${newLevel}!`, "🎉"), 1000);
            }
            updateXPUI();
        }

        function unlockBadge(badgeId) {
            let bData = getBadgesData();
            if (!bData[badgeId]) {
                bData[badgeId] = { unlockedAt: new Date().toISOString() };
                saveBadgesData(bData);
                let bDef = BADGES_DEFS.find(b => b.id === badgeId);
                if (bDef) {
                    showToast(`¡Logro Desbloqueado: ${bDef.title}!`, bDef.icon);
                    addXP(200, "Logro desbloqueado");
                    renderBadges();
                }
            }
        }

        function updateXPUI() {
            let xp = getXpData();
            let level = Math.floor(Math.sqrt(xp.totalXP / 100)) + 1;
            
            let currentLevelBaseXP = 100 * Math.pow(level - 1, 2);
            let nextLevelXP = 100 * Math.pow(level, 2);
            let xpInCurrentLevel = xp.totalXP - currentLevelBaseXP;
            let xpNeededForNext = nextLevelXP - currentLevelBaseXP;
            let pct = Math.min(100, Math.max(0, (xpInCurrentLevel / xpNeededForNext) * 100));
            
            let badgeEl = document.getElementById('levelBadge');
            let textEl = document.getElementById('xpText');
            let fillEl = document.getElementById('xpFill');
            
            if(badgeEl) badgeEl.textContent = `Nvl ${level}`;
            if(textEl) textEl.textContent = `${Math.floor(xp.totalXP)} XP`;
            if(fillEl) fillEl.style.width = `${pct}%`;
            
            let cont = document.getElementById('xpContainer');
            if(cont) {
                cont.classList.add('xp-flash');
                setTimeout(() => cont.classList.remove('xp-flash'), 500);
            }
        }

        function checkStreak() {
            let data = getStreakData();
            let todayStr = formatDate(new Date());
            
            let allT = getAllTrackerData();
            let studiedDates = allT.filter(d => Object.keys(d.data).length > 0).map(d => d.date).sort();
            
            if (studiedDates.length === 0) {
                data.currentStreak = 0;
            } else {
                let current = 0;
                let testDate = new Date();
                testDate.setHours(0,0,0,0);
                
                let studiedToday = studiedDates.includes(formatDate(testDate));
                if (studiedToday) current++;
                else {
                    let yesterday = new Date(testDate);
                    yesterday.setDate(yesterday.getDate() - 1);
                    if (!studiedDates.includes(formatDate(yesterday))) {
                        current = 0;
                    }
                }
                
                let checkDate = new Date(testDate);
                checkDate.setDate(checkDate.getDate() - (studiedToday ? 1 : 1));
                while(true) {
                    if (studiedDates.includes(formatDate(checkDate))) {
                        current++;
                        checkDate.setDate(checkDate.getDate() - 1);
                    } else {
                        break;
                    }
                }
                
                data.currentStreak = current;
                if (current > data.longestStreak) data.longestStreak = current;
            }
            
            saveStreakData(data);
            let sbEl = document.getElementById('streakBadge');
            if(sbEl) sbEl.innerHTML = `🔥 ${data.currentStreak}`;
            
            if (data.currentStreak >= 7) unlockBadge('streak_7');
            if (data.currentStreak >= 30) unlockBadge('streak_30');
        }
    '''
))

js_replacements.append((
    r"let sub = SUBJECTS[ev.subject];",
    r'''let sub = SUBJECTS[ev.subject];
            
            let tData = getTrackerData(dateStr);
            let hasSession = tData[ev.id] && tData[ev.id].sessions && tData[ev.id].sessions.length > 0;
    '''
))

js_replacements.append((
    r'''<div class="event-badge"></div>
                <div class="event-title">${sub.name}</div>
                <div class="event-time">${ev.start} - ${ev.end}</div>
                <div class="event-location">${ev.type === 'class' ? '📍 '+ev.location : '📚 '+ev.label}</div>''',
    r'''<div class="event-badge"></div>
                ${hasSession ? '<div class="session-indicator" title="Sesión registrada">✓</div>' : ''}
                <div class="event-title">${sub.name}</div>
                <div class="event-time">${ev.start} - ${ev.end}</div>
                <div class="event-location">${ev.type === 'class' ? '📍 '+ev.location : '📚 '+ev.label}</div>
                ${ev.type === 'study' ? `<div class="tracker-btn" data-evid="${ev.id}" data-date="${dateStr}">▶ Empezar</div>` : ''}'''
))

js_replacements.append((
    r"col.appendChild(el);",
    r'''col.appendChild(el);

            if (ev.type === 'study') {
                let tBtn = el.querySelector('.tracker-btn');
                if (tBtn) {
                    if (activeTracker && activeTracker.id === ev.id && activeTracker.dateStr === dateStr) {
                        tBtn.innerHTML = '⏹ Terminar';
                        tBtn.classList.add('stop');
                    }
                    
                    tBtn.addEventListener('click', (e) => {
                        e.stopPropagation();
                        if (tBtn.classList.contains('stop')) {
                            let endTime = new Date();
                            let elapsedMins = Math.round((endTime - activeTracker.startTime) / 60000);
                            
                            if (elapsedMins < 0) elapsedMins = 0;

                            tBtn.innerHTML = '▶ Empezar';
                            tBtn.classList.remove('stop');
                            
                            sessionToLog = {
                                id: ev.id,
                                dateStr: dateStr,
                                subject: ev.subject,
                                start: activeTracker.startTime.toISOString(),
                                end: endTime.toISOString(),
                                minutes: elapsedMins
                            };
                            
                            activeTracker = null;
                            openLogModal(elapsedMins);

                        } else {
                            if (activeTracker) {
                                showToast("Ya tienes una sesión activa en otro bloque.", "⚠️");
                                return;
                            }
                            activeTracker = {
                                id: ev.id,
                                dateStr: dateStr,
                                startTime: new Date()
                            };
                            tBtn.innerHTML = '⏹ Terminar';
                            tBtn.classList.add('stop');
                            showToast("Sesión iniciada. ¡A estudiar!", "▶️");
                        }
                    });
                }
            }'''
))

js_replacements.append((
    r"// --- 5. SIDEBAR LOGIC ---",
    r'''// --- 4.5 QUICK LOG MODAL ---
        const logModalOverlay = document.getElementById('logModalOverlay');
        const starSpans = document.querySelectorAll('#logStars span');

        function openLogModal(mins) {
            document.getElementById('logTimeTxt').textContent = mins;
            document.getElementById('logTema').value = '';
            document.getElementById('logDudas').value = '';
            currentRating = 0;
            updateStars(0);
            logModalOverlay.style.display = 'flex';
        }

        function updateStars(val) {
            starSpans.forEach(s => {
                if (parseInt(s.dataset.val) <= val) s.classList.add('active');
                else s.classList.remove('active');
            });
        }

        starSpans.forEach(s => {
            s.addEventListener('click', () => {
                currentRating = parseInt(s.dataset.val);
                updateStars(currentRating);
            });
        });

        document.getElementById('btnLogCancel').addEventListener('click', () => {
            saveSessionToStorage(null, 0, "");
            logModalOverlay.style.display = 'none';
        });

        document.getElementById('btnLogSave').addEventListener('click', () => {
            let tema = document.getElementById('logTema').value.trim();
            let dudas = document.getElementById('logDudas').value.trim();
            saveSessionToStorage(tema, currentRating, dudas);
            logModalOverlay.style.display = 'none';
        });

        function saveSessionToStorage(tema, rating, dudas) {
            if (!sessionToLog) return;
            
            let tData = getTrackerData(sessionToLog.dateStr);
            if (!tData[sessionToLog.id]) tData[sessionToLog.id] = { sessions: [] };
            
            let s = {
                start: sessionToLog.start,
                end: sessionToLog.end,
                minutes: sessionToLog.minutes,
                tema: tema,
                rating: rating,
                dudas: dudas
            };
            tData[sessionToLog.id].sessions.push(s);
            saveTrackerData(sessionToLog.dateStr, tData);
            
            if (sessionToLog.minutes > 0) {
                addXP(sessionToLog.minutes, "Tiempo de estudio");
            }
            
            let dObj = new Date(sessionToLog.start);
            let h = dObj.getHours();
            if (h >= 22 || h < 4) unlockBadge('night_owl');
            if (h >= 4 && h <= 8) unlockBadge('early_bird');
            
            checkStreak();
            updateStats();
            renderDashboard();
            renderCalendar();
            
            sessionToLog = null;
        }

        // --- 5. SIDEBAR LOGIC ---'''
))

js_replacements.append((
    r"saveProgress(progressData);",
    r'''saveProgress(progressData);
                        
                        if (pData[idx] === 2) {
                            addXP(100, "Unidad completada");
                        }
                        
                        if (sub.id === 'fisicoquimica' && pData.every(v => v === 2)) unlockBadge('fq_master');
                        if (sub.id === 'legislacion' && pData.every(v => v === 2)) unlockBadge('leg_master');
                        '''
))

js_replacements.append((
    r"pomodorosToday++;",
    r'''pomodorosToday++;
                            addXP(50, "Pomodoro completado");
                            
                            let totalPomos = parseInt(localStorage.getItem('total-pomos') || '0') + 1;
                            localStorage.setItem('total-pomos', totalPomos);
                            if (totalPomos === 1) unlockBadge('first_pomo');
                            if (totalPomos >= 100) unlockBadge('pomo_100');
    '''
))

update_stats_old = r'''        function updateStats() {
            let classHrs = 0;
            let studyHrs = 0;
            
            let sb = loadStudyBlocks(currentWeekStart);
            sb.forEach(b => {
                studyHrs += (timeToDecimal(b.end) - timeToDecimal(b.start));
            });
            FIXED_CLASSES.forEach(c => {
                classHrs += (timeToDecimal(c.end) - timeToDecimal(c.start));
            });

            document.getElementById('statClassHrs').textContent = classHrs.toFixed(1);
            document.getElementById('statStudyHrs').textContent = studyHrs.toFixed(1);
            document.getElementById('statTotalHrs').textContent = (classHrs + studyHrs).toFixed(1);
            
            // Pomodoros today
            let pToday = parseInt(localStorage.getItem(`pomos-${formatDate(new Date())}`) || '0');
            document.getElementById('statPomodoros').textContent = pToday;
        }'''

update_stats_new = r'''
        function renderBadges() {
            const grid = document.getElementById('badgesGrid');
            if(!grid) return;
            grid.innerHTML = '';
            let bData = getBadgesData();
            
            BADGES_DEFS.forEach(b => {
                let isUnlocked = bData[b.id] !== undefined;
                let dateStr = isUnlocked ? new Date(bData[b.id].unlockedAt).toLocaleDateString() : 'Bloqueado';
                
                let el = document.createElement('div');
                el.className = `badge ${isUnlocked ? 'unlocked' : ''}`;
                el.innerHTML = `
                    <div class="badge-icon">${b.icon}</div>
                    <div class="badge-title">${b.title}</div>
                    ${isUnlocked ? `<div class="badge-date">${dateStr}</div>` : ''}
                    <div class="badge-tooltip">${b.desc}</div>
                `;
                grid.appendChild(el);
            });
        }

        function renderDashboard() {
            // 1. Weekly Heatmap
            let hMap = document.getElementById('weeklyHeatmap');
            if (hMap) {
                hMap.innerHTML = '';
                const days = ['L', 'M', 'M', 'J', 'V', 'S', 'D'];
                for (let i=0; i<7; i++) {
                    let d = new Date(currentWeekStart);
                    d.setDate(d.getDate() + i);
                    let dStr = formatDate(d);
                    
                    let tData = getTrackerData(dStr);
                    let mins = 0;
                    Object.values(tData).forEach(ev => {
                        if(ev.sessions) ev.sessions.forEach(s => mins += s.minutes);
                    });
                    
                    let hrs = mins / 60;
                    let lvl = 0;
                    if (hrs > 0) lvl = 1;
                    if (hrs >= 2) lvl = 2;
                    if (hrs >= 4) lvl = 3;
                    if (hrs >= 6) lvl = 4;
                    
                    let box = document.createElement('div');
                    box.className = `heat-box lvl-${lvl}`;
                    box.textContent = days[i];
                    box.title = `${hrs.toFixed(1)} hrs el ${d.getDate()}/${d.getMonth()+1}`;
                    hMap.appendChild(box);
                }
            }
            
            // 2. Mini Calendar
            let mCal = document.getElementById('miniCalendar');
            let mMon = document.getElementById('miniCalMonth');
            if (mCal && mMon) {
                mCal.innerHTML = '';
                let today = new Date();
                mMon.textContent = formatDisplayDate(today).split(' ').slice(1).join(' ');
                
                let firstDay = new Date(today.getFullYear(), today.getMonth(), 1);
                let lastDay = new Date(today.getFullYear(), today.getMonth() + 1, 0);
                
                let startOffset = firstDay.getDay() === 0 ? 6 : firstDay.getDay() - 1;
                
                for(let i=0; i<startOffset; i++) {
                    let d = document.createElement('div'); d.className='mini-day empty'; mCal.appendChild(d);
                }
                
                for(let i=1; i<=lastDay.getDate(); i++) {
                    let d = new Date(today.getFullYear(), today.getMonth(), i);
                    let dStr = formatDate(d);
                    let el = document.createElement('div');
                    el.className = 'mini-day';
                    el.textContent = i;
                    
                    if (dStr === formatDate(today)) el.classList.add('today');
                    if (EXAMS.some(ex => ex.date === dStr)) el.classList.add('has-exam');
                    
                    let tData = getTrackerData(dStr);
                    if (Object.keys(tData).length > 0) el.classList.add('has-study');
                    
                    el.title = dStr;
                    el.addEventListener('click', () => {
                        currentWeekStart = getMonday(d);
                        renderCalendar();
                    });
                    
                    mCal.appendChild(el);
                }
            }
            
            // 3. Donut Chart
            let donut = document.getElementById('donutChart');
            let legend = document.getElementById('donutLegend');
            if (donut && legend) {
                let sb = loadStudyBlocks(currentWeekStart);
                let subjMins = {};
                
                for (let i=0; i<7; i++) {
                    let d = new Date(currentWeekStart);
                    d.setDate(d.getDate() + i);
                    let dStr = formatDate(d);
                    let tData = getTrackerData(dStr);
                    
                    Object.entries(tData).forEach(([evId, evData]) => {
                        let block = sb.find(b => b.id === evId);
                        if (block && evData.sessions) {
                            if (!subjMins[block.subject]) subjMins[block.subject] = 0;
                            evData.sessions.forEach(s => subjMins[block.subject] += s.minutes);
                        }
                    });
                }
                
                let totalMins = Object.values(subjMins).reduce((a,b)=>a+b, 0);
                legend.innerHTML = '';
                
                if (totalMins === 0) {
                    donut.style.background = 'conic-gradient(var(--bg-tertiary) 100%)';
                    document.getElementById('donutTotal').textContent = '0h';
                    legend.innerHTML = '<div style="color:var(--text-muted); text-align:center;">Sin datos</div>';
                } else {
                    document.getElementById('donutTotal').textContent = (totalMins/60).toFixed(1) + 'h';
                    let bgString = [];
                    let accPct = 0;
                    let sorted = Object.entries(subjMins).sort((a,b)=>b[1]-a[1]);
                    
                    let subsStudied = 0;
                    sorted.forEach(([subKey, mins]) => {
                        if (mins > 0) {
                            subsStudied++;
                            let pct = (mins / totalMins) * 100;
                            let color = SUBJECTS[subKey].rawColor;
                            bgString.push(`${color} ${accPct}% ${accPct + pct}%`);
                            accPct += pct;
                            
                            let leg = document.createElement('div');
                            leg.className = 'legend-item';
                            leg.innerHTML = `
                                <div class="legend-left">
                                    <div class="color-dot" style="background-color:${color}; width:12px; height:12px;"></div>
                                    <span>${SUBJECTS[subKey].name}</span>
                                </div>
                                <span style="font-weight:bold;">${pct.toFixed(0)}%</span>
                            `;
                            legend.appendChild(leg);
                        }
                    });
                    donut.style.background = `conic-gradient(${bgString.join(', ')})`;
                    if (subsStudied >= 5) unlockBadge('all_subjects');
                }
            }
        }

        function updateStats() {
            let classHrs = 0;
            let planHrs = 0;
            let realHrs = 0;
            
            let sb = loadStudyBlocks(currentWeekStart);
            sb.forEach(b => {
                planHrs += (timeToDecimal(b.end) - timeToDecimal(b.start));
            });
            FIXED_CLASSES.forEach(c => {
                classHrs += (timeToDecimal(c.end) - timeToDecimal(c.start));
            });

            for (let i=0; i<7; i++) {
                let d = new Date(currentWeekStart);
                d.setDate(d.getDate() + i);
                let tData = getTrackerData(formatDate(d));
                Object.values(tData).forEach(ev => {
                    if(ev.sessions) ev.sessions.forEach(s => realHrs += (s.minutes / 60));
                });
            }

            if (realHrs >= 10) unlockBadge('marathon');

            if(document.getElementById('statClassHrs')) document.getElementById('statClassHrs').textContent = classHrs.toFixed(1);
            if(document.getElementById('statPlanHrs')) document.getElementById('statPlanHrs').textContent = planHrs.toFixed(1);
            if(document.getElementById('statRealHrs')) document.getElementById('statRealHrs').textContent = realHrs.toFixed(1);
            
            let pToday = parseInt(localStorage.getItem(`pomos-${formatDate(new Date())}`) || '0');
            if(document.getElementById('statPomodoros')) document.getElementById('statPomodoros').textContent = pToday;
        }'''
js_replacements.append((update_stats_old, update_stats_new))

init_old = r'''        renderExamsBanner();
        renderProgress();
        updatePomoDisplay();
        updateStats();'''
init_new = r'''        renderExamsBanner();
        renderProgress();
        updatePomoDisplay();
        updateStats();
        updateXPUI();
        checkStreak();
        renderBadges();
        renderDashboard();'''
js_replacements.append((init_old, init_new))


for old, new_txt in js_replacements:
    if old not in text:
        print(f"WARNING: Could not find block to replace:\n{old[:100]}")
    text = text.replace(old, new_txt)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Calendar updated successfully.")
