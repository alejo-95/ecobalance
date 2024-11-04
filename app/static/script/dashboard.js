fetch('/historico/data')
    .then(response => response.json())
    .then(data => {
        
        console.log(data);
        let all = document.getElementById('allTemp').getContext('2d');
        let allTemp = new Chart(all, {
            type: 'line',
            data: {
                labels: data.all.labels,
                datasets: [{
                    label: 'Puntos acumulados',
                    data: data.all.values,
                    backgroundColor: 'rgba(6, 143, 143, 0.932)',
                    borderColor: 'rgba(6, 143, 143, 0.932)',
                    borderWidth: 1,
                    fill: false
                }]
            },
            options: {
                plugins: {
                    tooltip: {
                        enabled: true
                    },
                    datalabels: {
                        anchor: 'end',
                        align: 'top',
                        formatter: (value, context) => {
                            return value;
                        }
                    }
                },
                scales: {
                    y: {
                        grid: {
                            display: false, 
                        },
                        beginAtZero: true
                    },
                    x: {
                        grid: {
                            display: false, 
                        },
                        type: 'time',
                        time: {
                            unit: 'day',
                            //stepSize: 1,
                            tooltipFormat: 'yyyy-MM-dd'
                        },
                        title: {
                            display: true,
                            text: 'Fecha y Hora'
                        }
                        //beginAtZero: true
                    }
                }
            },
            plugins: [ChartDataLabels]
        });

        
        let max = document.getElementById('maxPoint').getContext('2d');
        let maxTemp = new Chart(max, {
            type: 'bar',
            data: {
                labels: data.max.labels,
                datasets: [{
                    label: 'Nuestro punto máximo',
                    data: data.max.values,
                    backgroundColor: 'rgba(1, 112, 97, 0.937)',
                    borderColor: 'rgba(1, 112, 97, 0.937)',
                    borderWidth: 1
                }]
            },
            options: {
                plugins: {
                    tooltip: {
                        enabled: true
                    },
                    legend: {
                        display: false
                    },
                    datalabels: {
                        anchor: 'end',
                        align: 'top',
                        formatter: (value, context) => {
                            return value.toFixed(2); // Formato de los valores
                        }
                    }
                },
                scales: {
                    y: {
                        grid: {
                        display: false, // Desactivar la cuadrícula en el eje x
                    },
                        beginAtZero: true
                    },
                    x: {
                        grid: {
                            display: false, // Desactivar la cuadrícula en el eje x
                        },
                        beginAtZero: true
                    },
                }
            },
            plugins: [ChartDataLabels]
        });

        // Gráfico de temperatura mínima
        let min = document.getElementById('minPoint').getContext('2d');
        let minTemp = new Chart(min, {
            type: 'bar',
            data: {
                labels: data.min.labels,
                datasets: [{
                    label: 'Puntos en crecimiento',
                    data: data.min.values,
                    backgroundColor: 'rgba(1, 112, 97, 0.575)',
                    borderColor: 'rgba(1, 112, 97, 0.575)',
                    borderWidth: 1
                }]
            },
            options: {
                plugins: {
                    tooltip: {
                        enabled: true
                    },
                    legend: {
                        display: false
                    },
                    datalabels: {
                        anchor: 'end',
                        align: 'top',
                        formatter: (value, context) => {
                            return value.toFixed(2); // Formato de los valores
                        }
                    }
                },
                scales: {
                    y: {
                        grid: {
                        display: false, // Desactivar la cuadrícula en el eje x
                    },
                        beginAtZero: true
                    },
                    x: {
                        grid: {
                            display: false, // Desactivar la cuadrícula en el eje x
                        },
                        beginAtZero: true
                    },
                }
            },
            plugins: [ChartDataLabels]
        });
    })
    .catch(error => console.error('Error:', error));
