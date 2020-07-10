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
                        if (response["is_user_follow"]) {
                            $("#follow").removeClass('btn-outline-danger').addClass('btn-danger');
                            $("#follow").html("Follow");
                        }
                        else {
                            window.location.href = '/users/login/';
                        }
                    }
                }
            }
        },
        error: function (response) {
            console.log(response);
        }
    });
});
$('input[name="follow_list"]').click(function (e) {
    e.preventDefault();
    var user_slug = $(this).attr("data-to-user");
    var href = window.location.origin + "/users/follow_toggle/" + user_slug;
    $.ajax({
        url: href,
        success: function (response) {
            if (response["is_following"]) {
                $(".follow" + user_slug).removeClass('btn-danger').addClass('btn-outline-danger');
                $(".follow" + user_slug).attr("value", "Unfollow");
            }
            else {
                if (!(response["is_following"])) {
                    if (response["is_user_follow"]) {
                        $(".follow" + user_slug).removeClass('btn-outline-danger').addClass('btn-danger');
                        $(".follow" + user_slug).attr("value", "Follow");
                    }
                    else {
                        window.location.href = '/users/login/';
                    }
                }

            }
        },
        error: function (response) {
            console.log(response);
        }
    });
});