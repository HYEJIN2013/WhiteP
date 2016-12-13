var margin = {top: 20, right: 30, bottom: 50, left: 40},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var xScale = d3.scale.ordinal()
    .rangeRoundBands([0, width],.15);

var yScale = d3.scale.linear()
    .range([height, 0]);

var xAxis = d3.svg.axis()
    .scale(xScale)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(yScale)
    .orient("left");

var tooltip = d3.select("body").append("div")
    .style("position", "absolute")
    .style("padding", "0 10px")
    .style("background", "white")
    .style("opacity", 0);

var chart3 = d3.select(".chart3")
    .attr("width", width + margin.right + margin.left)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.right + ")");

// Force a given string of data to a number
function typecheck(d) {
    d.makes = +d.makes;
    d.attempts = +d.attempts;
    return d;
}

var xGroupedScale = d3.scale.ordinal();

var color = d3.scale.ordinal()
    .range(['#d33682', '#268bd2']);

var tempColor;

// Chart 3 - Makes and Attempts (Grouped Bar)
d3.tsv("data.tsv", typecheck, function(error, data) {
    var dataGroup = d3.keys(data[0]).filter(function(key) {return key !== "year"; });

    data.forEach(function(d) {
        d.values = dataGroup.map(function(name) {return {name: name, value: +d[name]}; });
    });
    
    xScale.domain(data.map(function(d) {return d.year}));
    xGroupedScale.domain(dataGroup).rangeRoundBands([0, xScale.rangeBand()]);
    yScale.domain([0, d3.max(data, function (d) { return d.attempts; })]);

    chart3.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis)
        .selectAll("text")
        .attr("y", 0)
        .attr("x", 9)
        .attr("dy", ".35em")
        .attr("transform", "rotate(90)")
        .style("text-anchor", "start");

    chart3.append("g")
        .attr("class", "y axis")
        .call(yAxis)

    var year = chart3.selectAll(".year")
        .data(data)
        .enter().append("g")
        .attr("class", "g")
        .attr("transform", function(d) {
            return "translate(" + xScale(d.year) + ",0)";});

    year.selectAll("rect")
        .data(function(d) { return d.values; })
        .enter().append("rect")
        .attr("width", xGroupedScale.rangeBand())
        .attr("x", function(d) { return xGroupedScale(d.name); })
        .attr("y", function(d) { return yScale(d.value); })
        .attr("height", function(d) { return height - yScale(d.value); })
        .style("fill", function(d) { return color(d.name); })

        .on("mouseover", function(d) {
            tempColor = color(d.name);

            d3.select(this)
                .transition().duration(100)
                .style("fill", '#b58900');

            tooltip.transition()
                .style("opacity", .9);

            tooltip.html(d.value)
                .style("left", (d3.event.pageX + 5) + "px")
                .style("top", (d3.event.pageY - 25) + "px")
        })
        .on("mouseout", function(d) {
            d3.select(this)
                .transition().duration(250)
                .style("fill", tempColor);

            tooltip.transition()
                .style("opacity", 0);
        })

});
