function ajax_post(url,data,success) {
    $.ajax({
        type: "POST",
        url: url,
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(data),
        success: function(e) {
            success(e);
        }
    });
}

function ajax_get(url,success) {
    $.ajax({
        type: "GET",
        url: url,
        success: function(e) {
            success(e);
        }
    });
}