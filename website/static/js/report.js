$(function () {
  const date = new Date();
  generateChart(date.getMonth() + 1);
});

let myChart = new Chart(document.getElementById("report-chart"), {
  type: "bar",
  data: {
    labels: [],
    datasets: [
      {
        label: "Total Sales",
        data: [],
        borderWidth: 1,
        borderColor: "#A8842D",
        backgroundColor: "#A8842D",
      },
      {
        label: "Total Order",
        data: [],
        borderWidth: 1,
        borderColor: "#4D22A2",
        backgroundColor: "#4D22A2",
      },
      {
        label: "Total Product Sold",
        data: [],
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

function selectMonth(e) {
  generateChart(e.value);
}

function generateChart(month) {
  $.ajax({
    url: `http://localhost:5000/json/report?month=${month}`,
    method: "GET",
  }).then((resp) => {
    myChart.data.labels = resp.weeks;
    myChart.data.datasets[0].data = resp.total_sales;
    myChart.data.datasets[1].data = resp.total_order;
    myChart.data.datasets[2].data = resp.total_sold;
    myChart.update();
  });
}
