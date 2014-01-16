// Javascript to get waypoints for a movie
function getWaypoints(movie) {
  $.get('/waypoints?title='+movie, function(result) {
    $('#points').val(result);
  });
};