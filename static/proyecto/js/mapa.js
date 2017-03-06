function cargarmapa() {
	var map = new ol.Map({ 
	   layers: [ 
	     new ol.layer.Tile({ 
	        source: new ol.source.OSM() 
	     }) 
	   ], 
	   renderer: 'canvas',
	   target: 'map', 
	   view: new ol.View({ 
	     center: [0, 0], 
	     zoom: 2 
	   }) 
	});
}