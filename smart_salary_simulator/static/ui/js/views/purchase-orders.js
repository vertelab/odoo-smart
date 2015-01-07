/*
 * SCRIPTS FOR PURCHASE ORDERS VIEW
 */

$(document).ready(function() {
  
  /* DUPLICATES ORDER ROW */
  $('#new-item').click(function(){
    $(".order-row-item:first").clone().insertAfter( $("." + "order-row-item:last" ) );
    return false;
  });
  
  // Bind events to load child panels
  
  $("#select-client").change(function(e){
    var value = $(this).val();
    
    if(value == "company" || value == "public"){
      $(".contact").show(200);
    }else if (value == "individual") {
      $(".contact").hide(200);
    }else if(value.indexOf("panelsheet") > -1){ 
      // is looking for a panel
      var url = $(this).val().split(" ");
      var geturl = url[0];
      var element = url[1];
      console.log("test");
      loadPanel(geturl, element, $(this).closest(".panelsheet"));
    }
  });
  
  $("#select-contact").change(function(e){
    var value = $(this).val();
    if(value.indexOf("panelsheet") > -1){ 
      // is looking for a panel
      var url = $(this).val().split(" ");
      var geturl = url[0];
      var element = url[1];
      loadPanel(geturl, element, $(this).closest(".panelsheet"));
    }
  });
  
  $("#select-project").change(function(e){
    var value = $(this).val();
    
    if(value.indexOf("panelsheet") > -1){ 
      // is looking for a panel
      var url = $(this).val().split(" ");
      var geturl = url[0];
      var element = url[1];
      loadPanel(geturl, element, $(this).closest(".panelsheet"));
    }
  });
  
});
