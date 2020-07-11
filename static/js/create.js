$(function() {
    $('#btnCreate').click(function() {
 
        $.ajax({
            url: '/create',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});