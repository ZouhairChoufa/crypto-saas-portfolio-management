document.addEventListener('DOMContentLoaded', () => {
    console.log("Crypto SaaS Frontend chargé !");

    const ctx = document.getElementById('cryptoChart').getContext('2d');

    // Données simulées pour la démo (Heures de la journée)
    const labels = ['08:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00'];
    
    // Simulation : Le prix monte
    const priceData = [42000, 42100, 42500, 42300, 42800, 43000, 43500];
    
    // Simulation : Le sentiment suit le prix (0 à 100 pour l'échelle)
    const sentimentData = [50, 55, 60, 58, 70, 75, 80];

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Prix Bitcoin ($)',
                    data: priceData,
                    borderColor: '#3b82f6', // Bleu
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    yAxisID: 'y',
                    tension: 0.4 // Courbe lisse
                },
                {
                    label: 'Score de Sentiment (Hype)',
                    data: sentimentData,
                    borderColor: '#10b981', // Vert
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    yAxisID: 'y1', // Deuxième axe Y pour le sentiment
                    tension: 0.4,
                    borderDash: [5, 5] // Ligne pointillée pour le sentiment
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            scales: {
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    grid: { color: '#374151' } // Grille grise
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    grid: { drawOnChartArea: false } // Pas de grille pour le 2ème axe
                },
                x: {
                    grid: { color: '#374151' }
                }
            },
            plugins: {
                legend: {
                    labels: { color: 'white' } // Texte en blanc
                }
            }
        }
    });
});