async function carregar() {
    const req = await fetch("/api/leituras");
    const data = await req.json();

    const dados = data.slice(-40);

    const labels = dados.map(d => d.dataTime);
    const t = dados.map(d => d.temperatura);
    const u = dados.map(d => d.umidade);
    const p = dados.map(d => d.pressao);

    const configBase = {
        type: "line",
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    ticks: { 
                        color: "#ffffff",      // números do eixo X
                        font: { size: 12 }
                    },
                    grid: {
                        color: "rgba(255,255,255,0.08)" // linhas do fundo
                    }
                },
                y: {
                    ticks: { 
                        color: "#ffffff",      // números do eixo Y
                        font: { size: 12 }
                    },
                    grid: {
                        color: "rgba(255,255,255,0.08)"
                    }
                }
            },
            plugins: {
                legend: {
                    labels: {
                        color: "#ffffff",      // texto da legenda
                        font: { size: 14 }
                    }
                }
            }
        }
    };

    // Gráfico de Temperatura
    new Chart(document.getElementById("grafTemp"), {
        ...configBase,
        data: {
            labels,
            datasets: [{
                label: "Temperatura (°C)",
                data: t,
                borderColor: "#38bdf8",            // azul
                backgroundColor: "rgba(46,46,46,0.6)", // fundo cinza escuro
                tension: 0.3
            }]
        }
    });

    // Gráfico de Umidade
    new Chart(document.getElementById("grafUmi"), {
        ...configBase,
        data: {
            labels,
            datasets: [{
                label: "Umidade (%)",
                data: u,
                borderColor: "#34d399",            // verde
                backgroundColor: "rgba(46,46,46,0.6)",
                tension: 0.3
            }]
        }
    });

    // Gráfico de Pressão
    new Chart(document.getElementById("grafPres"), {
        ...configBase,
        data: {
            labels,
            datasets: [{
                label: "Pressão (hPa)",
                data: p,
                borderColor: "#f87171",            // vermelho
                backgroundColor: "rgba(46,46,46,0.6)",
                tension: 0.3
            }]
        }
    });
}

carregar();
