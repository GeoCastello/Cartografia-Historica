function inicializa() {
  $('nav#menu a').click(click_menu); //Conecta el click de todos los a
  //dentro del nav id=menu a la función click_menu
  crea_mapa();
}

var url= URL
var form_id= "none"


function click_menu() {
	//alert('Click menu: '+this.id);
	var opcion='aplicacion='+this.id;
	id_pag=this.id
	if (id_pag == form_id){
		document.getElementById('tablas').style.display = 'block';		
	}
	else{
		document.getElementById('tablas').style.display = 'none';		
	}
	
	menu_active(this.id);
	if (this.id!='bgrafica' && this.id!='inicio') {
		document.getElementById('mapa').style.display = 'none';
	}
	else {
		document.getElementById('mapa').style.display = 'block';
	}
	$.ajax({
		type: "GET",
		url: url,
		data: opcion, //Adjuntar los campos del formulario enviado
		success: reemplaza_cuerpo
	});		
	return false; //Evitar ejecutar el submit del formulario.
}

function reemplaza_cuerpo(datos) {
	var cuerpo=$("#seccion");
	cuerpo.replaceWith(datos)	
}

function crea_tablas(datos) {
	var respuesta=$.parseJSON(datos);
	if (respuesta.seccion=="#tablas" ||  respuesta.seccion=="#municipio_final"){
		var cuerpo=$(respuesta.seccion);
		cuerpo.replaceWith(respuesta.html);
		if (respuesta.seccion=="#municipio_final"){
			document.getElementById('municipio_final').style.display = 'block';		
		}
		else {
			if (respuesta.limite!="none") {
				alert(respuesta.limite+" Si desea una copia de todos los registros, diríjase a la web: http://")
			}
		}
	}
	if (respuesta.extension!="null"){
		var extension=$.parseJSON(respuesta.extension)
		zoom(extension.coordinates);
	}
	if (respuesta.seccion=="#reg_opinion"){
		alert(respuesta.mensaje)
		limpiar()
	}
	
	//****************************************************** ESTADISTICAS *************************************************//
	if (respuesta.seccion=="#estadisticas_gen"){
		var valores_x=respuesta.valores_x;
		var valores_stat=respuesta.valores_stat;
		var unidades=respuesta.unidades;
		var orientacion=respuesta.orientacion;
		var mensaje=respuesta.mensaje;
		var prov_mensaje=respuesta.prov_mensaje;
		
		try {
			d3.selectAll("svg").remove();
			d3.selectAll("p").remove();
			d3.selectAll(".info_box").remove();
		}
		catch (err) {
			pass;
		}
		
		d3.select("#estadisticas_sec")
			.append("p")
			.attr("id", "value_stat")
			.attr("class", "value_stat")
			.style("text-align", "center");
		//**************************ESTADISTICAS***********************************//
		var margin_rstat={top: 10, left: 10, bottom: 10, right: 10}
		var width_rstat1=parseInt(d3.select('#estadisticas_sec').style('width'))
		var width_rstat=width_rstat1-margin_rstat.left-margin_rstat.right
		var mapRatio= .5
		var height_rstat=width_rstat*mapRatio;

		var barPadding=1;
		
		if (orientacion=="vertical"){
			var estadisticas_gen=d3.select("#estadisticas_sec")
				.append( "svg" )
				.attr( "width", width_rstat )
				.attr( "height", height_rstat )
				.attr("class", "stats");
			//**********************************AXIS*************************************//
			var formatNumber=d3.format(".4")
			//**********************************X AXIS*************************************//
			xScale=d3.scaleBand()
				.rangeRound([0, (width_rstat-width_rstat/10)])
				.padding(0);
			xScale.domain(valores_x);
	
			xAxis=d3.axisBottom()
				.scale(xScale);
	
			estadisticas_gen.append("g")
				.attr("class", "xaxis")
				.attr("transform", "translate("+(margin_rstat.left*7)+","+(height_rstat-(margin_rstat.bottom*20))+")")
				.call(xAxis);
			    
	
			estadisticas_gen.selectAll(".xaxis text")  // select all the text elements for the xaxis
		        .attr("transform", "translate(-5,0) rotate(-45)")
		        .style("text-anchor", "end");
			
			//**********************************Y AXIS*************************************//
			yScale=d3.scaleLinear()
				.range([(height_rstat-(margin_rstat.bottom*20)), 0]);
			yScale.domain([0, d3.max(valores_stat)]);
	
			yAxis=d3.axisLeft()
				.scale(yScale)
				.tickFormat(formatNumber);
	
			estadisticas_gen.append("g")
				.attr("class", "yaxis")
				.attr("transform", "translate("+(margin_rstat.left*7)+",0)")
				.call(yAxis);
			
			//********************************** INFO BOX ********************************//
			var tooltip = d3.select("body")
			    .append("div")
			    .attr("class", "info_box")
			    .style("position", "absolute")
			    .style("z-index", "10")
			    .style("text-shadow", "1px 1px #FFF")
			    .style("visibility", "hidden")
			    
			//**********************************GRAPH************************************//
			max_value = Math.max.apply(Math, valores_stat);
			estadisticas_gen
				.selectAll("rect")
				.data(valores_stat)
				.enter()
				.append("rect")
				.on("mouseover", function(d,i) {
							d3.select(this).attr("stroke", "#FFF");
							d3.select("#value_stat")
								.style("display", "block");
							tooltip.style("visibility", "visible")
						    	.text(valores_x[i].toUpperCase()+": "+d+" "+unidades);
				})
				.on("mousemove", function(){return tooltip.style("top", (d3.event.pageY-20)+"px").style("left",(d3.event.pageX+20)+"px");})
				.on("mouseout", function(d) {
							d3.select(this).attr("stroke", "#000");
							d3.select("#value_stat");
							tooltip.style("visibility", "hidden");
						})
				.attr("class", "rect_stat")
				.attr("transform", "translate("+(margin_rstat.left*7)+","+(-margin_rstat.bottom-margin_rstat.top)+")")
				.attr("x", function(d, i) {
					return (width_rstat/100)+i*((width_rstat-width_rstat/8.5)/valores_stat.length);
				})
				.attr("y", function(d) {
					return (height_rstat-(margin_rstat.bottom*18))-(d*(height_rstat-(margin_rstat.bottom*20))/max_value);
				})
				.transition().duration(500)
				.attr("width", ((width_rstat-width_rstat/8.5)/valores_stat.length)-barPadding)
				.attr("height", function(d) {
					return (d*(height_rstat-(margin_rstat.bottom*20))/max_value);
				})
				.attr("fill", "#81BEF7")
				.attr("stroke", "#000");
		}
		
		if (orientacion=="horizontal") {
			var height_rstat2=height_rstat*6.5;
			
			var estadisticas_gen=d3.select("#estadisticas_sec")
				.append( "svg" )
				.attr( "width", width_rstat )
				.attr( "height", height_rstat2 )
				.attr("class", "stats");
			//**********************************AXIS*************************************//
			var formatNumber=d3.format(".4")
			//**********************************X AXIS*************************************//
			xScale=d3.scaleLinear().rangeRound([0, (width_rstat-width_rstat/5)]);
			
			xScale.domain([0, d3.max(valores_stat)]);
			
			estadisticas_gen.append("g")
				.attr("class", "x-axis")
				.attr("transform", "translate("+(margin_rstat.left*20)+","+(height_rstat2-(margin_rstat.bottom*5))+ ")")
				.call(d3.axisBottom(xScale));
			
			//**********************************Y AXIS*************************************//
			yScale=d3.scaleBand().rangeRound([0, (height_rstat2-(margin_rstat.bottom*2))]).padding(1);
			yScale.domain(valores_x);
			
			estadisticas_gen.append("g")
			.attr("class", "y-axis")
			.attr("transform", "translate("+(margin_rstat.left*20)+","+(margin_rstat.bottom*2)+ ")")
			.call(d3.axisLeft(yScale).tickSizeOuter(0));
			
			//********************************** INFO BOX ********************************//
			var tooltip = d3.select("body")
			    .append("div")
			    .attr("class", "info_box")
			    .style("position", "absolute")
			    .style("z-index", "10")
			    .style("text-shadow", "1px 1px #FFF")
			    .style("visibility", "hidden")
			    
			//**********************************GRAPH************************************//
			max_value = Math.max.apply(Math, valores_stat);
			estadisticas_gen
				.selectAll("rect")
				.data(valores_stat)
				.enter()
				.append("rect")
				.on("mouseover", function(d,i) {
							d3.select(this).attr("stroke", "#FFF");
							d3.select("#value_stat")
								.style("display", "block");
							tooltip.style("visibility", "visible")
						    	.text(valores_x[i].toUpperCase()+": "+d+" "+unidades);
				})
				.on("mousemove", function(){return tooltip.style("top", (d3.event.pageY-20)+"px").style("left",(d3.event.pageX+20)+"px");})
				.on("mouseout", function(d) {
							d3.select(this).attr("stroke", "#000");
							d3.select("#value_stat");
							tooltip.style("visibility", "hidden");
						})
				.attr("class", "rect_stat")
				.attr("transform", "translate(1,"+height_rstat2/43+")")
				.attr("x", function(d) {
					return (margin_rstat.left*20);
				})
				.attr("y", function(d, i) {
					return i*((height_rstat2-(margin_rstat.bottom*13.5))/valores_stat.length);
				})
				.transition().duration(500)
				.attr("width", function(d) {
					return (d*(width_rstat-(margin_rstat.bottom*30))/max_value);
				})
				.attr("height", ((height_rstat*6)/valores_stat.length))
				.attr("fill", "#81BEF7")
				.attr("stroke", "#000");
		}
		
		if (mensaje=='true') {
			alert("Por favor, seleccione una estadística")
		}
		
		if (prov_mensaje!='null') {
			alert(prov_mensaje);
		}
	}
	
	
}

