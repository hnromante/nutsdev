
import { capturarGrupoAlimentos, Recomendacion, crearGrupoAlimento, GrupoAlimento, Alimento, crearComida, Comida, agregarAlimentoAComida} from "./recomendaciones";

let initRecomendacion = (pkPaciente: number) => {
    const url_data_paciente = `/nutricionista/recomendaciones/${pkPaciente}/`;
    $.getJSON(url_data_paciente, (data) => {
        if(data['tiene_recomendacion']){
            $('#iniciar_recomendacion').addClass('hide')
            let recomendacion = new Recomendacion(data['pk'], data['paciente']);
            if (data['grupos_permitidos'] == null){
                alert('Debe primero llenar la calculadora piramidal de forma correcta.')
                window.location.replace(`/nutricionista/mis-pacientes/${pkPaciente}/calculadora`)
            }else{
                recomendacion.grupos_permitidos = data['grupos_permitidos']
                recomendacion.grupos_permitidos_aux = data['grupos_permitidos']
                recomendacion.total_kcal = data['total_kcal']
                
                console.log('data[\'total_kcal\']', data['total_kcal'])
                console.log('recomendacion.total_kcal', recomendacion.total_kcal)
                renderPorciones($('#select_porciones'), recomendacion.grupos_permitidos_aux[0])
                console.log(recomendacion.grupos_permitidos_aux)
                renderComboGrupos($('#select_grupos_permitidos'), recomendacion)
                renderComboAlimentos($('#select_grupos_permitidos'), $('#select_alimentos_permitidos'), recomendacion)
                agregarComidaListener($('#btn_agregar_comida'), recomendacion)
                agregarAlimentoListener($('#btn_agregar_alimento_comida'), recomendacion)
                renderMinutaDiaria($('#tabla_minuta'), recomendacion)
            }
            
        }else{
            $('#recomendacion_nutricional').addClass('hide')    
            $('#btn_iniciar_recomendacion').on('click', function() {
                $.get(`/nutricionista/recomendaciones/${pkPaciente}/crear`, (data) => {
                    location.reload()
                })
            })
        }
    })
}


function renderComboComidas(select: JQuery, arreglo: Array<Comida>){
    select.empty()
    arreglo.forEach(e => {
        select.append($('<option>', {
            text: e.nombre
        }))
    })
}
function renderComboGrupos(select: JQuery, recomendacion: Recomendacion){
    select.empty()
    recomendacion.grupos_permitidos_aux.forEach(e => {
        if (e.porcion) {
            select.append($('<option>', { 
                value: e.pk,
                text : `${e.nombre} - (${e.porcion})` 
            }))  
        }else{
            select.append($('<option>', { 
                value: e.pk,
                text : `${e.nombre} - (${e.porción})` 
            }))  
        }
    });
    select.on('change', function(){
        let grupo = recomendacion.getGrupoPermitidoById(Number(select.val()))
        renderPorciones($('#select_porciones'), grupo)
    })
}
/**
 * 
 * @param select_listener Select que escucha cuando se cambia la opcion seleccionada
 * @param select_taget Select que carga dinamicamente sgun el listener
 * @param recomendacion Recomendación donde se va a buscar el grupo de alimentos según el PK.
 */
function renderComboAlimentos(select_listener: JQuery, select_taget: JQuery,  recomendacion: Recomendacion){
    $(document).ready(() => renderComboAlimentosGrupoSelected(select_taget, recomendacion.grupos_permitidos_aux[0]))
    select_listener.on('change', function(e){
        const pk_grupo = Number(select_listener.val())
        let grupo = recomendacion.getGrupoPermitidoById(pk_grupo)
        renderComboAlimentosGrupoSelected(select_taget, grupo)
    })
}
/**
 * Funcion que carga de forma dinámica los alimentos según el grupo de alimentos seleccioando.
 * @param select Select input que va a renderear los alimentos del grupo
 * @param grupo grupo que contiene los alimentos a renderear
 */
function renderComboAlimentosGrupoSelected(select: JQuery, grupo: GrupoAlimento){
    select.empty()
    grupo.alimentos.forEach(e => {
        select.append($('<option>', {
            value: e.pk,
            text: `${e.nombre} - ${e.kcal} kcal`
        }))
    })
}

