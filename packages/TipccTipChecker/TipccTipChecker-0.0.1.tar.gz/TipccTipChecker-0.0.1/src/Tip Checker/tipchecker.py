class tipchecker:
  def checktip(tip, tipauthor, jsonfile):
    tip = (str(tip))
    tipauthor = (str(tipauthor))

    if tipauthor != ('617037497574359050'):
      print("The tip is not valid! (Usually because a user tried to imitate tip.cc)")
      data = '{"LastTip": {"realtip": "0", "whosent": "badtip", "whoreceived": "badtip", "amount": "badtip", "currency": "badtip", "usdvalue": "badtip"}}'
          
      with open(jsonfile, 'w') as f:
        f.write(str(data))
        
    elif tipauthor == ('617037497574359050'):
      tip = tip.replace("<", "")
      tip = tip.replace(">", "")
      tip = tip.replace("@", "")
      tip = tip.replace("(", "")
      tip = tip.replace(").", "")
      tip = tip.replace("≈", "")
      tip = tip.replace("sent", "")
      tip = tip.replace("$", "")
      tip = tip.replace("*", "")
      tip = (tip.split())
      print(tip)
      whosent = tip[0]
      whoreceived = tip[1]
      amount = tip[2]
      crypto = tip[3]
      usdvalue = tip[4]
      
      print(whosent + ' sent ' + whoreceived + ' ' + amount + ' ' + crypto + ' which is worth about $' + usdvalue)
      
      
      data = '{"LastTip": {"realtip": "1", "whosent": "' + whosent + '", "whoreceived": "' + whoreceived + '", "amount": "' + amount + '", "currency": "' + crypto + '", "usdvalue": "' + usdvalue + '"}}'
          
      with open(jsonfile, 'w') as f:
        f.write(str(data))