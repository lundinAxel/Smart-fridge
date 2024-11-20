// Define all your functions first
function fetchDateData(selectedDate, username = "AleksanderJ") {
    if (selectedDate && username) {
        fetch('/fetch_date', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `selected_date=${selectedDate}&username=${username}`,
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
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)'
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
                max: 120,
                title: {
                    display: true,
                    text: 'Percentage (%)'
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'Nutritional Components'
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
        fetchDateData(today, "AleksanderJ");

        // Add an event listener for date changes
        dateInput.addEventListener('change', () => {
            const selectedDate = dateInput.value;
            console.log("Date changed to:", selectedDate);

            // Fetch data for the new selected date
            fetchDateData(selectedDate, "AleksanderJ");
        });
    } else {
        console.error("Date input element not found.");
    }
});