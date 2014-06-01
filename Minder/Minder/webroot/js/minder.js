<!-- hide script from old browsers

$("#new_mind_orig").on("click", '#origin', function(){
  var o_toLoad = $(this).attr("href")+'#origin';
  var o_url = ($(this).attr('href'));
  var o_input = $('#origintext');
  var o_param = getURLParameter(o_url, 'root');
  var o_value = urldecode(o_param);

  $("#originfolder").load(o_toLoad, function() {
    if (o_value != 'null'){
      o_input.val(o_value);
    }
  });
  return false;
});

$("#new_mind_dest").on("click", "#origin", function(){
  var toLoad = $(this).attr("href")+'#origin';
  var url = ($(this).attr('href'));
  var input = $('#destinationtext');
  var param = getURLParameter(url, 'root');
  var value = urldecode(param);

  $("#destinationfolder").load(toLoad, function() {
    if (value != 'null'){
      input.val(value);
    }
  });
  return false;
});

function getURLParameter(url, name) {
    return (RegExp(name + '=' + '(.+?)(&|$)').exec(url)||[,null])[1];
}

function urldecode(str) {
   return decodeURIComponent((str+'').replace(/\+/g, '%20'));
}

// end hiding script from old browsers -->