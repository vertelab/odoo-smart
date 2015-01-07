/*
 * SCRIPTS FOR CLIENTS VIEW
 */

$(document).ready(function() {
  
    /* CLIENT TYPE */
    $(".client-type .radio.inline").click(function() {
      $("input[value=company]:checked").is(function() {
         $("#client-edit-company").toggle();
         $("#client-edit-individual").toggle();
      });
    });
    
    /* ADDRESS */
    $('label .checkbox_billing_address').click(function(){
        $(".billing-infos").toggle(200);
    });
    
    /* LOCATION */
    $(".country #select-country").change(function(e){
      if($(this).val() == "current") {
        $(".registration").show(200);
        $(".vat").show(200);
        $(".vat .add-on").text("SE");
      }else if ($(this).val().substring(0, 2) == "eu") {
        $(".vat").show(200);
        var code = $(this).val().split("-");
        code = code[1].toUpperCase();
        $(".vat .add-on").text(code);
        $(".registration").hide(200);
      } else { // is an url
        $(".registration").hide(200);
        $(".vat").hide(200);  
      }
    });
    
    
    $("#button-new-contact").click(function(e){
      var data = $(this).data("href")
      
      if(data.indexOf("panelsheet") > -1){ 
        // is looking for a panel
        var url = $(this).data().split(" ");
        var geturl = url[0];
        var element = url[1];
        loadPanel(geturl, element, $(this).closest(".panelsheet"));
      }
    });
});
