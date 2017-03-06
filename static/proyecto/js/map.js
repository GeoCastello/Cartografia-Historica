function crea_mapa() {
	
	map = new ol.Map({
	      target: 'map',
	      renderer: 'canvas',
	      layers: [
	        new ol.layer.Tile({
			   source: new ol.source.OSM()
			}),
	        new ol.layer.Tile({
	            source: new ol.source.TileWMS({
                  url: URL_IDE_WMS,
                  params: {LAYERS: 'autonomias'}
	                
              })
	        }),
	        new ol.layer.Tile({
              source: new ol.source.TileWMS({
                  url: URL_IDE_WMS,
                  params: {LAYERS: 'provincias'}
              })
            }),
            new ol.layer.Tile({
              source: new ol.source.TileWMS({
                  url: URL_IDE_WMS,
                  params: {LAYERS: 'municipios'}
              })
          })],
        
	        view: new ol.View({ 
	        	  projection: 'EPSG:4326',
	              center: [-3.8110059,40.4245521], 
	              zoom: 5 
	            })
	  });

	map.on('singleclick', gestion_coords);//enlaza el click con la función gestion_coords
}