function searchSpotify(){
  $('#search-container').html("");
  var q = $("#query").val();

  var spotifyAPI = "https://api.spotify.com/v1/search?q="+q+"&type=track&market=DK";
  $.getJSON( spotifyAPI, {
    format: "json"
  }).done(function( data ) {
    console.log(data.tracks.items);
    for (var i = data.tracks.items.length - 1; i >= 0; i--) {
      var item = data.tracks.items[i];
      $('#search-container').append('<div class="video"><img src='+data.tracks.items[i].album.images[0].url+'><div class="info"><h2>'+data.tracks.items[i].name+'</h2><audio controls="" name="media"><source src="'+data.tracks.items[i].preview_url+'"></audio><div class="add-video" data-id="'+data.tracks.items[i].uri+'" onclick="" data-title="'+data.tracks.items[i].name+'">Tilføj til kø</div></div></div>');
    }
    });
}