$(document).ready(function () {
    const sharedReportsDropdown = $("#sharedReports");
  
    // Flags to track whether each chart has been loaded
    const chartLoaded = {
      calories: false,
      vegMeat: false,
      grams: false,
      protein: false,
    };
  
    // Fetch shared reports and populate the dropdown
    $.getJSON("/sharings", function (sharings) {
      sharings.forEach(function (sharing) {
        sharedReportsDropdown.append(
          `<option value="${sharing.id}">Shared by ${sharing.sender_username}</option>`
        );
      });
    }).fail(function () {
      console.error("Error fetching shared reports.");
    });
  
    // Handle dropdown selection
    sharedReportsDropdown.on("change", function () {
      const selectedValue = $(this).val();
  
      if (selectedValue === "myself") {
        loadDataForUser();
      } else {
        loadDataForSharing(selectedValue);
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
        updateCaloriesChart(data);
        chartLoaded.calories = true; // Mark as loaded
      }).fail(function () {
        console.error("Error loading daily calories.");
      });
    }
  
    // Load veg-meat proportion chart
    function loadVegMeatChart(url) {
      if (chartLoaded.vegMeat) return; // Skip if already loaded
  
      $.getJSON(url, function (data) {
        updateVegMeatChart(data);
        chartLoaded.vegMeat = true; // Mark as loaded
      }).fail(function () {
        console.error("Error loading veg-meat proportion.");
      });
    }
  
    // Load grams chart
    function loadGramsChart(url) {
      if (chartLoaded.grams) return; // Skip if already loaded
  
      $.getJSON(url, function (data) {
        updateGramsChart(data);
        chartLoaded.grams = true; // Mark as loaded
      }).fail(function () {
        console.error("Error loading daily grams.");
      });
    }
  
    // Load protein chart
    function loadProteinChart(url) {
      if (chartLoaded.protein) return; // Skip if already loaded
  
      $.getJSON(url, function (data) {
        updateProteinChart(data);
        chartLoaded.protein = true; // Mark as loaded
      }).fail(function () {
        console.error("Error loading daily protein.");
      });
    }
  
    // Initialize charts when their tabs are shown
    $('a[data-bs-toggle="tab"]').on("shown.bs.tab", function (e) {
      const target = $(e.target).attr("href"); // Get the target tab ID
  
      if (target === "#calories") {
        loadCaloriesChart("/analytics/daily_calories");
      } else if (target === "#veg-meat") {
        loadVegMeatChart("/analytics/veg_meat_proportion");
      } else if (target === "#grams") {
        loadGramsChart("/analytics/daily_grams");
      } else if (target === "#protein") {
        loadProteinChart("/analytics/daily_protein");
      }
    });
  
    // Example function to update the calories chart
    function updateCaloriesChart(data) {
      const ctx = $("#caloriesChart")[0].getContext("2d");
      new Chart(ctx, {
        type: "line",
        data: {
          labels: data.map((entry) => entry.date), // Use the date instead of the day of the week
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
                text: "Date", // Update the x-axis title to "Date"
              },
            },
            y: {
              title: {
                display: true,
                text: "Calories", // Keep the y-axis title as "Calories"
              },
              beginAtZero: true,
            },
          },
        },
      });
    }
  
    // Example function to update the veg-meat proportion chart
    function updateVegMeatChart(data) {
      const ctx = $("#vegMeatChart")[0].getContext("2d");
      new Chart(ctx, {
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
    }
  
    // Example function to update the grams chart
    function updateGramsChart(data) {
      const ctx = $("#gramsChart")[0].getContext("2d");
      new Chart(ctx, {
        type: "bar",
        data: {
          labels: data.map((entry) => entry.date), // Use the date instead of the day of the week
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
                text: "Date", // Update the x-axis title to "Date"
              },
            },
            y: {
              title: {
                display: true,
                text: "Grams", // Keep the y-axis title as "Grams"
              },
              beginAtZero: true,
            },
          },
        },
      });
    }
  
    // Example function to update the protein chart
    function updateProteinChart(data) {
      const ctx = $("#proteinChart")[0].getContext("2d");
      new Chart(ctx, {
        type: "line",
        data: {
          labels: data.map((entry) => entry.date), // Use the date instead of the day of the week
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
                text: "Date", // Update the x-axis title to "Date"
              },
            },
            y: {
              title: {
                display: true,
                text: "Protein (g)", // Keep the y-axis title as "Protein (g)"
              },
              beginAtZero: true,
            },
          },
        },
      });
    }
  
    // Load the first chart (calories) by default
    loadDataForUser();
  });