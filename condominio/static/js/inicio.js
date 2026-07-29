google.charts.load('current', {'packages':['corechart', 'bar']});

function drawWaterConsumptionChart() {
    // Add your water consumption data here
    // and adapt the options to fit the data
    var data = new google.visualization.ArrayRow([
        ['Jan', 120],
        ['Feb', 140],
        ['Mar', 115],
        ['Apr', 130],
        ['May', 150],
        ['Jun', 165],
        ['Jul', 170],
        ['Aug', 185],
        ['Sep', 190],
        ['Oct', 210],
        ['Nov', 220],
        ['Dec', 235]
    ]);

    var options = {
        title: 'Water Consumption',
        curveType: 'function',
        legend: { position: 'bottom' }
    };

    var chart = new google.visualization.LineChart(document.getElementById('water-consumption-chart'));
    chart.draw(data, options);
}

function drawGasConsumptionChart() {
    // Add your gas consumption data here
    // and adapt the options to fit the data
    var data = new google.visualization.ArrayRow([
        ['Jan', 100],
        ['Feb', 120],
        ['Mar', 90],
        ['Apr', 115],
        ['May', 125],
        ['Jun', 140],
        ['Jul', 150],
        ['Aug', 165],
        ['Sep', 180],
        ['Oct', 195],
        ['Nov', 205],
        ['Dec', 215]
    ]);

    var options = {
        title: 'Gas Consumption',
        curveType: 'function',
        legend: { position: 'bottom' }
    };

    var chart = new google.visualization.LineChart(document.getElementById('gas-consumption-chart'));
    chart.draw(data, options);
}

function drawCashFlowChart() {
    // Add your cash flow data here
    // and adapt the options to fit the data
    var data = new google.visualization.ArrayRow([
        ['Jan', 10000, 12000, 15000],
        ['Feb', 12000, 14000, 18000],
        ['Mar', 11000, 1200, 17000],
        ['Apr', 9000, 14000, 18000],
        ['May', 7000, 16000, 19000],
        ['Jun', 10000, 18000, 20000]
    ]);

    var options = {
        title: "Cash Flow",
        curveType: 'function',
        legend: { position: 'bottom' }
    };

    var dataTable = google.visualization.arrayToDataTable(data, true);

    var formatter = new google.visualization.NumberFormat({
        pattern: '$,##0.00'
    });

    formatter.format(dataTable, 1);
    formatter.format(dataTable, 2);

    var chart = new google.visualization.LineChart(document.getElementById("cash-flow-chart"));
    chart.draw(dataTable, options);
}

function drawBarChart() {
    // Add your bar chart data here
    // and adapt the options to fit the data
    var data = google.visualization.arrayToDataTable([
        ['Category', 'Value', 'Type'],
        ['Receita', 20000, 'Received'],
        ['Receita', 25000, 'Expected'],
        ['Expenses', 12000, 'Paid'],
        ['Expenses', 10000, 'Expected'],
    ]);

    var options = {
        title: 'Budget',
        chart: {
            title: 'Budget',
            subtitle: 'Comparing Expenses and Receipts',
        },
        bars: 'horizontal',
        vAxis: {
            title: 'Value',
            titleTextStyle: {
                color: 'blue',
            },
        },
        hAxis: {
            title: 'Category',
            titleTextStyle: {
                color: 'black',
            },
        },
        series: {
            0: { color: 'green' },
            1: { color: 'red' },
        },
    };

    var chart = new google.visualization.BarChart(document.getElementById("bar-chart"));
    chart.draw(data, options);
}

// Call the functions to draw the charts
google.charts.setOnLoadCallback(drawWaterConsumptionChart);
google.charts.setOnLoadCallback(drawGasConsumptionChart);
google.charts.setOnLoadCallback(drawCashFlowChart);
google.charts.setOnLoadCallback(drawBarChart);