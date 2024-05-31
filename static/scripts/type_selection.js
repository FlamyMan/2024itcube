var type = document.getElementById("problem_type");
var hard = document.getElementById("hard_type");
var add = document.getElementById("addition");

type.addEventListener("change", render_additional);
render_additional();
function render_additional() {
    if (type.value == "calc") 
    {
        add.innerHTML = '<option value="no">Не выбрано</option><option value="only +">Только +</option><option value="only -">Только -</option><option value="only *">Только *</option><option value="only /">Только /</option>';
    }
    else
    {
        add.innerHTML = '<option value="no">Не выбрано</option><option value="only squared">Только ax^2+bx+c</option><option value="only linear">Только kx+b</option>';
    }
}