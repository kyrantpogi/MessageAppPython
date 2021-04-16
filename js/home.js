$(document).ready(function () {
    var username = sessionStorage.getItem("username");
    var receiver;
    var interval;
    var current_room_name;
    var last_message_id = 0;
    var multiply_value = 0;
    var messagecount = 0;

    //========================initialize socket==========================
    const socket = io("http://192.168.0.111:80/");
    socket.on("connect", (data) => {
        console.log(data);
        
    });

    //disconnect
    socket.on("disconnect", () => {
        console.log("disconnect");
    });
    //----------------------end------------------------------------------

    ajax_get("http://192.168.0.158:81/get-rooms?owner="+username, (data) => { 
        console.log(data);
        for (let i=0; i<data.length; i++) {
            if (data[i]["shared"] == username) {
                $("#room-panel").append("<tr>");
                $("#room-panel").append("<td><span id='stopinterval' class='badge badge-secondary'>"+data[i]["owner"]+"</span></td>");
                $("#room-panel").append("<td class='room-name' data-room='"+data[i]["room_name"]+"'><span id='stopinterval' class='badge badge-warning'>"+data[i]["room_name"]+"</span></td>");
                $("#room-panel").append("</tr>")
            } else {
                $("#room-panel").append("<tr>");
                $("#room-panel").append("<td><span id='stopinterval' class='badge badge-secondary'>"+data[i]["shared"]+"</span></td>");
                $("#room-panel").append("<td class='room-name' data-room='"+data[i]["room_name"]+"'><span id='stopinterval' class='badge badge-warning'>"+data[i]["room_name"]+"</span></td>");
                $("#room-panel").append("</tr>")
            }
            
        }
    });
    
    //back to login if no users
    if (username == "admin") {
        $("#stopinterval").click(function () {
            console.log("stop interval");
            clearInterval(interval);
        });
        $("#sendMessage").click(function () {
            socket.emit("message", {"message":"Message "+messagecount});
            messagecount++;
        });
    } else {
        $("#stopinterval").remove();
        $("#sendMessage").remove();
    }
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
        current_room_name = room_name
        receiver = $(this).text();
        console.log($(this));
        $("#place-room-name").text(room_name);
        $("#messages").empty();
        $("#msgbox").val("");
        multiply_value = 0;

        ajax_get("http://192.168.0.158:81/get-messages?room="+room_name, (data) => { 
            console.log(data);
            last_message_id = data[0]["id"];
            for (let i=data.length-1; i>-1; i--) {
                addMessage(data[i]["sender"], data[i]["message"], data[i]["date_time"]);
            }
            var top_scroll = $("#messages")[0].scrollHeight;
            $("#messages").scrollTop(top_scroll);
            
            //load data when scrolled up
            $("#messages").on("scroll", (e) => {
                var scrollLoc = $("#messages").scrollTop();
                //get more messages
                if (scrollLoc == 0) {
                    multiply_value++;
                    ajax_get("http://192.168.0.158:81/scroll-load-message?room="+room_name+"&x="+multiply_value, (data) => {
                        for (let i=0; i<data.length; i++) {
                            addPrependMessage(data[i]["sender"], data[i]["message"], data[i]["date_time"]);
                        }
                    });
                    
                }
            });

        });

        

        // last message
        // polling
        // interval = setInterval(() => {
        //     ajax_get("http://192.168.0.158:81/last-message?room="+room_name, (data) => {
        //         try {
        //             current_message_id = data[data.length-1]["id"];
        //             // console.log({"cur_id": current_message_id, "last_id": last_message_id});
        //             // console.log(data);
        //             if (current_message_id != last_message_id) {
        //                 last_message_id = current_message_id;
        //                 data.forEach((item,index) => {
        //                     addMessage(item["sender"], item["message"], item["date_time"]);
        //                 });
        //                 $("#messages").scrollTop($("#messages")[0].scrollHeight);
        //             }
        //         } catch (err) {
        //             throw "No Messages Found." + err;
        //         }
        //     });
        // }, 1000);

    });

    //broadcast message get
    socket.on("message", (data) => {
        console.log(current_room_name);
        if (current_room_name == data["room_name"]) {
            console.log(data);
            addMessage(data["sender"], data["message"], data["date_time"]);
            $("#messages").scrollTop($("#messages")[0].scrollHeight);
        }
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
            socket.emit("message", data);
            // ajax_post("http://192.168.0.158:81/send-message",data,(e) => {console.log(e);});
        }    
        $("#msgbox").val("");
    });

    
});

