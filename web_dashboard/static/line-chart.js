function drawGraph(data, divId) {
    // Process data
    data.forEach(function (d) {
        d.timestamp = d3.time.format("%Y-%m-%d").parse(d.timestamp);
        d.price = +d.price;
    });

    // Set the dimensions of the svg
    var margin = {
        top: 30,
        right: 50,
        bottom: 30,
        left: 50
    };
    var svgWidth = 600;
    var svgHeight = 270;
    var graphWidth = svgWidth - margin.left - margin.right;
    var graphHeight = svgHeight - margin.top - margin.bottom;

    // Create svg
    var svg = d3.select("#" + divId)
        .append("svg")
        .attr("width", svgWidth)
        .attr("height", svgHeight)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")")

    // Set the ranges
    var x = d3.time.scale().range([0, graphWidth]);
    var y = d3.scale.linear().range([graphHeight, 0]);

    x.domain(d3.extent(data, d => d.timestamp));
    y.domain([d3.min(data, d => d.price),d3.max(data, d => d.price)]);

    // Add line
    var line = d3.svg.line()
        .x(d => x(d.timestamp))
        .y(d => y(d.price));

    svg.append("path")
        .style("stroke", "green")
        .style("fill", "none")
        .attr("class", "line")
        .attr("d", line(data));

    // Add axes
    var xAxis = d3.svg.axis().scale(x)
        .orient("bottom").ticks(5);
    var yAxis = d3.svg.axis().scale(y)
        .orient("left").ticks(5);

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + graphHeight + ")")
        .call(xAxis);

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis);
};