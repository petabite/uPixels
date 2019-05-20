var brightnessSlider, startingPositionSlider, segmentLengthSlider
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
  $("#second-colorpicker").spectrum({
    color: "rgb(0, 171, 255)",
    preferredFormat: 'rgb',
    showButtons: false,
    showInput: true,
    containerClassName: 'second-colorpicker',
    change: function(color) {
      console.log($(this).spectrum('get').toRgb());
    }
  });

  M.AutoInit();
  $('.tabs').tabs({'swipeable':true});

  brightnessSlider = document.getElementById('brightness-slider');
  noUiSlider.create(brightnessSlider, {
   start: 50,
   step: 1,
   behavior: 'drag-tap',
   range: {
     'min': 0,
     'max': 100
   },
   format: wNumb({
     decimals: 0
   })
  });

  brightnessSlider.noUiSlider.on('update', function (brightness) {
    $('#brightness-label').text(brightness);
  })

  startingPositionSlider = document.getElementById('starting-position-slider');
  noUiSlider.create(startingPositionSlider, {
   start: 1,
   step: 1,
   behavior: 'drag-tap',
   range: {
     'min': [0],
     'max': [300]
   },
   format: wNumb({
     decimals: 0
   })
  });

  startingPositionSlider.noUiSlider.on('update', function (position) {
    $('#position-label').text(position);
  })

  // segmentLengthSlider = document.getElementById('segment-length-slider');
  // noUiSlider.create(segmentLengthSlider, {
  //  start: 50,
  //  step: 1,
  //  behavior: 'drag-tap',
  //  range: {
  //    'min': [1],
  //    'max': [300]
  //  },
  //  format: wNumb({
  //    decimals: 0
  //  })
  // });
});
