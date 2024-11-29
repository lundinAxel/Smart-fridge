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
            labels: labels,
            datasets: [{
                label: 'Calories Consumed (Last 7 Days)',
                data: calories,
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
                        display: false,
                        text: 'Date'
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Calories'
                    }
                }
            }
        }
    });
}