function limpiar(){
	document.getElementById('nombre').value="";
	document.getElementById('apellido').value="";
	document.getElementById('tipo_titulacion').value="Sin especificar";
	document.getElementById('tipo_trabajo').value="Sin especificar";
	document.getElementById('mejoras').value="";
	document.formulario_opinion.utilidad[0].checked=true
	
	}

function resetear(f) {
	var text='<select id="municipio_final" name="municipio_final" required><option value="iniciado">Seleccione un municipio</option></select>'
	var cuerpo=$('#municipio_final');
	cuerpo.replaceWith(text)
	document.getElementById('municipio_final').style.display = 'none';	
}

function reset_stats() {
	document.getElementById('tipo_estadistica').value='sin_especificar';
}

function boton_enviar(f){
	if (document.getElementById('municipio_final').value!="iniciado"){
		document.getElementById('type-form').value="send"
	}
	else{
		document.getElementById('type-form').value="search"		
	}
	enviar_formulario(f)
}

function enviar_formulario(f) {
	//Aquí no se tiene acceso a this porque el evento onclick es lanzado desde html
	//por eso recibe f, que es el formulario del botón desde el cual se ha lanzado
	//el evento onclick
	//No se puede hacer desde la función inicializa porque el formulario no está creado
	//todavía, ya que se crean por ajax, después de cargar la página principal
	form_id=id_pag
	var v=$(f).serialize() //extrrae los valores del formulario y los introduce
						   //en forma de cadena en la variable v
						   //serialize no tiene en cuenta los campos disabled.
						   //serialize es un método JQUERY
	$.ajax({
		type: "POST",
		url: url,
		//data: $(nombre_form).serialize(), //Adjuntar los campos del formulario enviado.
		data: v, //Otr forma de adjuntarlos
		success: crea_tablas,
		error:function (xhr, ajaxOptions, thrownError) {
		alert(xhr.status + '\n' + thrownError);
		}
		});
	return false; //Evitar ejecutar el submit del formulario
}

