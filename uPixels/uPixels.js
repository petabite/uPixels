const MP_WEBREPL_PASSWORD = 'nodemcu'
var brightnessSlider, delaySlider, startingPositionSlider, segmentLengthSlider
var schedulesContainer;

$(document).ready(function () {
  $("#colorpicker").spectrum({
    color: "rgb(0, 255, 155)",
    preferredFormat: 'rgb',
    showButtons: false,
    showInput: true
  });
  $("#second-colorpicker").spectrum({
    color: "rgb(0, 171, 255)",
    preferredFormat: 'rgb',
    showButtons: false,
    showInput: true,
    containerClassName: 'second-colorpicker',
    change: function (color) {
      console.log($(this).spectrum('get').toRgb());
    }
  });

  $('.color-buttons').children().each(function () {
    color_array = $(this).data('color')
    $(this).css('background-color', 'rgb(' + color_array[0] + ',' + color_array[1] + ',' + color_array[2] + ')')
    $(this).click(function () {
      color_array = $(this).data('color')
      color = {
        'r': Math.round(color_array[0] * getBrightness()),
        'g': Math.round(color_array[1] * getBrightness()),
        'b': Math.round(color_array[2] * getBrightness())
      }
      setStrip(color)
    })
  })

  delaySlider = document.getElementById('delay-slider');
  noUiSlider.create(delaySlider, {
    start: 10,
    step: 1,
    behavior: 'drag-tap',
    range: {
      'min': 10,
      'max': 1000
    },
    format: wNumb({
      decimals: 0
    })
  });

  delaySlider.noUiSlider.on('update', function (delay) {
    $('#delay-label').text(delay);
  })

  brightnessSlider = document.getElementById('brightness-slider');
  noUiSlider.create(brightnessSlider, {
    start: 100,
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

  $('#u-logo').on('click touchstart', function () {
    location.reload()
  })

  // Init Schedules UI

  schedules = JSON.parse($("#schedules-data").text())
  schedulesContainer = $('#schedules');
  scheduleTemplate = $('#schedule-template');
  schedules.forEach(({time, action, params}, index) => {
    schedule = scheduleTemplate.clone(true)
    schedule.find('#name').text(`Schedule ${index + 1}`);
    schedule.find('#time-input').val(secondsToTimeString(time));
    schedule.find('#action-input').val(action);
    schedule.find('#params-input').val(JSON.stringify(params));
    schedule.appendTo(schedulesContainer)
    schedule.removeAttr('id')
    schedule.addClass('schedule');
    schedule.show();
  });

  addScheduleBtn = $('#add-schedule-btn');
  addScheduleBtn.on('click', function() {
    schedule = scheduleTemplate.clone(true)
    schedule.find('#name').text(`Schedule ${schedulesContainer.children().length }`);
    schedule.appendTo(schedulesContainer)
    schedule.removeAttr('id')
    schedule.addClass('schedule');
    schedule.show();
  })

  schedulesContainer.on('click', '#delete-btn', function() {
    $(this).closest('.schedule').remove();
  });

  saveSettingsBtn = $('#save-settings-btn');
  saveSettingsBtn.on('click', saveSettings);

  M.AutoInit();
  M.updateTextFields();
  $('.tabs').tabs({
    'swipeable': true
  });
});

// UI Helpers

const SEC_IN_HOUR = 3600;
const SEC_IN_MIN = 60;

function secondsToTimeString(seconds) {
  hours = Math.floor(seconds / SEC_IN_HOUR);
  minutes = Math.floor((seconds % SEC_IN_HOUR) / SEC_IN_MIN);
  hours = hours < 10 ? '0' + hours : hours;
  minutes = minutes < 10 ? '0' + minutes : minutes;
  return `${hours}:${minutes}`;
}

function timeStringToSeconds(timeString) {
  const [hours, minutes] = timeString.split(':').map(Number);
  return (hours * SEC_IN_HOUR) + (minutes * SEC_IN_MIN);
}

function saveSettings() {
  schedulesList = schedulesContainer.find('.schedule').map(function() {
      time = $(this).find('#time-input').val();
      action = $(this).find('#action-input').val();
      params = $(this).find('#params-input').val();
      return {
        time: timeStringToSeconds(time),
        action,
        params: JSON.parse(params)
      }
    }
  ).toArray();
  updateSchedules(schedulesList)
}

function changeVal(element, val) {
  $(element).val(+$(element).val() + val);
}

function togglePickers() {
  if ($("#random-color-checkbox").prop('checked')) {
    $("#colorpicker").spectrum("disable");
    $("#second-colorpicker").spectrum("disable");
    document.getElementById('brightness-slider').setAttribute('disabled', true);
  } else {
    $("#colorpicker").spectrum("enable");
    $("#second-colorpicker").spectrum("enable");
    document.getElementById('brightness-slider').removeAttribute('disabled');
  }
}

function toggleDelaySlider() {
  if ($("#default-delay-checkbox").prop('checked')) {
    document.getElementById('delay-slider').setAttribute('disabled', true);
  } else {
    document.getElementById('delay-slider').removeAttribute('disabled');
  }
}


function getFirstColor() {
  return $("#colorpicker").spectrum("get").toRgb();
}

function getBrightness() {
  return document.getElementById('brightness-slider').noUiSlider.get() / 100;
}

function getColorSelection() {
  brightness = getBrightness()
  if ($('#random-color-checkbox').is(":checked")) {
    return null
  } else {
    color = getFirstColor()
  }
  return {
    'r': Math.round(color['r'] * brightness),
    'g': Math.round(color['g'] * brightness),
    'b': Math.round(color['b'] * brightness)
  }
}

function getDelaySelection() {
  if ($('#default-delay-checkbox').is(":checked")) {
    return undefined
  } else {
    return Number(document.getElementById('delay-slider').noUiSlider.get())
  }
}

// API Helpers

function execute(action, params = {}) {
  var xhr = new XMLHttpRequest();
  xhr.open("POST", '/execute', true);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.send(JSON.stringify({
    'action': action,
    'params': params
  }));
}

function reset() {
  ws = new WebSocket('ws://' + '192.168.200.161' + ':8266')
  ws.addEventListener('open', function () {
    ws.send(MP_WEBREPL_PASSWORD + '\r')
    ws.send('')
    ws.send('import machine;machine.reset()\r')
  })
}

function updateSchedules(schedules) {
  var xhr = new XMLHttpRequest();
  xhr.open("POST", '/schedules', true);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.send(JSON.stringify(schedules));
}

// Animation Functions

function rainbow() {
  execute('rainbow', {
    'ms': getDelaySelection(),
    'iterations': Number($('.rainbow .iterations').val())
  })
}

function rainbowChase() {
  execute('rainbowChase', {
    'ms': getDelaySelection(),
  })
}

function bounce() {
  execute('bounce', {
    'ms': getDelaySelection(),
    'color': getColorSelection()
  })
}

function sparkle() {
  execute('sparkle', {
    'ms': getDelaySelection(),
    'color': getColorSelection()
  })
}

function wipe() {
  execute('wipe', {
    'ms': getDelaySelection(),
    'color': getColorSelection()
  })
}

function chase() {
  if ($('.chase #left').is(":checked")) {
    direction = 'left'
  } else {
    direction = 'right'
  }
  execute('chase', {
    'ms': getDelaySelection(),
    'color': getColorSelection(),
    'direction': direction
  })
}

function rgbFade() {
  execute('rgbFade', {
    'ms': getDelaySelection()
  })
}

function altColors() {
  if ($('#random-color-checkbox').is(":checked")) {
    secondColor = false
  } else {
    secondColor = $("#second-colorpicker").spectrum("get").toRgb()
  }
  execute('altColors', {
    'ms': getDelaySelection(),
    'firstColor': getColorSelection(),
    'secondColor': secondColor
  })
}

function randomFill() {
  execute('randomFill', {
    'ms': getDelaySelection(),
    'color': getColorSelection()
  })
}

function fillFromMiddle() {
  execute('fillFromMiddle', {
    'ms': getDelaySelection(),
    'color': getColorSelection()
  })
}

function fillFromSides() {
  execute('fillFromSides', {
    'ms': getDelaySelection(),
    'color': getColorSelection()
  })
}

function fillStrip() {
  execute('fillStrip', {
    'ms': getDelaySelection(),
    'color': getColorSelection()
  })
}

function christmas() {
  execute('altColors', {
    'ms': 300,
    'firstColor': {
      'r': 0,
      'g': 255,
      'b': 0
    },
    'secondColor': {
      'r': 255,
      'g': 13,
      'b': 13
    }
  })
}

function setStrip(color) {
  execute('setStrip', {
    "color": color
  })
}

function clearStrip() {
  execute('clear')
}
