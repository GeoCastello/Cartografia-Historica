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


$(document).ready(inicializa); //Ejecuta la función inicializa cuando el documento
//está totalmente cargado