function menu_active(id) {
	$('nav#menu li').removeClass('active')
	document.getElementById(id+"_li").className='active'
}

function zoom(bbox) {
	map.getView().fit([bbox[0][0][0],bbox[0][0][1],bbox[0][2][0],bbox[0][2][1]], map.getSize())
}

function click_tabla(valor){
	var sentencia = "nombre-form=click_tabla&result="+String(valor);
	enviar_click(sentencia)
}

function gestion_coords(evt){
    var coordinate = evt.coordinate;
    var list = String(coordinate).split(",");
    var sentencia = "nombre-form=click_mapa&lon="+String(list[0])+"&lat="+String(list[1]);
	form_id=id_pag;
	enviar_click(sentencia)
}

function enviar_click(sentencia) {
	$.ajax({
		type: "POST",
		url: url,
		//data: $(nombre_form).serialize(), //Adjuntar los campos del formulario enviado.
		data: sentencia, //Otr forma de adjuntarlos
		success: crea_tablas,
		error:function (xhr, ajaxOptions, thrownError) {
		alert(xhr.status + '\n' + thrownError);
		}
		});
	return false; //Evitar ejecutar el submit del formulario
}


function abrir_web(url){
	// window.open(url, "_self");
	window.open(url);
}

function enviar_provincias(f) {
	//Here you don't have the acces to 'this' because the event onClick is launched
	//from html; for that it receives f; this is the formular of the button from which 
	//the event onClick is launched.
	//it can't be done from the initialize function because the formular is not created
	//yet, because it's created by ajax, after loading the main page
	
	var v=$(f).serialize() //It extracts the values of the formular and introduce them
	   //like an string on the variable v
	   //serialize has not into account the dissabled fields.
	   //serialize is a JQUERY method.

	$.ajax({
	type: "POST",
	url: url,
	//data: $(nombre_form).serialize(), //Add the fields of the sended formular.
	data: v, //Otr forma de adjuntarlos
	success: generar_provincias,
	error:function (xhr, ajaxOptions, thrownError) {
	alert(xhr.status + '\n' + thrownError);
	}
	});
	return false; //Avoid to execute the submit of the formular	
}

function generar_provincias(data) {
	var response=$.parseJSON(data);
	if (response.geom_type!='null'){
		var types=response.geom_type;
		var list=new Array();
		list[0]="Seleccione una provincia";
		for (var i = 0; i<types.length; i++) {
			list[i+1]=types[i][0].toString();
		}
		var options='';
		for (var j = 0; j<list.length; j++) {
			if (list[j]=="Seleccione una provincia") {
				options+='<option value="sin_especificar">'+list[j]+'</option>';
			}
			else {
				options+='<option value="'+list[j]+'">'+list[j]+'</option>';
			}
		}
		document.getElementById('tipo_provincia').innerHTML=options;
	}
}


$(document).ready(inicializa); //Ejecuta la función inicializa cuando el documento
//está totalmente cargado