// Calories Line Chart
const caloriesCtx = document.getElementById('caloriesChart').getContext('2d');
new Chart(caloriesCtx, {
    type: 'line',
    data: {
        labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        datasets: [{
            label: 'Calories Consumed',
            data: [2000, 2200, 2100, 2300, 2500, 2400, 2000],
            borderColor: 'rgba(75, 192, 192, 1)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderWidth: 2,
            tension: 0.4
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                display: true,
                position: 'top'
            }
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Days of the Week'
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Calories'
                },
                beginAtZero: true
            }
        }
    }
});

// Macronutrient Proportions Pie Chart
const macronutrientCtx = document.getElementById('macronutrientChart').getContext('2d');
new Chart(macronutrientCtx, {
    type: 'pie',
    data: {
        labels: ['Carbohydrates', 'Proteins', 'Fats', 'Fiber'],
        datasets: [{
            data: [50, 25, 15, 10], // Example proportions
            backgroundColor: [
                'rgba(255, 99, 132, 0.6)', // Carbohydrates
                'rgba(54, 162, 235, 0.6)', // Proteins
                'rgba(255, 206, 86, 0.6)', // Fats
                'rgba(75, 192, 192, 0.6)'  // Fiber
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                display: true,
                position: 'top'
            }
        }
    }
});

// Food Category Proportions Doughnut Chart
const foodCategoryCtx = document.getElementById('foodCategoryChart').getContext('2d');
new Chart(foodCategoryCtx, {
    type: 'doughnut',
    data: {
        labels: ['Vegetables', 'Fruits', 'Grains', 'Dairy', 'Meat and Alternatives', 'Snacks and Sweets'],
        datasets: [{
            data: [30, 20, 20, 10, 15, 5], // Example proportions
            backgroundColor: [
                'rgba(75, 192, 192, 0.6)', // Vegetables
                'rgba(255, 159, 64, 0.6)', // Fruits
                'rgba(255, 205, 86, 0.6)', // Grains
                'rgba(201, 203, 207, 0.6)', // Dairy
                'rgba(153, 102, 255, 0.6)', // Meat and Alternatives
                'rgba(255, 99, 132, 0.6)'  // Snacks and Sweets
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                display: true,
                position: 'top'
            }
        }
    }
});

// Weekly Protein Intake Bar Chart
const proteinCtx = document.getElementById('proteinChart').getContext('2d');
new Chart(proteinCtx, {
    type: 'bar',
    data: {
        labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        datasets: [{
            label: 'Protein Intake (grams)',
            data: [50, 60, 55, 70, 65, 80, 75],
            backgroundColor: 'rgba(153, 102, 255, 0.6)',
            borderColor: 'rgba(153, 102, 255, 1)',
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                display: true,
                position: 'top'
            }
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Days of the Week'
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Protein (grams)'
                },
                beginAtZero: true
            }
        }
    }
});

// Daily Water Intake Chart
const waterIntakeCtx = document.getElementById('waterIntakeChart').getContext('2d');
new Chart(waterIntakeCtx, {
    type: 'line',
    data: {
        labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        datasets: [{
            label: 'Water Intake (liters)',
            data: [2.5, 3, 2.8, 3.2, 3, 2.7, 3.1],
            borderColor: 'rgba(54, 162, 235, 1)',
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderWidth: 2,
            tension: 0.4
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                display: true,
                position: 'top'
            }
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Days of the Week'
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Liters'
                },
                beginAtZero: true
            }
        }
    }
});