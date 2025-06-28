// Initialize Bootstrap Scrollspy for active sidebar links
// Needs to be initialized after content is loaded
$(document).ready(function() {
    const main  = document.querySelector('main');
    main.classList.remove('my-4');
    
    $('body').scrollspy({
        target: '.sidebar',
        offset: 80 // Adjust offset based on navbar height
    });

    // Smooth scrolling for sidebar links and top navbar links
    $('a.nav-link[href^="#"]').on('click', function(event) {
        if (this.hash !== "") {
            event.preventDefault();
            var hash = this.hash;
            $('html, body').animate({
                scrollTop: $(hash).offset().top - 70 // Adjust for fixed navbar height
            }, 800, function(){
                window.location.hash = hash;
            });
        }
    });

    // --- Chart.js Initialization with Dummy Data ---

    // Chart 1: Stock Value by Item Group (Bar Chart)
    var ctx1 = document.getElementById('stockValueByItemGroupChart').getContext('2d');
    new Chart(ctx1, {
        type: 'bar',
        data: {
            labels: ['Raw Materials', 'Finished Goods', 'Packaging', 'Consumables'],
            datasets: [{
                label: 'Stock Value ($)',
                data: [12000, 18000, 5000, 2500],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.7)',
                    'rgba(54, 162, 235, 0.7)',
                    'rgba(255, 206, 86, 0.7)',
                    'rgba(75, 192, 192, 0.7)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        callback: function(value, index, values) {
                            return '$' + value;
                        }
                    }
                }]
            },
            legend: { display: false },
            title: {
                display: true,
                text: 'Current Stock Value by Item Group'
            }
        }
    });

    // Chart 2: Monthly Stock Movements (Line Chart)
    var ctx2 = document.getElementById('monthlyStockMovementChart').getContext('2d');
    new Chart(ctx2, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [
                {
                    label: 'Material Receipts',
                    data: [1500, 1800, 1200, 2000, 2500, 1900],
                    borderColor: 'rgba(75, 192, 192, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    fill: true,
                    tension: 0.1
                },
                {
                    label: 'Material Issues',
                    data: [1000, 1300, 1500, 1800, 2200, 1700],
                    borderColor: 'rgba(255, 99, 132, 1)',
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    fill: true,
                    tension: 0.1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            },
            title: {
                display: true,
                text: 'Monthly Stock Movements (Quantity)'
            }
        }
    });

    // Chart 3: Purchase Order Status (Doughnut Chart)
    var ctx3 = document.getElementById('poStatusChart').getContext('2d');
    new Chart(ctx3, {
        type: 'doughnut',
        data: {
            labels: ['Received', 'To Receive', 'Cancelled'],
            datasets: [{
                data: [70, 20, 10], // Dummy percentages
                backgroundColor: [
                    'rgba(40, 167, 69, 0.7)', // Green
                    'rgba(255, 193, 7, 0.7)',  // Yellow
                    'rgba(108, 117, 125, 0.7)' // Grey
                ],
                borderColor: [
                    'rgba(40, 167, 69, 1)',
                    'rgba(255, 193, 7, 1)',
                    'rgba(108, 117, 125, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            title: {
                display: true,
                text: 'Purchase Order Status Breakdown'
            }
        }
    });

    // Chart 4: Sales Order Status (Doughnut Chart)
    var ctx4 = document.getElementById('soStatusChart').getContext('2d');
    new Chart(ctx4, {
        type: 'doughnut',
        data: {
            labels: ['Delivered', 'To Deliver', 'Cancelled'],
            datasets: [{
                data: [60, 30, 10], // Dummy percentages
                backgroundColor: [
                    'rgba(0, 123, 255, 0.7)',  // Blue
                    'rgba(23, 162, 184, 0.7)', // Teal
                    'rgba(108, 117, 125, 0.7)' // Grey
                ],
                borderColor: [
                    'rgba(0, 123, 255, 1)',
                    'rgba(23, 162, 184, 1)',
                    'rgba(108, 117, 125, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            title: {
                display: true,
                text: 'Sales Order Status Breakdown'
            }
        }
    });
});