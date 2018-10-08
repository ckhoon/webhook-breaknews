'use strict';
var express = require('express');

module.exports = function(app) {
 // var gameDataController = require('../Controllers/GameDataController');

	var apiRoutes =  express.Router();

	app.get('/',function(req,res){
    res.send('We are happy to see you using Chat Bot Webhook @ get');
  });

	app.post('/',function(req,res){
		console.log(req.body.queryResult.outputContexts);
		var reply = 'Default webhook reply, -1';
		var source = '-1';
	  switch(req.body.queryResult.intent.displayName){
	    case 'Intro_good' :
	      reply = 'Nope, I am alone. How is my result?';
	      source = '0';
	      break;
	    case 'Intro_sad' :
	      reply = 'You dont remember? How is my result?';
	      source = '1';
	      break;
	    case 'Intro_shock' :
	      reply = 'I am shocked. How is my result?';
	      source = '2';
	      break;
	    case 'Result_good' :
	      reply = 'I was worried about my cancer';
	      source = '0';
	      break;
	    case 'Result_sad' :
	      reply = 'I don\'t know. I am nervous';
	      source = '1';
	      break;
	    case 'Result_shock' :
	      reply = 'I am shocked.';
	      source = '2';
	      break;
	    default :
	      reply = "Default webhook reply";
	      source = '-1';
	  }
	  res.json({'fulfillmentText': reply,
							'source': source});
    //res.send('We are happy to see you using Chat Bot Webhook @ post');
  });

	// registerUser Route
	//app.route('/')
	//  .post(gameDataController.processRequest);
};
