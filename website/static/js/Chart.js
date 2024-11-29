document.addEventListener('DOMContentLoaded', () => {
    // Fetch weekly data from the backend
    fetch('/fetch_weekly_calories')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                renderChart(data.data); // Pass the data to renderChart function
            } else {
                console.error("Error fetching weekly calories:", data.error);
                alert("Failed to load weekly data.");
            }
        })
        .catch(error => {
            console.error("Error fetching weekly calories:", error);
            alert("Failed to fetch weekly data.");
        });
});

function renderChart(weeklyData) {
    const labels = weeklyData.map(item => item.date); // Dates for the x-axis
    const calories = weeklyData.map(item => item.total_calories); // Calories for the y-axis

    const ctx = document.getElementById('weeklyCalorieChart').getContext('2d');
    new Chart(ctx, {
        type: 'line', // Line chart type
        data: {
            labels: labels, // Dynamically provided labels
            datasets: [{
                label: 'Calories Consumed (Last 7 Days)',
                data: calories, // Dynamically provided data
                backgroundColor: 'rgba(255, 255, 255, 1)',
                borderColor: 'rgba(255, 255, 255, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    title: {
                        display: true,
                        font: {
                            size: 9, // Set font size for X-axis title
                            weight: 'bold', // Make title bold
                            family: 'Arial', // Optional: Set font family
                        },
                        color: '#000000' // Set title color to black
                    },
                    ticks: {
                        font: {
                            size: 9, // Set font size for X-axis labels
                            weight: 'bold', // Make labels bold
                        },
                        color: '#000000' // Set label color to black
                    }
                },
                y: {
                    min: 0, // Start Y-axis at 0
                    max: 4000, // End Y-axis at 4000
                    title: {
                        display: true,
                        text: 'Calories',
                        font: {
                            size: 14, // Set font size for Y-axis title
                            weight: 'bold', // Make title bold
                            family: 'Arial', // Optional: Set font family
                        },
                        color: '#000000' // Set title color to black
                    },
                    ticks: {
                        font: {
                            size: 14, // Set font size for Y-axis labels
                            weight: 'bold', // Make labels bold
                        },
                        color: '#000000' // Set label color to black
                    }
                }
            },
            plugins: {
                annotation: {
                    annotations: {
                        lineAtZero: {
                            type: 'line',
                            yMin: 0,
                            yMax: 0,
                            borderColor: 'rgba(255, 0, 0, 0.8)', // Red color for the line
                            borderWidth: 2,
                            borderDash: [5, 5], // Dotted line
                            label: {
                                enabled: true,
                                content: '0 Calories',
                                position: 'end',
                                backgroundColor: 'rgba(255, 0, 0, 0.8)',
                                color: '#fff',
                                font: {
                                    size: 10, // Font size for annotation label
                                    style: 'bold', // Bold font style for annotation label
                                    family: 'Arial', // Optional: Set font family for annotation
                                }
                            }
                        }
                    }
                }
            }
        }
    });
}



