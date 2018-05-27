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
            <td >${element.nombre}</td>
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
$(document).ready(function(){ 
    $("input").on("keyup change", ()=>{
        $(".calculadora-body").children('tr').each((i, e) => { 
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
        $(".kcal").each((i,e) => { chos.push($(e).html()) })
        chos_num = chos.map(e => Number(e))

        const prots = []
        $(".kcal").each((i,e) => { prots.push($(e).html()) })
        prots_num = prots.map(e => Number(e))

        const lips = []
        $(".kcal").each((i,e) => { lips.push($(e).html()) })
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
        
    })
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
    })
})  
$("#peso-a-utilizar").on("keyup", (e) => {
    let peso = e.target.value
    let kcal = Number($("#kcal-a-utilizar").html())
    $(".total-kcal").html(peso*kcal)
})


 /**
*!Función para calcular el valor lateral de los campos
*/
let multiplicarAtributos = (porcion, arrayAtributos) => {
    return arrayAtributos.map(e => e*porcion);
}