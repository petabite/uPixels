$(document).ready(function(){
  $("#colorpicker").spectrum({
    color: "rgb(0, 255, 155)",
    preferredFormat: 'rgb',
    showButtons: false,
    showInput: true,
    change: function(color) {
      console.log($(this).spectrum('get').toRgb());
    }
  });
  M.AutoInit();
  var slider = document.getElementById('brightness-slider');
  noUiSlider.create(slider, {
   start: 50,
   connect: true,
   step: 1,
   orientation: 'horizontal', // 'horizontal' or 'vertical'
   range: {
     'min': 0,
     'max': 100
   },
   format: wNumb({
     decimals: 0
   })
  });
});
