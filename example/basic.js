//var BOSH_SERVICE = 'http://localhost:5280/xmpp-httpbind'
var BOSH_SERVICE = 'http://localhost:5280/http-bind'


var connection = null;

function log(msg)
{
    $('#log').append('<div></div>').append(document.createTextNode(msg));
}

function rawInput(data)
{
    log('RECV: ' + data);
}

function rawOutput(data)
{
    log('SENT: ' + data);
}

function onMessage(msg) {
    var to = msg.getAttribute('to');
    var from = msg.getAttribute('from');
    var type = msg.getAttribute('type');
    var elems = msg.getElementsByTagName('body');

    if (type == "chat" && elems.length > 0) {
      var body = elems[0];
      alert(Strophe.getText(body));
    }
    return true;
}

function onConnect(status)
{
    if (status == Strophe.Status.CONNECTING) {
	log('Strophe is connecting.');
    } else if (status == Strophe.Status.CONNFAIL) {
	log('Strophe failed to connect.');
    } else if (status == Strophe.Status.DISCONNECTING) {
	log('Strophe is disconnecting.');
    } else if (status == Strophe.Status.DISCONNECTED) {
	log('Strophe is disconnected.');
    } else if (status == Strophe.Status.CONNECTED) {
	log('Strophe is connected.');
  // hack the domain for bow 
  var from = currentUser.split('@')[0] + '@localhost';
  connection.addHandler(onMessage, null, 'message', null, null,  null);
  connection.send($msg({to: 'tarek2@localhost', from: from, 
     type: 'chat'}).c("body").t('some data'));

    }

}

$(document).ready(function () {
    connection = new Strophe.Connection(BOSH_SERVICE);
    connection.rawInput = rawInput;
    connection.rawOutput = rawOutput;

});