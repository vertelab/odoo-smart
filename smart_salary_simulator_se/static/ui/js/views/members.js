/*
 * GLOBAL SCRIPTS
 */

$(document).ready(function() {

  
  /* SIMULATE PANELSTACK IF DATA-PANEL
     At end, replace with app's own events handler */
 
  $("*[data-show-panel]").bind("click", function(e){
    var value = $(this).data("show-panel");
    var url = value.split(" ");
    var geturl = url[0];
    var element = url[1];
    loadPanel(geturl, element, $(this).closest(".panelsheet"));
  });  
});
