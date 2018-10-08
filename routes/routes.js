'use strict';
var express = require('express');

module.exports = function(app) {
 // var gameDataController = require('../Controllers/GameDataController');

	var apiRoutes =  express.Router();

	app.get('/',function(req,res){
    res.send('We are happy to see you using Chat Bot Webhook @ get');
  });

	app.post('/',function(req,res){
	  switch(req.body.queryResult.intent.displayName){
	    case 'Pain' :
	      reply = 'I am having chest pain'
	      break;
	    case 'Pain.Duration.context' :
	      reply = "The chest pain starts about 4 days ago"
	      break
	    case 'Pain.Area.context' :
	      reply = "The chest pain is at the upper left area"
	      break
	    default :
	      reply = "Default webhook reply";
	  }
	  res.json({'fulfillmentText': reply})
    //res.send('We are happy to see you using Chat Bot Webhook @ post');
  });

	// registerUser Route
	//app.route('/')
	//  .post(gameDataController.processRequest);
};
