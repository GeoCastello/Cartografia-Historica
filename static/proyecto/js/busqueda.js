function z_busqueda(zona) {
	
	if (zona=="peninsula") {
		document.getElementById('com_aut').disabled=false;
		var lista=new Array();
		lista[0]="Seleccione una Comunidad Autónoma";
		lista[1]="Andalucía";
		lista[2]="Aragón";
		lista[3]="Principado de Asturias";
		lista[4]="Cantabria";
		lista[5]="Castilla-La Mancha";
		lista[6]="Castilla y León";
		lista[7]="Cataluña/Catalunya";
		lista[8]="Comunidad Valenciana/Comunitat Valenciana";
		lista[9]="Extremadura";
		lista[10]="Galicia";
		lista[11]="La Rioja";
		lista[12]="Comunidad de Madrid";
		lista[13]="Comunidad Foral de Navarra";
		lista[14]="País Vasco/Euskadi";
		lista[15]="Región de Murcia";
		map.getView().fit([-9.50, 43.79, 3.33, 36.00], map.getSize())
	}
		
	else if (zona=="baleares") {
		document.getElementById('com_aut').disabled=false;
		var lista=new Array();
		lista[0]="Seleccione una Comunidad Autónoma";
		lista[1]="Islas Baleares/Illes Balears";
		map.getView().fit([1.15, 40.10, 4.33, 38.63], map.getSize())
	}
	
	else if (zona=="canarias") {
		document.getElementById('com_aut').disabled=false;
		var lista=new Array();
		lista[0]="Seleccione una Comunidad Autónoma";
		lista[1]="Islas Canarias";
		map.getView().fit([-18.17, 29.42, -13.40, 27.62], map.getSize())
	}

	else if (zona=="ceuta_melilla") {
		document.getElementById('com_aut').disabled=false;
		var lista=new Array();
		lista[0]="Seleccione una Comunidad Autónoma";
		lista[1]="Ciudad Autónoma de Ceuta";
		lista[2]="Ciudad Autónoma de Melilla";
		map.getView().fit([ -5.39, 35.92, -2.93, 35.26], map.getSize())		
	}
	
	else {
		var lista=new Array();
		document.getElementById('com_aut').disabled=true;
	}
	
	var options='';
		
	for (var i = 0; i<lista.length; i++) {
		if (lista[i]=="Seleccione una Comunidad Autónoma") {
			options+='<option value="none">'+lista[i]+'</option>';
		}
		else {
			options+='<option value="'+lista[i]+'">'+lista[i]+'</option>';
		}
	}
	
	document.getElementById('com_aut').innerHTML=options;	
	document.getElementById('provincia').innerHTML="";
	document.getElementById('provincia').disabled=true;

}

