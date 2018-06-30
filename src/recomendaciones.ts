interface GrupoAlimento{
    pk: number,
    nombre: string, 
    porcion?: number,
    porción?: number,
    alimentos?: Array<Alimento>
}

interface Alimento {
    pk: number,
    nombre: string,
    kcal: number, 
}

interface Comida {
    nombre: string, 
    horario_1: any,
    horario_2?: any, 
    alimentos_porcion?: Array<[Alimento, number]>,
}

class Recomendacion {
    pk: number;
    paciente: number;
    grupos_permitidos: Array<GrupoAlimento>;
    grupos_permitidos_aux?: Array<GrupoAlimento>;
    total_kcal: number;
    observacion: string;
    comidas: Array<Comida> = [];
    /**
     * 
     * @param pk Constructor de recomendacion
     * @param paciente Opcional
     * @param observacion 
     * @param comidas 
     */
    constructor(pk?: number, paciente?:number, observacion?: string, comidas?: Comida[]) {
        this.pk = pk;
        this.paciente = paciente;
        if (observacion){
            this.observacion = observacion;
        }
        if (comidas){
            this.comidas = comidas;
        }
    }
    /**
     * Agrega una comida al arreglo de comidas
     * @param c Objeto comida a agregar
     */
    agregarComida (c: Comida) {
        this.comidas.push(c)
    }
    /**
     * Devuelve la comida que coincida con el nombre exacto 
     * @param nombre String  
     */
    getComidaByName(nombre: string){
        return this.comidas.filter(e => e.nombre==nombre)[0]
    }
    /**
     * Devuelve el grupo de alimentos de la recomendación según la PK.
     * @param pk pk de un grupo de alimentos
     */
    getGrupoPermitidoById(pk: number){
        return this.grupos_permitidos_aux.filter(e => e.pk == pk)[0]
    }
    /**
     * Devuelve un alimento en un determinado grupo de alimentos, según ID.
     * @param pk PK  del alimento
     * @param grupo Grupo donde buscar
     */
    getAlimentoById(pk: number, grupo: GrupoAlimento){  
        return grupo.alimentos.filter(e => e.pk == pk)[0]
    }

    restarPorcion(grupo: GrupoAlimento, porcion: number){
        this.grupos_permitidos_aux.filter(e => e==grupo)[0].porción = this.grupos_permitidos_aux.filter(e => e==grupo)[0].porción - porcion
    }

    addAlimento(a: Alimento){
    
    }

}


/**
 * Crea un objeto grupo de alimento, se utiliza cuando se captura la data 
 * (Aunque ya viene en este formato, sacamos los campos inncesarios para este modelo.)
 * @param grupo Interfaz de objeto GrupoAlimento
 */
let crearGrupoAlimento = (c: GrupoAlimento): {pk: number, nombre: string, porcion?: number, porción?: number} => {
    let nuevoGrupo = {pk: c.pk, nombre: c.nombre, porcion: 0, porción: 0}
    if (c.porcion) {
        nuevoGrupo.porcion = c.porcion
    }
    if (c.porción) {
        nuevoGrupo.porción = c.porción
    }
    return nuevoGrupo;
}
/**
 * Crea un objeto alimento en base a una Interfaz. Para capturar la data 
 * @param a Interfaz de alimento
 */
let crearAlimento = (a: Alimento) => {
    let nuevoAlimento = {pk: a.pk, nombre: a.nombre, kcal: a.kcal}
    return nuevoAlimento
}
/**
 * Crea un objeto comida, que contiene todos los alimentos dentro de un rango de horarios.
 * @param c Interfaz de objeto Comida.
 */
let crearComida = (c: Comida) => {
    let nuevaComida = {'nombre': c.nombre, 'horario_1': c.horario_1}
    return nuevaComida
}
/**
 * Función que agrega un alimento a una comida, pregunta primero siesiste el array, si no lo crea.
 * @param c Comida a la cual se le agrega el alimento
 * @param a Alimento 
 */
let agregarAlimentoAComida = (c: Comida, a: Alimento, porcion: number) => {
    if(c.alimentos_porcion) {
        c.alimentos_porcion.push([a,porcion])
    }else{
        c.alimentos_porcion = [[a, porcion]]
    }
}
/**
 * Funcion que agrega una comida al arreglode comidas de la recomendacion
 * @param r recomendación a la cual agregamos una comida, preguntamos primero si ya tiene un arry de comidas.
 * @param c objeto comida
 */
let agregarComidaARecomendacion = (r: Recomendacion, c: Comida) => {
    if (r.comidas){
        r.comidas.push(c)
    }else{
        r.comidas = [c]
    }
}



/**
 * ! Función para capturar los grupos de alimentos desde Django
 */
const url_alimentos_json = `/superadmin/grupo-alimentos-json`
const capturarGrupoAlimentos = () => {
    let grupos_de_alimentos: Array<GrupoAlimento> = [];

    $.getJSON(url_alimentos_json, (data)=> {
        let grupos_alimentos = JSON.parse(data)
        grupos_alimentos.forEach((e: GrupoAlimento) => {
            let grupo = crearGrupoAlimento(e)
            grupos_de_alimentos.push(grupo)
        });
    })
    return grupos_de_alimentos
}

let crearRecomendacion = (pk:number, pk_paciente: number) =>{
    return new Recomendacion(pk, pk_paciente)
}





export {
    capturarGrupoAlimentos,
    Recomendacion,
    crearGrupoAlimento,
    GrupoAlimento,
    Alimento,
    crearComida,
    Comida,
    agregarAlimentoAComida
}