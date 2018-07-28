$( document ).ready(function() {
    console.log( "ready!" );

    $('#btn_login').click(function() {
        window.location.replace('/login');
    });

    $('#btn_logout').click(function() {
        $.ajax({
            type: 'GET',
            url: '/gdisconnect',
            processData: false,
            contentType: 'application/octet-stream; charset=utf-8',
            success: function(result) {
                if (result == 'successfully_disconnected') {
                    window.location.href = "/";
                } else {
                    console.log('There was an error: ' + result);
                }
            },
            error: function (xhr) {
                console.log('There was an error: ' + xhr.status + ' - ' + xhr.responseText);
                window.location.href = "/";
            }
        });
    });

});