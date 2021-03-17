$(document).ready(function () {
    $("#submit").click(function () {
        var username = $("#username").val();
        var password = $("#password").val();
        var obj = {
            "username": username,
            "password": password
        }
        ajax_post("http://192.168.0.158:81/login",obj,(data) => {
            if (data["login"] == "true") {
                sessionStorage.setItem("username", username);
                window.location.href = "http://192.168.0.158/home.html";
            }
        });
    });

});