const ctx = document.getElementById("report-chart");

new Chart(ctx, {
  type: "bar",
  data: {
    labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
    datasets: [
      {
        label: "Total Sales",
        data: [12, 19, 3, 5, 2, 3],
        borderWidth: 1,
        borderColor: "#A8842D",
        backgroundColor: "#A8842D",
      },
      {
        label: "Total Order",
        data: [12, 19, 3, 5, 2, 3],
        borderWidth: 1,
        borderColor: "#4D22A2",
        backgroundColor: "#4D22A2",
      },
      {
        label: "Total Product Sold",
        data: [12, 19, 3, 5, 2, 3],
        borderWidth: 1,
        borderColor: "#247E7C",
        backgroundColor: "#247E7C",
      },
    ],
  },
  options: {
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  },
});
