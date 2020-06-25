$(document).ready(function () {
    $(".score-form").each(function (index) {
        var is_comment = $(this).attr("data-is-comment");
        var question_pk = $(this).attr("data-pk");
        var is_profile_view = $(this).attr("data-profile");
        console.log(is_profile_view);
        var base_url = window.location.origin + "/";
        var upvote_fill_url = base_url + "static/imgs/qnA/caret-up-square-fill.svg";
        var downvote_fill_url = base_url + "static/imgs/qnA/caret-down-square-fill.svg";
        if (is_profile_view) {
            var url = base_url + question_pk + "/vote";
            console.log(url);
        }
        else {
            var url = question_pk + "/vote";
        }
        $.ajax({
            type: 'GET',
            url: url,
            data: { "status": question_pk, is_comment: is_comment, },
            success: function (response) {
                if (response["is_question_detail"]) {
                    if (is_comment) {
                        if (response["has_upvoted"]) {
                            $(".Up_comment" + question_pk).attr('src', upvote_fill_url);
                        }
                        if (response["has_downvoted"]) {
                            $(".Down_comment" + question_pk).attr('src', downvote_fill_url);
                        }
                    }
                    else {
                        if (response["has_upvoted"]) {
                            $(".Up" + question_pk).attr('src', upvote_fill_url);
                        }
                        if (response["has_downvoted"]) {
                            $(".Down" + question_pk).attr('src', downvote_fill_url);
                        }
                    }
                }
                else {
                    if (response["has_upvoted"]) {
                        $(".Up" + question_pk).attr('src', upvote_fill_url);
                    }
                    if (response["has_downvoted"]) {
                        $(".Down" + question_pk).attr('src', downvote_fill_url);
                    }
                }
            }
        });
    });
});
$('input[name="up"]').click(function (e) {
    e.preventDefault();
    var is_comment = $(this).attr("data-is-comment");
    var question_pk = $(this).attr("data-pk");
    var is_profile_view = $(this).attr("data-profile");
    var base_url = window.location.origin + "/";
    var upvote_url = base_url + "static/imgs/qnA/caret-up-square.svg";
    var upvote_fill_url = base_url + "static/imgs/qnA/caret-up-square-fill.svg";
    var downvote_url = base_url + "static/imgs/qnA/caret-down-square.svg";
    if (is_profile_view) {
        var url = window.location.origin + "/" + question_pk + "/vote";
        console.log(url);
    }
    else {
        var url = question_pk + "/vote";
        console.log("hihih");
    }
    $.ajax({
        type: 'GET',
        url: url,
        data: { "up": 'Up', is_comment: is_comment, },
        success: function (response) {
            if (response["valid"]) {
                if (response["data"]["is_question_detail"]) {
                    if (is_comment) {
                        if (response["data"]["has_upvoted"]) {
                            console.log("User upvoted");
                            $(".Up_comment" + question_pk).attr('src', upvote_fill_url);
                            $(".Down_comment" + question_pk).attr('src', downvote_url);
                        }
                        else {
                            console.log("User upvote removed");
                            $(".Up_comment" + question_pk).attr('src', upvote_url);
                        }
                    }
                    else {
                        if (response["data"]["has_upvoted"]) {
                            console.log("User upvoted");
                            $(".Up" + question_pk).attr('src', upvote_fill_url);
                            $(".Down" + question_pk).attr('src', downvote_url);
                        }
                        else {
                            console.log("User upvote removed");
                            $(".Up" + question_pk).attr('src', upvote_url);
                        }
                    }
                }
                else {
                    if (response["data"]["has_upvoted"]) {
                        console.log("User upvoted");
                        $(".Up" + question_pk).attr('src', upvote_fill_url);
                        $(".Down" + question_pk).attr('src', downvote_url);
                    }
                    else {
                        console.log("User upvote removed");
                        $(".Up" + question_pk).attr('src', upvote_url);
                    }
                }
                if (is_comment) {
                    $('#score_comment' + question_pk).html(response["data"]["score"]);
                }
                else {
                    $('#score' + question_pk).html(response["data"]["score"]);
                }
            }
            else {
                window.location.href = '/users/login/';
            }
        },
        error: function (response) {
            console.log(response)
        }
    });
});
$('input[name="down"]').click(function (e) {
    e.preventDefault();
    var is_comment = $(this).attr("data-is-comment");
    var question_pk = $(this).attr("data-pk");
    var is_profile_view = $(this).attr("data-profile");
    var base_url = window.location.origin + "/";
    var upvote_url = base_url + "static/imgs/qnA/caret-up-square.svg";
    var downvote_fill_url = base_url + "static/imgs/qnA/caret-down-square-fill.svg";
    var downvote_url = base_url + "static/imgs/qnA/caret-down-square.svg";
    if (is_profile_view) {
        var url = window.location.origin + "/" + question_pk + "/vote";
        console.log(url);
    }
    else {
        var url = question_pk + "/vote";
        console.log("hihih");
    }
    $.ajax({
        type: 'GET',
        url: url,
        data: { "down": 'Down', is_comment: is_comment, },
        success: function (response) {
            if (response["valid"]) {
                if (response["data"]["is_question_detail"]) {
                    if (is_comment) {
                        if (response["data"]["has_downvoted"]) {
                            console.log("User downvoted");
                            $(".Down_comment" + question_pk).attr('src', downvote_fill_url);
                            $(".Up_comment" + question_pk).attr('src', upvote_url);
                        }
                        else {
                            console.log("User downvote removed");
                            $(".Down_comment" + question_pk).attr('src', downvote_url);
                        }
                    }
                    else {
                        if (response["data"]["has_downvoted"]) {
                            console.log("User downvoted");
                            $(".Down" + question_pk).attr('src', downvote_fill_url);
                            $(".Up" + question_pk).attr('src', upvote_url);
                        }
                        else {
                            console.log("User downvote removed");
                            $(".Down" + question_pk).attr('src', downvote_url);
                        }
                    }
                }
                else {
                    if (response["data"]["has_downvoted"]) {
                        console.log("User downvoted");
                        $(".Down" + question_pk).attr('src', downvote_fill_url);
                        $(".Up" + question_pk).attr('src', upvote_url);
                    }
                    else {
                        console.log("User downvote removed");
                        $(".Down" + question_pk).attr('src', downvote_url);
                    }
                }
                if (is_comment) {
                    $('#score_comment' + question_pk).html(response["data"]["score"]);
                }
                else {
                    $('#score' + question_pk).html(response["data"]["score"]);
                }
            }
            else {
                window.location.href = '/users/login/';
            }
        },
        error: function (response) {
            console.log(response)
        }
    });
});