function c_autonoma(zona, f) {
    if (zona=="Andalucía") {
            var lista=new Array();
            document.getElementById('provincia').disabled=false;
    		lista[0]="Seleccione una Provincia";
            lista[1]="Almería";
            lista[2]="Cádiz";
            lista[3]="Córdoba";
            lista[4]="Granada";
            lista[5]="Huelva";
            lista[6]="Jaén";
            lista[7]="Málaga";
            lista[8]="Sevilla";
    }
    else if (zona=="Aragón") {
        var lista=new Array();
        document.getElementById('provincia').disabled=false;
        lista[0]="Seleccione una Provincia";
        lista[1]="Huesca";
        lista[2]="Teruel";
        lista[3]="Zaragoza";
    }
    else if (zona=="Principado de Asturias") {
        var lista=new Array();
        document.getElementById('provincia').disabled=false;
        lista[0]="Seleccione una Provincia";
        lista[1]="Asturias";
    }
    else if (zona=="Islas Baleares/Illes Balears") {
        var lista=new Array();
        document.getElementById('provincia').disabled=false;
        lista[0]="Seleccione una Provincia";
        lista[1]="Islas Baleares/Illes Balears";
    }
    else if (zona=="Islas Canarias") {
        var lista=new Array();
        document.getElementById('provincia').disabled=false;
        lista[0]="Seleccione una Provincia";
        lista[1]="Las Palmas";
        lista[2]="Santa Cruz de Tenerife";
    }
    else if (zona=="Cantabria") {
        var lista=new Array();
        document.getElementById('provincia').disabled=false;
        lista[0]="Seleccione una Provincia";
        lista[1]="Cantabria";
    }
    else if (zona=="Castilla-La Mancha") {
        var lista=new Array();
        document.getElementById('provincia').disabled=false;
        lista[0]="Seleccione una Provincia";
        lista[1]="Albacete";
        lista[2]="Ciudad Real";
        lista[3]="Cuenca";
        lista[4]="Guadalajara";
        lista[5]="Toledo";
    }
    else if (zona=="Castilla y León") {
        var lista=new Array();
        document.getElementById('provincia').disabled=false;
        lista[0]="Seleccione una Provincia";
        lista[1]="Ávila";
        lista[2]="Burgos";
        lista[3]="León";
        lista[4]="Palencia";
        lista[5]="Salamanca";
        lista[6]="Segovia";
        lista[7]="Soria";
        lista[8]="Valladolid";
        lista[9]="Zamora";
    }
    else if (zona=="Cataluña/Catalunya") {
        var lista=new Array();
        document.getElementById('provincia').disabled=false;
        lista[0]="Seleccione una Provincia";
        lista[1]="Barcelona";
        lista[2]="Gerona/Girona";
        lista[3]="Lérida/Lleida";
        lista[4]="Tarragona";
    }
    else if (zona=="Comunidad Valenciana/Comunitat Valenciana") {
        var lista=new Array();
        document.getElementById('provincia').disabled=false;
        lista[0]="Seleccione una Provincia";
        lista[1]="Alicante/Alacant";
        lista[2]="Castellón/Castelló";
        lista[3]="Valencia/València";
    }
    else if (zona=="Extremadura") {
        var lista=new Array();
        document.getElementById('provincia').disabled=false;
        lista[0]="Seleccione una Provincia";
        lista[1]="Badajoz";
        lista[2]="Cáceres";
    }
    else if (zona=="Galicia") {
        var lista=new Array();
        document.getElementById('provincia').disabled=false;
        lista[0]="Seleccione una Provincia";
        lista[1]="A Coruña";
        lista[2]="Lugo";
        lista[3]="Ourense";
        lista[4]="Pontevedra";
    }
    else if (zona=="La Rioja") {
        var lista=new Array();
        document.getElementById('provincia').disabled=false;
        lista[0]="Seleccione una Provincia";
        lista[1]="La Rioja";
    }
    else if (zona=="Comunidad de Madrid") {
        var lista=new Array();
        document.getElementById('provincia').disabled=false;
        lista[0]="Seleccione una Provincia";
        lista[1]="Madrid";
    }
    else if (zona=="Comunidad Foral de Navarra") {
        var lista=new Array();
        document.getElementById('provincia').disabled=false;
        lista[0]="Seleccione una Provincia";
        lista[1]="Navarra";
    }
    else if (zona=="País Vasco/Euskadi") {
        var lista=new Array();
        document.getElementById('provincia').disabled=false;
        lista[0]="Seleccione una Provincia";
        lista[1]="Álava/Araba";
        lista[2]="Guipúzcoa/Gipuzkoa";
        lista[3]="Vizcaya/Bizkaia";
    }
    else if (zona=="Región de Murcia") {
        var lista=new Array();
        document.getElementById('provincia').disabled=false;
        lista[0]="Seleccione una Provincia";
        lista[1]="Murcia";
    }
    else if (zona=="Ciudad Autónoma de Ceuta") {
        var lista=new Array();
        document.getElementById('provincia').disabled=false;
        lista[0]="Seleccione una Provincia";
        lista[1]="Ceuta";
    }
    else if (zona=="Ciudad Autónoma de Melilla") {
        var lista=new Array();
        document.getElementById('provincia').disabled=false;
        lista[0]="Seleccione una Provincia";
        lista[1]="Melilla";
    }
    else {
        var lista=new Array();
        document.getElementById('provincia').disabled=true;
        
    }
    if (zona!="none") {
    	document.getElementById('type-form').value="c_autonoma";
    	enviar_formulario(f);
    }

    var options='';
        
    for (var i = 0; i<lista.length; i++) {
		if (lista[i]=="Seleccione una Provincia") {
			options+='<option value="none">'+lista[i]+'</option>';			
		}
		else{
        	options+='<option value="'+lista[i]+'">'+lista[i]+'</option>';
			}
		}
    document.getElementById('provincia').innerHTML=options;
}

function b_provincia(zona, f) {
	document.getElementById('type-form').value="prov";
    if (zona!="none") {
    	enviar_formulario(f);
    }

}
		
		
		
		
		
		