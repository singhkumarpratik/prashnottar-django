$(document).ready(function () {
    $(".score-form").each(function (index) {
        var question_pk = $(this).attr("data-pk");
        var url = question_pk + "/vote";
        $.ajax({
            type: 'GET',
            url: url,
            data: { "status": question_pk },
            success: function (response) {
                if (response["is_question_detail"]) {
                    if (response["has_upvoted"]) {
                        $(".Up" + question_pk).attr('src', '../../static/imgs/qnA/caret-up-square-fill.svg');
                    }
                    if (response["has_downvoted"]) {
                        $(".Down" + question_pk).attr('src', '../../static/imgs/qnA/caret-down-square-fill.svg');
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
    var question_pk = $(this).attr("data-pk");
    var url = question_pk + "/vote";
    console.log(url)
    $.ajax({
        type: 'GET',
        url: url,
        data: { "up": 'Up' },
        success: function (response) {
            if (response["valid"]) {
                if (response["data"]["is_question_detail"]) {
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
                $('#score' + question_pk).html(response["data"]["score"]);
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
    var question_pk = $(this).attr("data-pk");
    var url = question_pk + "/vote";
    console.log(url)
    $.ajax({
        type: 'GET',
        url: url,
        data: { "down": 'Down' },
        success: function (response) {
            if (response["valid"]) {
                if (response["data"]["is_question_detail"]) {
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
                $('#score' + question_pk).html(response["data"]["score"]);
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