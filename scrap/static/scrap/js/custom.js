(function ($) {
    $(document).ready(function(){
        $('#btn-scan').click(function(){
            var csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val();
            var data = {
                csrfmiddlewaretoken: csrfmiddlewaretoken
            };
            $.post('/', data, function(response){
                var task_id = response['task_id'];
                $('#task_id').text(task_id);
                $('#scanning').removeClass('hidden');

                var timer = setInterval(function(){
                    var data = {
                        id: task_id
                    };
                    $.get("/check", data, function(response){
                        if(response['is_ready']){
                            $('#scanning').addClass('hidden');
                            $('#result').removeClass('hidden');
                            clearInterval(timer);
                        }
                    }, "json");
                }, 3000);


            }, 'json');
        });
    });
})(jQuery);
