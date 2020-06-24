$("#follow").click(function (e) {
    e.preventDefault();
    var href = this.href;
    console.log(href);
    $.ajax({
        url: href,
        success: function (response) {
            if (response["is_following"]) {
                if (response["is_question_follow"]) {
                    $("#follow").removeClass('badge-danger').addClass('badge-info');
                    $("#follow").html("Unfollow Question");
                }
                else {
                    $("#follow").removeClass('btn-danger').addClass('btn-outline-danger');
                    $("#follow").html("Unfollow");
                }
            }
            else {
                if (!(response["is_following"])) {
                    if (response["is_question_follow"]) {
                        $("#follow").removeClass('badge-info').addClass('badge-danger');
                        $("#follow").html("Follow Question");
                    }
                    else {
                        $("#follow").removeClass('btn-outline-danger').addClass('btn-danger');
                        $("#follow").html("Follow");
                    }
                }
                else {
                    window.location.href = '/users/login/';
                }
            }
        },
        error: function (response) {
            console.log(response);
        }
    });
});