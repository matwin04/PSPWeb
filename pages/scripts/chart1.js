const xValues = [50,60,70,80,90,100,110,120,130,140,150];
const yValues = [7,8,8,9,9,9,10,11,14,14,15];
new Chart("myChart", {
  type: "line",
  data: {
    labels: xValues,
    datasets: [{
      data: yValues,
      backgroundColor: "red",
      borderColor: "black",
      fill: false,
    }]
  },
  options: {
    legend: {display: false}
  }
});