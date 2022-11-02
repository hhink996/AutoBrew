window.onload = funciton () {
    var url, i, jqxhr;

    url = document.URL + 'inputs/';
    jqxhr = $.getJSON(url, function(data) {
        console.log('API responce received');
        $('#data').append('<p>Gryp: ' + data['Angle'] + '\nTempC: ' + data['TempC'] + '\nTempF: ' + data['TempF'] + '</p>');
    });
};