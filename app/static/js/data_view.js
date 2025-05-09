$(document).ready(function () {
  const sharedReportsDropdown = $("#sharedReports");
  let reportVal = "myself";

  // Flags to track whether each chart has been loaded
  const chartLoaded = {
    calories: false,
    vegMeat: false,
    grams: false,
    protein: false,
  };

  // Variables to store chart instances
  let caloriesChartInstance = null;
  let vegMeatChartInstance = null;
  let gramsChartInstance = null;
  let proteinChartInstance = null;

  // Fetch shared reports and populate the dropdown
  $.getJSON("/sharings", function (sharings) {
    sharings.forEach(function (sharing) {
      sharedReportsDropdown.append(
        `<option value="${sharing.id}">${sharing.sender}</option>`
      );
    });
  }).fail(function () {
    console.error("Error fetching shared reports.");
  });

  // Handle dropdown selection
  sharedReportsDropdown.on("change", function () {
    reportVal = $(this).val();
    const selectedValue = $(this).val();

    // Reset all chartLoaded flags to false
    Object.keys(chartLoaded).forEach((key) => {
      chartLoaded[key] = false;
    });

    // Activate the first tab (e.g., #calories)
    $('a[data-bs-toggle="tab"][href="#calories"]').tab("show");

    if (selectedValue === "myself") {
      loadDataForUser();
    } else {
      loadDataForSharing(selectedValue);
    }
  });

  // Handle tab activation
  $('a[data-bs-toggle="tab"]').on("shown.bs.tab", function (e) {
    const target = $(e.target).attr("href"); // Get the target tab ID

    if (reportVal === "myself") {
      // Load data for the current user
      if (target === "#calories" && !chartLoaded.calories) {
        loadCaloriesChart("/analytics/daily_calories");
      } else if (target === "#veg-meat" && !chartLoaded.vegMeat) {
        loadVegMeatChart("/analytics/veg_meat_proportion");
      } else if (target === "#grams" && !chartLoaded.grams) {
        loadGramsChart("/analytics/daily_grams");
      } else if (target === "#protein" && !chartLoaded.protein) {
        loadProteinChart("/analytics/daily_protein");
      }
    } else {
      // Load data for the selected sharing
      if (target === "#calories" && !chartLoaded.calories) {
        loadCaloriesChart(`/analytics/daily_calories?sharing_id=${reportVal}`);
      } else if (target === "#veg-meat" && !chartLoaded.vegMeat) {
        loadVegMeatChart(`/analytics/veg_meat_proportion?sharing_id=${reportVal}`);
      } else if (target === "#grams" && !chartLoaded.grams) {
        loadGramsChart(`/analytics/daily_grams?sharing_id=${reportVal}`);
      } else if (target === "#protein" && !chartLoaded.protein) {
        loadProteinChart(`/analytics/daily_protein?sharing_id=${reportVal}`);
      }
    }
  });

  // Function to load data for the current user
  function loadDataForUser() {
    loadCaloriesChart("/analytics/daily_calories");
  }

  // Function to load data for a specific sharing
  function loadDataForSharing(sharingId) {
    loadCaloriesChart(`/analytics/daily_calories?sharing_id=${sharingId}`);
  }

  // Load calories chart
  function loadCaloriesChart(url) {
    if (chartLoaded.calories) return; // Skip if already loaded

    $.getJSON(url, function (data) {
      if (caloriesChartInstance) {
        caloriesChartInstance.destroy(); // Destroy existing chart instance
      }
      const ctx = $("#caloriesChart")[0].getContext("2d");
      caloriesChartInstance = new Chart(ctx, {
        type: "line",
        data: {
          labels: data.map((entry) => entry.date),
          datasets: [
            {
              label: "Calories",
              data: data.map((entry) => entry.calories),
              borderColor: "rgba(75, 192, 192, 1)",
              backgroundColor: "rgba(75, 192, 192, 0.2)",
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              display: true,
            },
          },
          scales: {
            x: {
              title: {
                display: true,
                text: "Date",
              },
            },
            y: {
              title: {
                display: true,
                text: "Calories",
              },
              beginAtZero: true,
            },
          },
        },
      });
      chartLoaded.calories = true; // Mark as loaded
    }).fail(function () {
      console.error("Error loading daily calories.");
    });
  }

  // Load veg-meat proportion chart
  function loadVegMeatChart(url) {
    if (chartLoaded.vegMeat) return; // Skip if already loaded

    $.getJSON(url, function (data) {
      if (vegMeatChartInstance) {
        vegMeatChartInstance.destroy(); // Destroy existing chart instance
      }
      const ctx = $("#vegMeatChart")[0].getContext("2d");
      vegMeatChartInstance = new Chart(ctx, {
        type: "pie",
        data: {
          labels: ["Vegetable", "Meat"],
          datasets: [
            {
              data: [data.vegetable, data.meat],
              backgroundColor: ["#4caf50", "#f44336"],
            },
          ],
        },
        options: {
          responsive: true,
        },
      });
      chartLoaded.vegMeat = true; // Mark as loaded
    }).fail(function () {
      console.error("Error loading veg-meat proportion.");
    });
  }

  // Load grams chart
  function loadGramsChart(url) {
    if (chartLoaded.grams) return; // Skip if already loaded

    $.getJSON(url, function (data) {
      if (gramsChartInstance) {
        gramsChartInstance.destroy(); // Destroy existing chart instance
      }
      const ctx = $("#gramsChart")[0].getContext("2d");
      gramsChartInstance = new Chart(ctx, {
        type: "bar",
        data: {
          labels: data.map((entry) => entry.date),
          datasets: [
            {
              label: "Grams",
              data: data.map((entry) => entry.grams),
              backgroundColor: "rgba(54, 162, 235, 0.5)",
              borderColor: "rgba(54, 162, 235, 1)",
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              display: false,
            },
          },
          scales: {
            x: {
              title: {
                display: true,
                text: "Date",
              },
            },
            y: {
              title: {
                display: true,
                text: "Grams",
              },
              beginAtZero: true,
            },
          },
        },
      });
      chartLoaded.grams = true; // Mark as loaded
    }).fail(function () {
      console.error("Error loading daily grams.");
    });
  }

  // Load protein chart
  function loadProteinChart(url) {
    if (chartLoaded.protein) return; // Skip if already loaded

    $.getJSON(url, function (data) {
      if (proteinChartInstance) {
        proteinChartInstance.destroy(); // Destroy existing chart instance
      }
      const ctx = $("#proteinChart")[0].getContext("2d");
      proteinChartInstance = new Chart(ctx, {
        type: "line",
        data: {
          labels: data.map((entry) => entry.date),
          datasets: [
            {
              label: "Protein",
              data: data.map((entry) => entry.protein),
              borderColor: "rgba(255, 159, 64, 1)",
              backgroundColor: "rgba(255, 159, 64, 0.2)",
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              display: true,
            },
          },
          scales: {
            x: {
              title: {
                display: true,
                text: "Date",
              },
            },
            y: {
              title: {
                display: true,
                text: "Protein (g)",
              },
              beginAtZero: true,
            },
          },
        },
      });
      chartLoaded.protein = true; // Mark as loaded
    }).fail(function () {
      console.error("Error loading daily protein.");
    });
  }

  loadDataForUser();
});