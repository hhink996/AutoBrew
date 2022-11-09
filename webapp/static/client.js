window.onload = function () {
    var url, i, jqxhr;

    url = document.URL;
    jqxhr = $.getJSON(url, function(data) {
        console.log('API responce received');
        $('#input').append('<p>Gryp: ' + data['Angle'] + '\nTempC: ' + data['TempC'] + '\nTempF: ' + data['TempF'] + '</p>');
    });
};
