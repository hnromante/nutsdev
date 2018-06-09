/**
*!Funcion para capturar la data de grupo de alimento
ESTESCRIPT ESTA SIENDO LLAMADO DESDE CALCULADORA APCIENTE EN LA APLICACIONE DE NUTRICIONISTA
*/
$.getJSON(url_alimentos_json, function(data){
    let lista_grupo_alimentos = []
    lista_grupo_alimentos = JSON.parse(data)
    lista_grupo_alimentos.forEach(function(element){
        $(".calculadora-body").append(`
        <tr class="grey-text center" 
        data-nombre="${element.nombre}" 
        data-kcal="${element.kcal_prom}"
        data-cho="${element.cho_prom}"
        data-pro="${element.pro_prom}"
        data-lip="${element.lip_prom}">
            <td >${element.nombre} - (Kcal: ${element.kcal_prom}, Cho: ${element.cho_prom},   Proteínas: ${element.pro_prom}, Lipidos: ${element.lip_prom}) </td>
            <td class="porcion" style="width:100px;"><input type="number" value=0 min=0 max=10></td>
            <td class="kcal">0</td>
            <td class="cho">0</td>
            <td class="pro">0</td>
            <td class="lip">0</td>
        </tr>`)
    })
})

/**
*!Función JQuery que captura la porcion y los atributos
*/
$(document).on("keyup change", ".calculadora-body input", function(){
    $(".calculadora-body").children('tr').each((i, e) => { 
        console.log(this)
        const porcion = $(e).find("input").val()
        const kcal = $(e).data("kcal")
        const cho = $(e).data("cho")
        const pro = $(e).data("pro")
        const lip = $(e).data("lip")
        atributos = [kcal, cho, pro, lip]
        a_x_p = multiplicarAtributos(porcion, atributos)
        //a_x_p = Atributos kcal,cho,pro,lip POR porcion.
        $(e).find(".kcal").html(a_x_p[0])
        $(e).find(".cho").html(a_x_p[1])
        $(e).find(".pro").html(a_x_p[2])
        $(e).find(".lip").html(a_x_p[3])    

    })
    //Asignar subtotal
    const porciones = []
    $(".porcion").each((i, e)=> { porciones.push($(e).find("input").val() )})
    porciones_num = porciones.map(e => Number(e))

    const kcals = []
    $(".kcal").each((i,e) => { kcals.push($(e).html()) })
    kcals_num = kcals.map(e => Number(e))

    const chos = []
    $(".cho").each((i,e) => { chos.push($(e).html()) })
    chos_num = chos.map(e => Number(e))

    const prots = []
    $(".pro").each((i,e) => { prots.push($(e).html()) })
    prots_num = prots.map(e => Number(e))

    const lips = []
    $(".lip").each((i,e) => { lips.push($(e).html()) })
    lips_num = lips.map(e => Number(e))

    sub_porciones = porciones_num.reduce((suma, val) => suma + val)
    sub_kcals = kcals_num.reduce((suma, val) => suma + val)
    sub_cho = chos_num.reduce((suma, val) => suma + val)
    sub_pro = prots_num.reduce((suma, val) => suma + val)
    sub_lip = lips_num.reduce((suma, val) => suma + val)

    $(".sub-porcion").html(sub_porciones)
    $(".sub-kcal").html(sub_kcals)
    $(".sub-cho").html(sub_cho)
    $(".sub-pro").html(sub_pro)
    $(".sub-lip").html(sub_lip)
    actualizarAdecuacion()
    
})
$(document).ready(function(){ 
    
    total_kcal = $(".total-kcal").html()
    $(".kcal-cho").html(total_kcal)
    $(".gr-cho").html(total_kcal)
    
    $(".kcal-pro").html(total_kcal)
    $(".gr-pro").html(total_kcal)

    $(".kcal-lip").html(total_kcal)
    $(".gr-lip").html(total_kcal)

})

/**
* ! Captura cuando se ahc click en un 'kcal-fis'. Para asignarselo al 'Kcal según actividad fisica'
**/
$(".kcal-fis").each((i,e) => {
    $(e).on("click", function(){
        $(".kcal-fis").removeClass("green")
        $(e).addClass("green")
        let val = $(e).html()
        $("#kcal-a-utilizar").html(val)
        $("#kcal-a-utilizar").addClass("green")

        let peso = $("#peso-a-utilizar").val()
        let kcal = Number($("#kcal-a-utilizar").html())
        $(".total-kcal").html(peso*kcal)
        actualizarAdecuacion()
    })
})  
$("#peso-a-utilizar").on("keyup", (e) => {
    let peso = e.target.value
    let kcal = Number($("#kcal-a-utilizar").html())
    $(".total-kcal").html(peso*kcal)
    actualizarAdecuacion()
    actualizarVCT()
})


 /**
*!Función para calcular el valor lateral de los campos
*/
let multiplicarAtributos = (porcion, arrayAtributos) => {
    return arrayAtributos.map(e => e*porcion);
}

$("#total-kcal").bind("DOMSubtreeModified",function(){
    actualizarVCT()
});

$(".porc-cho, .porc-pro, .porc-lip").on("keyup change", (e) => {
    actualizarVCT()
    actualizarAdecuacion()
})

let actualizarVCT = () => {
    let total_kcal = $("#total-kcal").html()

    let kcal_cho = (total_kcal * $(".porc-cho").val()) / 100
    $(".kcal-cho").html(kcal_cho)
    $(".gr-cho").html((kcal_cho/4).toFixed(2))

    let kcal_pro = (total_kcal * $(".porc-pro").val()) / 100
    $(".kcal-pro").html(kcal_pro)
    $(".gr-pro").html((kcal_pro/4).toFixed(2))

    let kcal_lip = (total_kcal * $(".porc-lip").val()) / 100
    $(".kcal-lip").html(kcal_lip)
    $(".gr-lip").html((kcal_lip/9).toFixed(2))

    $("#vct-porc").html(Number($(".porc-cho").val()) + Number($(".porc-pro").val()) + Number($(".porc-lip").val()))
    vct_porc = Number($("#vct-porc").html())
    if (vct_porc>100){
        $("#vct-porc").addClass("red-text")
        alert("VCT no puede ser mayor a 100%")
    }else{
        $("#vct-porc").removeClass("red-text")
    }
}
let actualizarAdecuacion = () => {
    total_kcal = Number($("#total-kcal").html())
    sub_kcal = Number($(".sub-kcal").html())
    porc_ade = ((sub_kcal*100)/total_kcal).toFixed(2)
    $(".porc_ade_kcal").html(`${porc_ade} % adecuación`)

    total_cho = Number($(".kcal-cho").html())
    sub_cho = Number($(".sub-cho").html())
    porc_ade = ((sub_cho*100)/total_cho).toFixed(2)
    $(".porc_ade_cho").html(`${porc_ade} % adecuación`)

    total_pro = Number($(".kcal-pro").html())
    sub_pro = Number($(".sub-pro").html())
    porc_ade = ((sub_pro*100)/total_pro).toFixed(2)
    $(".porc_ade_pro").html(`${porc_ade} % adecuación`)

    total_lip = Number($(".kcal-lip").html())
    sub_lip = Number($(".sub-lip").html())
    porc_ade = ((sub_lip*100)/total_lip).toFixed(2)
    $(".porc_ade_lip").html(`${porc_ade} % adecuación`)
}
