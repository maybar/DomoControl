
function lee_status_json() {
    //var output1 = document.getElementById('output1');
    
    var xmlhttp = new XMLHttpRequest();
    var url = "http://192.168.1.109:8000/status.json";

    xmlhttp.onreadystatechange=function() {
        if (this.readyState == 4 && this.status == 200) {
            var datos_json = JSON.parse(this.responseText);
            output1.innerHTML = "json recibido";
            write_form(datos_json);
        }
    }
    xmlhttp.open("GET", url, true);
    xmlhttp.send();

}

function write_form(datos_json){
    //output1.innerHTML = "escribiendo....";
    var estado_caldera = {
        false : "DESACTIVADA",
        true  : "ACTIVADA"
    };
    temp1.innerHTML = "Temperatura actual: " + datos_json.temp1+ " ºC";
    hum.innerHTML = "Humedad actual: " + datos_json.hum+ " %";
    mode.innerHTML = "Modo de operación: " + datos_json.mode;
    temp2.innerHTML = "Temperatura deseada: " + datos_json.temp2+ " ºC";
    state.innerHTML = "Estado de caldera: " + estado_caldera[datos_json.state];
    time.innerHTML = "Tiempo de activación: " + datos_json.time;
    pir.innerHTML = "Detector de presencia: " + datos_json.pir;
    alarma.innerHTML = "Alarma: " + datos_json.alarma;
    
    //document.getElementById("T1").value = datos_json.temp_1;
    //document.getElementById("T2").value = datos_json.temp_2;
    //document.getElementById("T3").value = datos_json.temp_3;
    //output1.innerHTML = " ";
}


