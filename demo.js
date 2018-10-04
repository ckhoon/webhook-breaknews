'use strict';

const http = require('http');

exports.painWebhook = (req, res) => {
  var reply = 'ah ha..';
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
      reply = "Sorry I don't understand your question.";
  }
  res.json({'fulfillmentText': reply})
};