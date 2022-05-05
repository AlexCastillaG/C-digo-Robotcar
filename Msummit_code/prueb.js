var secano = Secano.getNumber()
var libre = Libre.getNumber()
var invernadero = Invernadero.getNumber()
var regadio = Regadio.getNumber()

var max =  secano
var label = "Secano"



if(max>libre){
    label = "Aire Libre"
    max=libre
}else if (max>invernadero){
    max = invernadero
    label = "Invernadero"
}else if (max>regadio){
    max=regadio
    label = "Regadio"
}


Produccion_maxima.setValue(Math.max(regadio,invernadero,libre,secano));

var max_label = Cultivo.Clone();
max_label.setValue(label);
newRow.addValue(max_label);