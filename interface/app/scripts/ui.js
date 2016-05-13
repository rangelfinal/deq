$(document)
  .ready(function() {
    $('.ui.toggle.onoff.button')
      .state({ text: { inactive : 'Off', active   : 'On' } });
    $('.ui.toggle.adsorption.button')
        .state({ text: { inactive : 'Adsorption', active   : 'Desorption' } });

    $('.menu .item')
      .tab();
  });
