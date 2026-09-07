import sys
import re

with open(r"c:\Users\nahue\Desktop\segundo cuatrimestre\calendario.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Insert UI Card
html_to_insert = """                <div class="dashboard-card">
                    <div class="section-header">📚 Temario Semanal (S<span id="topicWeekNum"></span>)</div>
                    <div id="weeklyTopicsContent" style="font-size: 0.85rem; display: flex; flex-direction: column; gap: 0.8rem;">
                        <!-- Injected via JS -->
                    </div>
                </div>"""
content = content.replace('<div class="mini-cal" id="miniCalendar"></div>\n                </div>', '<div class="mini-cal" id="miniCalendar"></div>\n                </div>\n' + html_to_insert)

# 2. Insert WEEKLY_SCHEDULE constant
js_const = """        ];

        const WEEKLY_SCHEDULE = [
            { fq: "Unidad 1: Termodinámica de soluciones", bme: "Unidad 1: Modelado flujos, mezcladores, splitter", fdt: "Presentación, Sist. Unidades, Balance Placa" },
            { fq: "Unidad 1: Resolución problemas / Feriado", bme: "Feriado", fdt: "Balance tubo circular, Factor de fricción" },
            { fq: "Unidad 1: Resolución problemas", bme: "Unidad 1: Simulación sin sólidos", fdt: "Guías 4 y 5, Labs 1-2-3" },
            { fq: "Unidad 2: Equilibrio fases multicomponentes", bme: "Unidad 1: Simulación sin sólidos", fdt: "Evaluación TP 1 / Sólidos sumergidos" },
            { fq: "Unidad 3: Eq. binarios / U2 multicomponentes", bme: "Unidad 1: Simulación con sólidos (1 pto)", fdt: "Lecho de partículas / Ec. Bernoulli" },
            { fq: "Repaso U1, 2, 3 / TP Laboratorio 1", bme: "1er PARCIAL Teórico-Práctico", fdt: "Análisis dimensional / TP 3" },
            { fq: "Unidad 4: Ternarios / 1er Cuest. Teórico", bme: "Feriado", fdt: "¿Por qué ing. química? / Transferencia calor" },
            { fq: "Unidad 5: Equilibrio químico", bme: "Unidad 2: Balances de flujos entalpía y calor", fdt: "Práctica Guía 8" },
            { fq: "Unidad 5: Equilibrio químico", bme: "Unidad 2: Simulación de energía", fdt: "1er PARCIAL / Calor Paredes Cilíndricas" },
            { fq: "Unidad 7: Soluciones iónicas", bme: "Feriado", fdt: "Intercambiadores de calor" },
            { fq: "Unidad 7: Conducción - Electroquímica", bme: "Unidad 2: Simulación de energía (1 pto)", fdt: "Práctica / Radiación" },
            { fq: "Unidad 7: Cinética de electrodos", bme: "2do PARCIAL Teórico-Práctico", fdt: "Laboratorio 6 / Difusión" },
            { fq: "Unidad 6: Cinética química / TP Lab", bme: "Unidad 2: Red de intercambiadores (1 pto)", fdt: "Práctica Guía 12" },
            { fq: "Unidad 6: Cinética / Consulta U4,5,7", bme: "3er PARCIAL Teórico-Práctico", fdt: "Laboratorio 7 / 2do PARCIAL" },
            { fq: "Unidad 8: Fenóm. superficiales / 2do Cuest. Teórico", bme: "Consultas", fdt: "Recuperatorio Labs / Feriado" },
            { fq: "Coloquio / Recuperatorio", bme: "Recuperatorio Integral", fdt: "Recuperatorio / Fin de ciclo" }
        ];

        let currentWeekStart"""
content = content.replace("];\n\n        let currentWeekStart", js_const)

# 3. Insert rendering function call and function
js_call = """                    if (subsStudied >= 5) unlockBadge('all_subjects');
                }
            }
            renderWeeklyTopics();
        }

        function renderWeeklyTopics() {
            let container = document.getElementById('weeklyTopicsContent');
            let weekSpan = document.getElementById('topicWeekNum');
            if(!container) return;
            
            let startOfSemester = new Date('2026-08-10T00:00:00');
            let diffTime = currentWeekStart.getTime() - startOfSemester.getTime();
            let diffDays = Math.round(diffTime / 86400000);
            let weekNum = Math.floor(diffDays / 7) + 1;
            
            if (weekNum >= 1 && weekNum <= 16) {
                weekSpan.textContent = weekNum;
                let data = WEEKLY_SCHEDULE[weekNum - 1];
                container.innerHTML = `
                    <div style="display:flex; flex-direction:column; gap:4px;">
                        <div style="font-weight:600; color:var(--color-fisicoquimica);">⚗️ Fisicoquímica</div>
                        <div style="color:var(--text-main); margin-left:1.5rem;">${data.fq}</div>
                    </div>
                    <div style="display:flex; flex-direction:column; gap:4px;">
                        <div style="font-weight:600; color:var(--color-balances);">⚖️ Balances de Masa y Energía</div>
                        <div style="color:var(--text-main); margin-left:1.5rem;">${data.bme}</div>
                    </div>
                    <div style="display:flex; flex-direction:column; gap:4px;">
                        <div style="font-weight:600; color:var(--color-fenomenos);">🌊 Fenómenos de Transporte</div>
                        <div style="color:var(--text-main); margin-left:1.5rem;">${data.fdt}</div>
                    </div>
                `;
            } else {
                weekSpan.textContent = "-";
                container.innerHTML = `<div style="color:var(--text-muted); text-align:center; padding:1.5rem 0;">No hay clases programadas para esta semana.</div>`;
            }
        }

        function updateStats() {"""
content = content.replace("if (subsStudied >= 5) unlockBadge('all_subjects');\n                }\n            }\n        }\n\n        function updateStats() {", js_call)

with open(r"c:\Users\nahue\Desktop\segundo cuatrimestre\calendario.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated calendario.html")
