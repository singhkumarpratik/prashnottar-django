$('input[name="request"]').click(function (e) {
    e.preventDefault();
    var user_pk = $(this).attr("data-pk");
    var question_pk = $(this).attr("data-qpk");
    var href = window.location.origin + "/question/request/" + question_pk + "/" + user_pk;
    $.ajax({
        url: href,
        success: function (response) {
            if (response["success"]) {
                $(".request" + user_pk + question_pk).attr({
                    'disabled': true,
                    'value': 'Request Sent',
                });
            }
        },
        error: function (response) {
            console.log(response);
        }
    });
});