const CALC = '<option value="no" selected >Не выбрано</option><option value="only +">Только +</option><option value="only -">Только -</option><option value="only *">Только *</option><option value="only /">Только /</option>';
const EQUATION = '<option value="no" selected >Не выбрано</option><option value="only squared">Только ax^2+bx+c</option><option value="only linear">Только kx+b</option>';

var type = document.getElementById("problem_type");
var hard = document.getElementById("hard_type");
var add = document.getElementById("addition");

type.addEventListener("change", render_additional);
render_additional();

function render_additional() {
    if (type.value == "calc") 
    {
        add.innerHTML = CALC;
    }
    else
    {
        add.innerHTML = EQUATION;
    }
}