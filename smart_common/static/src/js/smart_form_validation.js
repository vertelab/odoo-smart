
function init_smart_form_handler(decSign, kSeparator){
    smart_decSign = decSign;
    smart_kSeparator = kSeparator;
    var fields = document.getElementsByClassName("smart-input-float");
    var i = 0;
    for (i = 0; i < fields.length; i++) {
	fields[i].value = String(fields[i].value).replace(".", smart_decSign);
	fields[i].setAttribute("onchange", "validateFloatField(this)");
    };
    fields = document.getElementsByClassName("smart-input-form");
    for (i = 0; i < fields.length; i++) {
	fields[i].setAttribute("onsubmit", "convertInputFields(this)");
    };
};


function validateFloatField(element){
    if(isNaN(convert_decSign(element.value))){
	element.setCustomValidity('Please enter a number.');
    }
    else{
	element.setCustomValidity('');
    }
};

function convert_decSign(str){
    return String(str).replace(smart_decSign, ".");
};

function convertInputFields(form){
    if (! form.checkValidity()) {
	return false;
    }
    var fields = form.getElementsByClassName("smart-input-float");
    var i = 0;
    for (i = 0; i < fields.length; i++) {
	fields[i].value = convert_decSign(fields[i].value);
    }
    return true;
};
