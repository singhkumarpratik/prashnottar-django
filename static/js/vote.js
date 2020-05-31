$(document).ready(function () {
    $(".score-form").each(function (index) {
        var is_comment = $(this).attr("data-is-comment");
        var question_pk = $(this).attr("data-pk");
        var url = question_pk + "/vote";
        $.ajax({
            type: 'GET',
            url: url,
            data: { "status": question_pk, is_comment: is_comment, },
            success: function (response) {
                if (response["is_question_detail"]) {
                    if (is_comment) {
                        if (response["has_upvoted"]) {
                            $(".Up_comment" + question_pk).attr('src', '../../static/imgs/qnA/caret-up-square-fill.svg');
                        }
                        if (response["has_downvoted"]) {
                            $(".Down_comment" + question_pk).attr('src', '../../static/imgs/qnA/caret-down-square-fill.svg');
                        }
                    }
                    else {
                        if (response["has_upvoted"]) {
                            $(".Up" + question_pk).attr('src', '../../static/imgs/qnA/caret-up-square-fill.svg');
                        }
                        if (response["has_downvoted"]) {
                            $(".Down" + question_pk).attr('src', '../../static/imgs/qnA/caret-down-square-fill.svg');
                        }
                    }
                }
                else {
                    if (response["has_upvoted"]) {
                        $(".Up" + question_pk).attr('src', 'static/imgs/qnA/caret-up-square-fill.svg');
                    }
                    if (response["has_downvoted"]) {
                        $(".Down" + question_pk).attr('src', 'static/imgs/qnA/caret-down-square-fill.svg');
                    }
                }
            }
        });
    });
});
$('input[name="up"]').click(function (e) {
    e.preventDefault();
    var is_comment = $(this).attr("data-is-comment");
    console.log(is_comment);
    var question_pk = $(this).attr("data-pk");
    var url = question_pk + "/vote";
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
                            $(".Up_comment" + question_pk).attr('src', '../../static/imgs/qnA/caret-up-square-fill.svg');
                            $(".Down_comment" + question_pk).attr('src', '../../static/imgs/qnA/caret-down-square.svg');
                        }
                        else {
                            console.log("User upvote removed");
                            $(".Up_comment" + question_pk).attr('src', '../../static/imgs/qnA/caret-up-square.svg');
                        }
                    }
                    else {
                        if (response["data"]["has_upvoted"]) {
                            console.log("User upvoted");
                            $(".Up" + question_pk).attr('src', '../../static/imgs/qnA/caret-up-square-fill.svg');
                            $(".Down" + question_pk).attr('src', '../../static/imgs/qnA/caret-down-square.svg');
                        }
                        else {
                            console.log("User upvote removed");
                            $(".Up" + question_pk).attr('src', '../../static/imgs/qnA/caret-up-square.svg');
                        }
                    }
                }
                else {
                    if (response["data"]["has_upvoted"]) {
                        console.log("User upvoted");
                        $(".Up" + question_pk).attr('src', 'static/imgs/qnA/caret-up-square-fill.svg');
                        $(".Down" + question_pk).attr('src', 'static/imgs/qnA/caret-down-square.svg');
                    }
                    else {
                        console.log("User upvote removed");
                        $(".Up" + question_pk).attr('src', 'static/imgs/qnA/caret-up-square.svg');
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
    var url = question_pk + "/vote";
    console.log(url)
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
                            $(".Down_comment" + question_pk).attr('src', '../../static/imgs/qnA/caret-down-square-fill.svg');
                            $(".Up_comment" + question_pk).attr('src', '../../static/imgs/qnA/caret-up-square.svg');
                        }
                        else {
                            console.log("User downvote removed");
                            $(".Down_comment" + question_pk).attr('src', '../../static/imgs/qnA/caret-down-square.svg');
                        }
                    }
                    else {
                        if (response["data"]["has_downvoted"]) {
                            console.log("User downvoted");
                            $(".Down" + question_pk).attr('src', '../../static/imgs/qnA/caret-down-square-fill.svg');
                            $(".Up" + question_pk).attr('src', '../../static/imgs/qnA/caret-up-square.svg');
                        }
                        else {
                            console.log("User downvote removed");
                            $(".Down" + question_pk).attr('src', '../../static/imgs/qnA/caret-down-square.svg');
                        }
                    }
                }
                else {
                    if (response["data"]["has_downvoted"]) {
                        console.log("User downvoted");
                        $(".Down" + question_pk).attr('src', 'static/imgs/qnA/caret-down-square-fill.svg');
                        $(".Up" + question_pk).attr('src', 'static/imgs/qnA/caret-up-square.svg');
                    }
                    else {
                        console.log("User downvote removed");
                        $(".Down" + question_pk).attr('src', 'static/imgs/qnA/caret-down-square.svg');
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