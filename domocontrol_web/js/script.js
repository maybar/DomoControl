
function lee_json() {
    var output1 = document.getElementById('output1');
    //output1.innerHTML = "leyendo....";
    var xmlhttp = new XMLHttpRequest();
    var url = "http://192.168.1.109:8000/config.json";

    xmlhttp.onreadystatechange=function() {
        if (this.readyState == 4 && this.status == 200) {
            var datos_json = JSON.parse(this.responseText);
            write_form(datos_json);
        }
    }
    xmlhttp.open("GET", url, true);
    xmlhttp.send();

}

function write_form(datos_json){
    document.getElementById("T1").value = datos_json.temp_1;
    document.getElementById("T2").value = datos_json.temp_2;
    document.getElementById("T3").value = datos_json.temp_3;
}


