"use strict";
exports.__esModule = true;
var url_alimentos_json = "/superadmin/grupo-alimentos-json";
var capturarGrupoAlimentos = function () {
    $.getJSON(url_alimentos_json, function (data) {
        console.log(data);
    });
};
exports.capturarGrupoAlimentos = capturarGrupoAlimentos;
var GrupoAlimento = (function () {
    function GrupoAlimento(pk, nombre, porciones) {
    }
    return GrupoAlimento;
}());
var Alimento = (function () {
    function Alimento(nombre, kcal, grupoAlimento) {
    }
    return Alimento;
}());
var Comida = (function () {
    function Comida(nombre, horario, alimentos) {
    }
    return Comida;
}());
var Minuta = (function () {
    function Minuta(paciente, comidas) {
    }
    return Minuta;
}());
