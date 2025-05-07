// Populate the dropdown with dummy users
const dummyUsers = [
  { id: 1, name: 'Alice' },
  { id: 2, name: 'Bob' }
];

const dropdown = document.getElementById('sharedReports');
dummyUsers.forEach(user => {
  const option = document.createElement('option');
  option.value = user.id;
  option.textContent = user.name;
  dropdown.appendChild(option);
});

const dummyDataSets = {
  1: { // Data for Alice
    caloriesChartData: {
      labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
      datasets: [{
        label: 'Calories Consumed',
        data: [1800, 1950, 2100, 2000, 2200, 2350, 2400],
        borderColor: 'rgba(75, 192, 192, 1)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        tension: 0.4
      }]
    },
    macronutrientChartData: {
      labels: ['Carbohydrates', 'Proteins', 'Fats', 'Fiber'],
      datasets: [{
        label: 'Macronutrient Distribution',
        data: [60, 20, 15, 5],
        backgroundColor: [
          'rgba(255, 99, 132, 0.6)',
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 206, 86, 0.6)',
          'rgba(75, 192, 192, 0.6)'
        ]
      }]
    },
    foodCategoryChartData: {
      labels: ['Vegetables', 'Fruits', 'Grains', 'Dairy', 'Meat and Alternatives', 'Snacks and Sweets'],
      datasets: [{
        label: 'Food Category Distribution',
        data: [30, 20, 20, 10, 15, 5],
        backgroundColor: [
          'rgba(75, 192, 192, 0.6)',
          'rgba(255, 159, 64, 0.6)',
          'rgba(255, 205, 86, 0.6)',
          'rgba(201, 203, 207, 0.6)',
          'rgba(153, 102, 255, 0.6)',
          'rgba(255, 99, 132, 0.6)'
        ]
      }]
    },
    proteinChartData: {
      labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
      datasets: [{
        label: 'Protein Intake (grams)',
        data: [50, 65, 55, 70, 60, 85, 75],
        backgroundColor: 'rgba(153, 102, 255, 0.6)',
        borderColor: 'rgba(153, 102, 255, 1)',
        borderWidth: 1
      }]
    },
    waterIntakeChartData: {
      labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
      datasets: [{
        label: 'Water Intake (liters)',
        data: [2.5, 3.1, 2.8, 3.3, 3, 2.9, 3.2],
        borderColor: 'rgba(54, 162, 235, 1)',
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderWidth: 2,
        tension: 0.4
      }]
    }
  },
  2: { // Data for Bob
    caloriesChartData: {
      labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
      datasets: [{
        label: 'Calories Consumed',
        data: [2000, 2150, 2200, 2300, 2450, 2500, 2600],
        borderColor: 'rgba(75, 192, 192, 1)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        tension: 0.4
      }]
    },
    macronutrientChartData: {
      labels: ['Carbohydrates', 'Proteins', 'Fats', 'Fiber'],
      datasets: [{
        label: 'Macronutrient Distribution',
        data: [50, 25, 20, 5],
        backgroundColor: [
          'rgba(255, 99, 132, 0.6)',
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 206, 86, 0.6)',
          'rgba(75, 192, 192, 0.6)'
        ]
      }]
    },
    foodCategoryChartData: {
      labels: ['Vegetables', 'Fruits', 'Grains', 'Dairy', 'Meat and Alternatives', 'Snacks and Sweets'],
      datasets: [{
        label: 'Food Category Distribution',
        data: [35, 25, 15, 10, 10, 5],
        backgroundColor: [
          'rgba(75, 192, 192, 0.6)',
          'rgba(255, 159, 64, 0.6)',
          'rgba(255, 205, 86, 0.6)',
          'rgba(201, 203, 207, 0.6)',
          'rgba(153, 102, 255, 0.6)',
          'rgba(255, 99, 132, 0.6)'
        ]
      }]
    },
    proteinChartData: {
      labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
      datasets: [{
        label: 'Protein Intake (grams)',
        data: [55, 70, 60, 75, 65, 90, 80],
        backgroundColor: 'rgba(153, 102, 255, 0.6)',
        borderColor: 'rgba(153, 102, 255, 1)',
        borderWidth: 1
      }]
    },
    waterIntakeChartData: {
      labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
      datasets: [{
        label: 'Water Intake (liters)',
        data: [3, 3.4, 3.2, 3.7, 3.5, 3.3, 3.6],
        borderColor: 'rgba(54, 162, 235, 1)',
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderWidth: 2,
        tension: 0.4
      }]
    }
  }
};

document.getElementById('sharedReports').addEventListener('change', function () {
  const selectedUserId = this.value;
  if (selectedUserId && dummyDataSets[selectedUserId]) {
    console.log(`Loaded shared report for user ID: ${selectedUserId}`);
    updateCharts(dummyDataSets[selectedUserId]);
  }
});

function updateCharts(data) {
  // Update the calories chart
  const caloriesChart = Chart.getChart('caloriesChart');
  if (caloriesChart) {
    caloriesChart.data = data.caloriesChartData;
    caloriesChart.update();
  }

  // Update the macronutrient proportions chart
  const macronutrientChart = Chart.getChart('macronutrientChart');
  if (macronutrientChart) {
    macronutrientChart.data = data.macronutrientChartData;
    macronutrientChart.update();
  }

  // Update the food category proportions chart
  const foodCategoryChart = Chart.getChart('foodCategoryChart');
  if (foodCategoryChart) {
    foodCategoryChart.data = data.foodCategoryChartData;
    foodCategoryChart.update();
  }

  // Update the weekly protein intake chart
  const proteinChart = Chart.getChart('proteinChart');
  if (proteinChart) {
    proteinChart.data = data.proteinChartData;
    proteinChart.update();
  }

  // Update the daily water intake chart
  const waterIntakeChart = Chart.getChart('waterIntakeChart');
  if (waterIntakeChart) {
    waterIntakeChart.data = data.waterIntakeChartData;
    waterIntakeChart.update();
  }
}

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
            data: [50, 25, 15, 10],
            backgroundColor: [
                'rgba(255, 99, 132, 0.6)',
                'rgba(54, 162, 235, 0.6)',
                'rgba(255, 206, 86, 0.6)',
                'rgba(75, 192, 192, 0.6)'
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
            data: [30, 20, 20, 10, 15, 5],
            backgroundColor: [
                'rgba(75, 192, 192, 0.6)',
                'rgba(255, 159, 64, 0.6)',
                'rgba(255, 205, 86, 0.6)',
                'rgba(201, 203, 207, 0.6)',
                'rgba(153, 102, 255, 0.6)',
                'rgba(255, 99, 132, 0.6)'
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