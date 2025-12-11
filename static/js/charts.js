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
                        color: "#ffffff",     
                        font: { size: 12 }
                    },
                    grid: {
                        color: "rgba(255,255,255,0.08)" 
                    }
                },
                y: {
                    ticks: { 
                        color: "#ffffff",     
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
                        color: "#ffffff",     
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
                borderColor: "#38bdf8",           
                backgroundColor: "rgba(46,46,46,0.6)", 
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
                borderColor: "#34d399",            
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
                borderColor: "#f87171",           
                backgroundColor: "rgba(46,46,46,0.6)",
                tension: 0.3
            }]
        }
    });
}

carregar();
