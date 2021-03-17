$(document).ready(function () {
    var username = sessionStorage.getItem("username");
    var receiver;
    var interval;
    var last_message_id = 0;
    ajax_get("http://192.168.0.158:81/get-rooms?owner="+username, (data) => { 
        for (let i=0; i<data.length; i++) {
            if (data[i]["shared"] == username) {
                $("#room-panel").append("<button type='button' class='btn btn-warning room-name' data-room='"+data[i]["room_name"]+"'>"+data[i]["owner"]+"</button>");
            } else {
                $("#room-panel").append("<button type='button' class='btn btn-warning room-name' data-room='"+data[i]["room_name"]+"'>"+data[i]["shared"]+"</button>")
            }
            
        }
    });
    
    //back to login if no users
    if (username == null) {
        window.location.href = "http://192.168.0.158/index.html";
    }
    $("#nameTag").text(username);

    $("#logout").click(function () {
        sessionStorage.removeItem("username");
        window.location.href = "http://192.168.0.158/index.html";
    });

    $("#composeBtn").click(function () {
        $(".mainPanel").addClass("dim");
        $("#room-name").addClass("hide");
        $("#composeForm").removeClass("hide");
    });

    $("#submitCompose").click(function () {
        var recipient = $("#recipient");
        if (recipient.val() != "") {
            ajax_post("http://192.168.0.158:81/compose-message",{
                "owner": username,
                "shared": recipient.val()
            }, (e) => { console.log(e); });

            recipient.val("");
            recipient.attr("placeholder", "Name of Recipient");

            $(".mainPanel").removeClass("dim");
            $("#room-name").removeClass("hide");
            $("#composeForm").addClass("hide");
            window.location.href = "http://192.168.0.158/home.html";

            
        } else {
            recipient.attr("placeholder", "Do Not Leave Blank");
        }
        
    });

    $("#close").click(function () {
        $(".mainPanel").removeClass("dim");
        $("#room-name").removeClass("hide");
        $("#composeForm").addClass("hide");
    });

    $("body").on("click", ".room-name", function(e) {
        e.preventDefault();
        room_name = $(this).attr("data-room");
        receiver = $(this).text();
        $("#place-room-name").text(room_name);
        $("#msgbox").val("");

        ajax_get("http://192.168.0.158:81/get-messages?room="+room_name, (data) => { 
            last_message_id = data[data.length-1]["id"];
            for (let i=0; i<data.length; i++) {
                if (data[i]["sender"] == username) {
                    $("#messages").append(" <div class='message-wrapper'>\
                    <p class='message-sender'>"+data[i]["message"]+" <- "+"["+data[i]["sender"]+"]"+"</p>"+"\
                    </div>");
                } else {
                    $("#messages").append(" <div class='message-wrapper'>\
                    <p class='message-receiver'>"+"["+data[i]["sender"]+"]"+" -> "+data[i]["message"]+"</p>"+"\
                    </div>");
                }
            }
            $("#messages").scrollTop($("#messages")[0].scrollHeight);
        });

        interval = setInterval(() => {
            console.log(room_name);
            ajax_get("http://192.168.0.158:81/last-message?room="+room_name, (data) => {
                try {
                    current_message_id = data[data.length-1]["id"];
                    if (current_message_id != last_message_id) {
                        last_message_id = current_message_id;
                        for (let i=0; i<data.length; i++) {
                            if (data[i]["sender"] == username) {
                                $("#messages").append(" <div class='message-wrapper'>\
                                <p class='message-sender'>"+data[i]["message"]+" <- "+"["+data[i]["sender"]+"]"+"</p>"+"\
                                </div>");
                            } else {
                                $("#messages").append(" <div class='message-wrapper'>\
                                <p class='message-receiver'>"+"["+data[i]["sender"]+"]"+" -> "+data[i]["message"]+"</p>"+"\
                                </div>");
                            }
                        }
                        $("#messages").scrollTop($("#messages")[0].scrollHeight);
                    }
                } catch {
                    throw "No Messages Found.";
                }
            });
        }, 1000);
    });

    $("#stopinterval").click(function () {
        clearInterval(interval);
    });

    $("#send").click(function () {
        var room_name = $("#place-room-name").text();
        if (room_name != "?") {
            var data = {
                "room_name": room_name,
                "message": $("#msgbox").val(),
                "sender": username,
                "receiver": receiver
            }
            ajax_post("http://192.168.0.158:81/send-message",data,(e) => {console.log(e);});
        }    
        $("#msgbox").val("");
    });

    
});

