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

function addMessage(sender,message,date) {
    var username = sessionStorage.getItem("username");
    if (sender == username) {
        $("#messages").append("<div class='message-wrapper'>\
        <span class='message-sender badge badge-primary'>"+message+" "+"<span class='badge badge-light'>"+date+"</span></span>"+"\
        </div>");
    } else {
        $("#messages").append("<div class='message-wrapper'>\
        <span class='message-receiver badge badge-primary'><span class='badge badge-light'>"+date+"</span>"+" "+message+"</span>"+"\
        </div>");
    }
}

function addPrependMessage(sender,message,date) {
    var username = sessionStorage.getItem("username");
    if (sender == username) {
        $("#messages").prepend("<div class='message-wrapper'>\
        <span class='message-sender badge badge-primary'>"+message+" "+"<span class='badge badge-light'>"+date+"</span></span>"+"\
        </div>");
    } else {
        $("#messages").prepend("<div class='message-wrapper'>\
        <span class='message-receiver badge badge-primary'><span class='badge badge-light'>"+date+"</span>"+" "+message+"</span>"+"\
        </div>");
    }
}


        