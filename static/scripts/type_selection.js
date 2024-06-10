const CALC = '<option value="no" >Не выбрано</option><option value="plus">Только +</option><option value="minus">Только -</option><option value="addsub">Только + и -</option><option value="muldiv">Только * и /</option>';
const EQUATION = '<option value="no" >Не выбрано</option><option value="squared">Только ax^2+bx+c</option><option value="lin">Только kx+b</option>';

const VAL_TO_PTYPE = ['calc', 'equation', 'inequality']

const VAL_TO_HARD = ['low', 'mid', 'high']

var type = document.getElementById("problem_type");
var hard = document.getElementById("hard_type");
var add = document.getElementById("addition");

type.addEventListener("change", render_additional);

let pairs = document.cookie.split('; ');
var cookies = {};
for (var i=0; i<pairs.length; i++){
var pair = pairs[i].split("=");
cookies[(pair[0]+'').trim()] = unescape(pair.slice(1).join('='));
}
type.value = VAL_TO_PTYPE[cookies["P_TYPE"]];
hard.value = VAL_TO_HARD[cookies["HARDNESS"]];
render_additional();
add.value = cookies["ADDITIONAL"];
function render_additional() {
    if (type.value == "calc") 
    {
        add.innerHTML = CALC;
    }
    else
    {
        // add.innerHTML = EQUATION;
        add.innerHTML = CALC;
    }
}