function renderPorciones(select: JQuery, grupo: GrupoAlimento){
    select.empty()
    let porcion: number;
    let porciones: Array<number> = []
    if (grupo.porción){
        porcion = grupo.porción
    }else{
        porcion = grupo.porcion
    }
    
    for (let i = 1; i <= porcion; i++) {
        porciones.push(i)
    }

    porciones.forEach(e =>{
        select.append($('<option>', {
            value: e,
            text: e
        }))
    })

}

function agregarComidaListener (elemento: JQuery, recomendacion: Recomendacion){
    elemento.on('click', (e) => {
        const nombre = String($('#input_comida').val())
        const horario = $('#input_horario').val()
        if  (nombre.trim() == ''){
            alert('El nombre no puede quedar vacio')
            return false;
        }
        if  (horario == 'horario'){
            alert('Debe seleccionar una hora')
            return false;
        }
        const comida = crearComida({'nombre':nombre, 'horario_1': horario})
        recomendacion.agregarComida(comida)
        renderComboComidas($('#select_comidas'), recomendacion.comidas)
        $('#msg_add_alimento').html('')
        $('#msg_add_alimento').append(`<p class="green-text">Comida ${comida.nombre} agregada</p>`)
        console.log('recomendacion.comidas  ',recomendacion.comidas)
        renderMinutaDiaria($('#tabla_minuta'), recomendacion)
    })
}
function agregarAlimentoListener(elemento: JQuery, recomendacion: Recomendacion ) {
    elemento.on('click', (e) => {
        const pk_grupo = Number($('#select_grupos_permitidos').val())
        const pk_alimento = Number($('#select_alimentos_permitidos').val())
        const porcion = Number($('#select_porciones').val())
        const nom_comida = $('#select_comidas').find(":selected").text();
        let grupo = recomendacion.getGrupoPermitidoById(pk_grupo)
        let comida = recomendacion.getComidaByName(nom_comida)
        let alimento = recomendacion.getAlimentoById(pk_alimento, grupo)
        if(validateAgregarAlimento(pk_grupo, pk_alimento, porcion)){
            if (comida){
                if(comida.alimentos_porcion){
                    //IF ALIMENTO IN ARRAY, AÑADE UNA PORCION EN LUGAR DE OTRO ELEMENTO EN LA LISTA
                    if (recomendacion.alimentoEnMinuta(alimento)){
                        comida.alimentos_porcion.push([alimento,porcion])
                    }else{

                    }
                    

                }else{
                    comida.alimentos_porcion = [[alimento,porcion]]

                }
                recomendacion.restarPorcion(grupo, porcion)
                renderComboGrupos($('#select_grupos_permitidos'), recomendacion)
                renderPorciones($('#select_porciones'), grupo)
                renderMinutaDiaria($('#tabla_minuta'), recomendacion)
            }else{
                alert('Seleccione una comida')
            }
    
        }
        
    })
}

function renderMinutaDiaria(tabla:JQuery, recomendacion: Recomendacion){
    tabla.empty()
    recomendacion.comidas.forEach(c => {
        let alimentos = c.alimentos_porcion
        let html_alimentos = '';
        let suma_kcal = 0;
        let porc = 0;
        const kcal_total = recomendacion.total_kcal
        
        // let cuota_diaria = 0;
        // let 
        if (c.alimentos_porcion) {
            c.alimentos_porcion.forEach(tupla => {
                suma_kcal += tupla[0].kcal*tupla[1]
                html_alimentos+= `${tupla[0].nombre} (${tupla[1]}) `
            });

        }
        if (suma_kcal != 0){
            porc = (kcal_total/suma_kcal)*100
        }
        tabla.append($("<tr>")
            .append($('<td>', {text:c.nombre}))
            .append($('<td>', {text:html_alimentos}))
            .append($('<td>', {text:suma_kcal}))
            .append($('<td>', {text: porc}))
    )  
    });
}
function validateAgregarAlimento(pk_grupo: number, pk_alimento: number, porcion: number){
    if (!pk_grupo){
        alert('Seleccione un grupo')
        return false
    }
    if (!pk_alimento){
        alert('Selecciona un alimento')
        return false
    }
    if (!porcion){
        alert('La porción debe ser mayor a 0')
        return false
    }
    return true
}

if (Number($('#pk_paciente').val()) != 0) {
    initRecomendacion(Number($('#pk_paciente').val()))    
}else{
    $('#recomendacion_nutricional').html(`No hay datos para llenar la recomendacion`)
}



/**
 * Inicializa la aplicación de recomendación para el paciente.
 * @param pkPaciente 
 */
