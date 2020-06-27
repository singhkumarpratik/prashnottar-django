$('input[name="dismiss"]').click(function (e) {
    e.preventDefault();
    var pk = $(this).attr("data-pk");
    if (pk) {
        var href = window.location.origin + "/notifications/dismiss/" + pk;
    } else {
        var href = window.location.origin + "/notifications/dismiss/all";
    }
    $.ajax({
        url: href,
        success: function (response) {
            if (response["success"]) {
                if (response["dismiss_all"]) {
                    $(".dismiss-all").addClass('animate__slideOutRight').delay(1000).queue(function () { $(this).remove(); });;
                }
                else {
                    $(".dismiss" + pk).addClass('animate__slideOutRight').delay(1000).queue(function () { $(this).remove(); });;
                }
            }
        },
        error: function (response) {
            console.log(response);
        }
    });
});