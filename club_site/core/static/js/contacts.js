$(function() {
    console.log('start');

    (function () {
        var e = document.getElementById("adress1");
        e.parentNode.removeChild(e);
    })();

    $('#name').focus(function() {
        $('#name').removeClass('error');
    });
    
    $('#message').focus(function() {
        $('#message').removeClass('error');
    });
    
    $('#email').focus(function() {
        $('#email').removeClass('error');
    });

    var bot = false;
    
    $("#submit").click(function(event){
        var form_data = $("#contactform").serializeArray();
        var isFormValid = [true, true, true];
        for (var i = 0; i < form_data.length; i++) {
            if (form_data[i].name === 'name') {
             isFormValid[0] = Boolean(form_data[i].value);
                if (!isFormValid[0]) {
                    $('#name').addClass('error');
                }
            }
    
            if (form_data[i].name === 'email') {
             isFormValid[1] = validateEmail(form_data[i].value);
                if (!isFormValid[1]) {
                    $('#email').addClass('error');
                }
            }
    
            if (form_data[i].name === 'message') {
             isFormValid[2] = Boolean(form_data[i].value);
                if (!isFormValid[2]) {
                    $('#message').addClass('error');
                }
            }
            if (form_data[i],name === 'adress') {
                bot = true;
            }
        }
    
        var allValid = isFormValid.every(function(elem) { return elem; });
        
        console.log('allvalid ', allValid, isFormValid);
    
        event.preventDefault();
        event.stopPropagation();

        var data = $('#contactform').serialize();
        data.csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val();
    
        if (allValid && !bot) {
            $.ajax({
                type: 'post',
                url: $('#submit').data('url'),
                data: data,
                success: function () {
                    console.log('success');
                    // $('#formtext').text('Ваше сообщение отправлено.');
                    $('#name').val('');
                    $('#email').val('');
                    $('#message').val('');
                },
                error: function() {
                    console.log('error');
                    $('#formtext').html('<span style="color: red">Что то пошло не так, сервер не отвечает. Попробуйте связаться с нами позднее.</span>');
                }
            });

            return allValid;
        } else {
            $('#formtext').html('<span style="color: red">Заполните форму корректными данными</span>');
        }
    
    });

});

function validateEmail(email) {
    var regexp = /[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?/;
    return regexp.test(email);
}