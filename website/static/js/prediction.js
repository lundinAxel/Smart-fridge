// Define all your functions first
function fetchDateData(selectedDate) {
        fetch('/fetch_date', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `selected_date=${selectedDate}`,
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error(data.error);
        } else {
            updateChart(data);
        }
    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });
}


function updateChart(data) {
    // Update the chart with percentage data
    nutritionChart.data.datasets[0].data = [
        data.calorie_percentage,
        data.carbs_percentage,
        data.protein_percentage,
        data.fat_percentage
    ];

    // Attach actual values to the dataset for tooltip use
    nutritionChart.data.datasets[0].actualValues = [
        data.total_calories,
        data.total_carbohydrates,
        data.total_protein,
        data.total_fat
    ];

    nutritionChart.update();
}

// Initialize the chart globally
const ctx = document.getElementById('nutritionChart').getContext('2d');
const nutritionChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Calories', 'Carbohydrates', 'Protein', 'Fat'],
        datasets: [
            {
                label: 'Total Nutrition Value (%)',
                data: [0, 0, 0, 0], // Default values
                backgroundColor: [
                    'rgba(255, 99, 132, 0.6)',
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(75, 192, 192, 0.6)',
                    'rgba(153, 102, 255, 0.6)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)'
                ],
                borderWidth: 1
            }
        ]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                max: 150,
                title: {
                    display: true,
                    text: 'Percentage (%)',
                    font: {
                        size: 14, // Increase the font size of the Y-axis title
                        weight: 'bold', // Make the title bold
                        family: 'Arial', // Optional: Set the font family
                    },
                    color: '#000000' // Change the title color to white
                },
                ticks: {
                    font: {
                        size: 14, // Increase Y-axis tick font size
                        weight: 'bold' // Make Y-axis tick labels bold
                    },
                    color: '#000000' // Change Y-axis tick label color to white
                }
            },
            x: {
                title: {
                    display: true,
                    font: {
                        size: 10, // Increase the font size of the X-axis title
                        weight: 'bold', // Make the title bold
                        family: 'Arial', // Optional: Set the font family
                    },
                    color: '#000000' // Change the title color to white
                },
                ticks: {
                    font: {
                        size: 10, // Increase X-axis tick font size
                        weight: 'bold' // Make X-axis tick labels bold
                    },
                    color: '#000000' // Change X-axis tick label color to white
                }
            }
        },
        plugins: {
            tooltip: {
                callbacks: {
                    label: function (tooltipItem) {
                        const percentage = tooltipItem.raw.toFixed(1);
                        const actualValue = tooltipItem.chart.data.datasets[0].actualValues[tooltipItem.dataIndex].toFixed(2);
                        const maxValues = [
                            document.getElementById('nutritionChart').dataset.calorieGoal,
                            document.getElementById('nutritionChart').dataset.carbsGoal,
                            document.getElementById('nutritionChart').dataset.proteinGoal,
                            document.getElementById('nutritionChart').dataset.fatGoal
                        ];
                        const maxValue = maxValues[tooltipItem.dataIndex];

                        return [
                            `Percentage: ${percentage}%`,
                            `Actual/Goal: ${actualValue}/${maxValue}`
                        ];
                    }
                }
            }
        }
    }
});
// Use `DOMContentLoaded` at the bottom of the file
document.addEventListener('DOMContentLoaded', () => {
    const today = new Date().toISOString().split('T')[0];
    const dateInput = document.getElementById('selected_date');

    if (dateInput) {
        // Set the default value to today's date
        dateInput.value = today;

        // Fetch data for today's date on page load
        fetchDateData(today);

        // Add an event listener for date changes
        dateInput.addEventListener('change', () => {
            const selectedDate = dateInput.value;
            console.log("Date changed to:", selectedDate);

            // Fetch data for the new selected date
            fetchDateData(selectedDate);
        });
    } else {
        console.error("Date input element not found.");
    }
});