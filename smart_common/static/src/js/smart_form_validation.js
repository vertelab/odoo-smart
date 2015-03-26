var decSign = ",";

function validateFloatField(element){
    if(isNaN(convertDecSign(element.value))){
	element.setCustomValidity('Please enter a number.');
    }
    else{
	element.setCustomValidity('');
    }
};

function convertDecSign(str){
    return String(str).replace(decSign, ".");
};

function convertInputFields(form){
    if (! form.checkValidity()) {
	return false;
    }
    var fields = form.getElementsByClassName("smart-input-float");
    var i = 0;
    for (i = 0; i < fields.length; i++) {
	fields[i].value = convertDecSign(fields[i].value);
    }
    return true;
};

document.addEventListener("DOMContentLoaded", function() {
    console.log("Content loaded!")
    var fields = document.getElementsByClassName("smart-input-float");
    var i = 0;
    for (i = 0; i < fields.length; i++) {
	fields[i].value = String(fields[i].value).replace(".", decSign);
	fields[i].setAttribute("onchange", "validateFloatField(this)");
    };
    fields = document.getElementsByClassName("smart-input-form");
    for (i = 0; i < fields.length; i++) {
	fields[i].setAttribute("onsubmit", "convertInputFields(this)");
    };
});
