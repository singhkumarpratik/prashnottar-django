$("#follow").click(function (e) {
    e.preventDefault();
    var href = this.href;
    var question_pk = $(this).attr("data-pk");
    console.log(href);
    console.log(question_pk);
    $.ajax({
        url: href,
        success: function (response) {
            if (response["is_following"]) {
                $("#follow").removeClass('btn-danger').addClass('btn-outline-danger');
                $("#follow").html("Unfollow");
            }
            else {
                if (!(response["is_following"])) {
                    $("#follow").removeClass('btn-outline-danger').addClass('btn-danger');
                    $("#follow").html("Follow");
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