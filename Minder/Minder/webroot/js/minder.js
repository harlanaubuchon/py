<!-- hide script from old browsers
$("#origin").on("click", function(e){
      e.preventDefault();                      
  $("#originfolder").load($("#origin").attr("href"));
  return false;
});
$("#destination").on("click", function(e){
      e.preventDefault();
  $("#destinationfolder").load($("#destination").attr("href"));
  return false;
});
// end hiding script from old browsers -->
