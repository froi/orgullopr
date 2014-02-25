var orgullopr = {
	SCRIPT_ROOT: '',
	gridster: {},
	init: function() {
		this.SCRIPT_ROOT = '{{ request.script_root|tojson|safe }}'; // application location

		this.gridster = $('.gridster ul').gridster({
			widget_margins: [10, 10],
			widget_base_dimensions: [140, 140],
			max_cols: 4,
			min_rows: 1
		});
	}
};

var mapOperator = {
    puertoRico: {},
    pueblos: {},
    tooltip: {},
    youTubeAPIKey: '{{ youTubeAPIKey }}', // TODO: eliminate when dev if finished
    init: function() {
//    	this.tooltip = d3.select('#map').append('div').attr('class', 'tooltip');
      	var config = {
	      	node: $('#map')[0],
	  		tiles: ['pueblos'],
	  		size: 'medium',
            'background-color': 'rgba(104,203,245,1)',
            'stroke-color': 'rgba(255,255,255,1)',
            'stroke-width': 2,
            'mouseover-stroke-width': 5,
            'mouseover-labels': true,
	  		events: {
	  			on_ready: mapOperator.bindActions,
	 			on_click: mapOperator.seeTownVideos
	  		}
	 		
      	};
      	this.puertoRico = new AtlasPR(config);
    },

    seeTownVideos: function(feature, svg_path) {
        alert('This will come soon, but you clicked on: ' + feature.properties.NAME);
    },
    getTownVideos: function(feature, svg_path) {
    	var videos = {};
    	$.ajax({
    		type: 'GET',
    		url: '/municipios/' + feature.properties.NAME,
    		contentType: 'application/json',
    		dataType: 'json',
    		success: function(data) {
    			for (var i = 0; i < data.length; i++) {
    				var li = $('<li />', { class: 'new'} ).append($('<iframe />', {
    					src: data[i]['youtube_link'],
    					name: data[i]['name']
    				}));
    				$('ul').append(li.html());
    				//orgullopr.gridster.add(li.html());
    			}
    		}
    	});
    },

    getPlayListItems: function(playListID) {
		var playListID = 'PL5Mlzwwjsgub3w0W18UFcIn3d998mPqXC'; // @todo -- bye bye once abstracted
      	var url = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=' +
      	playListID +
      	'&key=' +
      	this.youTubeAPIKey;

      	$.ajax({
          	type: 'GET',
          	url: url,
          	async: false,
          	contentType: "application/json",
          	dataType: 'jsonp',
          	success: function(res) {
            	console.log(res);
          	}
      	});
    },

    bindActions: function() {
        mapOperator.getPlayListItems('ten');
        var pueblos = mapOperator.puertoRico.svg.selectAll('.pueblos');
        pueblos.on('mousemove', function(d,i){
            var mouse = d3.mouse(mapOperator.puertoRico.svg.node()).map(function(d) { return parseInt(d); });
            mapOperator.tooltip.html('<span id=' + d.properties.NAME + '>Name: ' + d.properties.NAME + '</span>'+
                '<br />' +
                '<div class="video" id=video-' + d.properties.NAME + '>' +
                '<iframe width="100" height="100" src="//www.youtube.com/embed/cHTyUz86fMY?list=PL65XgbSILalV-wInUiERrhjweMlJkukMd" frameborder="0" allowfullscreen></iframe>' +
                '</div>')
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
            mapOperator.tooltip.style('visibility', 'hidden').html('');
            // tooltip.classed("hidden", true)
        });

    }
}