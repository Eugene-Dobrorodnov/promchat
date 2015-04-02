$( document ).ready(function() {

//var ws = new WebSocket("ws://127.0.0.1:5000/ws/"+ROOM_ID);
var ws = new WebSocket("ws://https://promchat.herokuapp.com/ws"+ROOM_ID)

ws.onmessage = function (evt) {
    console.log('Socket open');

    var data = JSON.parse(evt.data)

    $('.table > tbody:first').prepend(data['html']);
    var n = $(document).height();
    $('html, body').animate({ scrollTop: n });
};


$('#msg_form').submit(function(){
    $massage = $("input[name='msg']")
    var msg = $massage.val()
    $massage.val('');
    ws.send(msg);
    return false;
});

ws.onclose = function () {
    console.log('Socket close');
};

});