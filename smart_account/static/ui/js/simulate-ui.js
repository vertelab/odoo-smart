/*
 * GLOBAL SCRIPTS
 */

$(document).ready(function() {
  
  /* SIMULATE SUBMIT ON PANELSHEETS */
  
  $(".panelsheet-footer .btn").click(function(e){

    // Some vars
    $this = $(this);
    $container = $this.closest(".panelsheet");

    if($this.data("loading-text")){
      e.preventDefault();
      
      // Lock down the form
      $("input, button, submit, select", $container).prop('disabled', true);
      
      // Simulate delay then submit
      setTimeout(function () {  
        if($this.attr("href")) document.location.href = $this.attr("href");
      }, 500)
    }
    
  });
  
  
  /* SIMULATE LINK ON DATA-HREF
     At end, replace with app's own events handler */
 
  $("*[data-href]").bind("click", function(e){
    document.location = $(this).data("href");
  });
  
  
});
