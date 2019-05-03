/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author guilhermeribeiro
 */

var zerorpc = require("zerorpc");

var client = new zerorpc.Client();
client.connect("tcp://127.0.0.1:4242");

/*client.invoke("hello", "RPC", "2", function(error, res, more) {
    console.log(res);
});*/

client.invoke("calc_peso", "1.68", "masculino", function(error, res, more) {
    console.log("Seu peso ideal deve ser: ", parseFloat(res));
});

