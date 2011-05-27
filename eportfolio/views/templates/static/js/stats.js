$(function () {

    var stack = 0, bars = true, lines = false, steps = false;

    function plotWithOptions() {
        $.plot($("#placeholder"), graph_data, {
            series: {
                stack: stack,
                lines: { show: lines, steps: steps },
                bars: { show: bars, barWidth: 0.6, align: "center" }
            },
            xaxis : {
                ticks: graph_axis,
                autoscaleMargin: 0.02
            },
            yaxis : {
                min: 0,
                tickDecimals: 0,
                minTickSize: 1
            },
            legend: { 
                position: 'ne',
                noColumns: 2
            }
        });
    }

    plotWithOptions();

});