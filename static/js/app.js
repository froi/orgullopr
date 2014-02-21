function main() {

	var pueblos = puertoRico.svg.selectAll('.pueblos');
	console.log(pueblos);
	pueblos.on('mousemove', function(d,i){
		var mouse = d3.mouse(puertoRico.svg.node()).map(function(d) { return parseInt(d); });
		{% autoescape false %}
		var tooltipHtml = '<span id=' + d.properties.NAME + '>Name: ' + d.properties.NAME + '</span>'+ 
			'<br />' +
			'<div class="video" id="video-' + d.properties.NAME + '">' +
			'<iframe width="100" height="100" src="//www.youtube.com/embed/cHTyUz86fMY?list=PL65XgbSILalV-wInUiERrhjweMlJkukMd" frameborder="0" allowfullscreen></iframe>' +
			'</div>'
		{% endautoescape %}
		tooltip.html(tooltipHtml)
			.transition()
			.duration(300)
			.style('visibility', 'visible')
			.style('left', (mouse[0] + 25) + 'px')
			.style('top', mouse[1] + 'px');

    })
    .on('mouseover', function(d, i) {
    	d3.select(this).style('stroke-width', 3).style('fill', 'red');
    })
    .on("mouseout",  function(d,i) {
    	d3.select(this).style('stroke-width', 2).style('fill', 'white');
    	tooltip.style('visibility', 'hidden').html('');
    });

}