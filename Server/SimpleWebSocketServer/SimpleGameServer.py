'''
The MIT License (MIT)
Copyright (c) 2013 Dave P.

Modifications for SAM classes by pawelplodzpl
'''

import json
import signal
import sys
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer, SimpleSSLWebSocketServer
from optparse import OptionParser
import ssl

# using dictionary as a simple example packet holder - easy to modify and JSON-ify
dataPacket = dict(ID=0, int_list=[1, 2, 3], text='string', number=3.44, boolean=True, none=None)

# ???????????? START do 100!

dataPacket_init = {
	'packetStatus': 'init',
  	'id': 0
}
dataPacket_end = {
 	'packetStatus': 'end',
   	'isGameOver': True
 }


dict_xy = dict(x=0, y=0)
dict_player = dict(id=0, positionPlayer=dict_xy, positionBullet=dict_xy, positionWalls=dict_xy, score=0)

players_size = [{
    'id': 0,
    'height': 100,
    'width': 80
    },{
    'id': 1,
    'height': 100,
    'width': 80

    },{
    'id': 2,
    'height': 100,
    'width': 80

    },{
    'id': 3,
    'height': 100,
    'width': 80

    }]

dataPacket_game = {
	"packetStatus": "game",
    "explosions": [
       {
         "positionExplode": {"x": 0,"y":0}
       },
       {
         "positionExplode": {"x": 0,"y":0}
       }
      ],
        "players": [
      {
        "id": 0,
        "positionPlayer": {"x": 100, "y": 300},
        "positionBullet": {"x": 0, "y": 0},
        "positionWalls":  {"x": 0, "y": 0},
        "score": 0
      },
      {
        "id": 1,
        "positionPlayer": {"x": 200, "y": 10},
        "positionBullet": {"x": 0, "y": 0},
        "positionWalls":  {"x": 0, "y": 0},
        "score": 0
      },
      {
        "id": 2,
        "positionPlayer": {"x": 100, "y": 500},
        "positionBullet": {"x": 0, "y": 0},
        "positionWalls":  {"x": 0, "y": 0},
        "score": 0
      },
      {
        "id": 3,
        "positionPlayer": {"x": 200, "y": 350},
        "positionBullet": {"x": 0, "y": 0},
        "positionWalls":  {"x": 0, "y": 0},
        "score": 0
      }
    ]
}

avaiableIndexes = [0, 1, 2, 3]

endGame = 1

#??????? KONIEC

class SimpleEcho(WebSocket):
   def handleMessage(self):
      self.sendMessage(self.data)

   def handleConnected(self):
      pass

   def handleClose(self):
      pass
   def tmp(a): # ????????
       pass

clients = []

class SimpleGameServer(WebSocket): #????????????? START 209
      def handleMessage(self):
            for client in clients:
                decodedPacket = json.loads(self.data)

                if (endGame == 2):
                    print('endGame')
                    dataPacket_game['packetStatus'] = 'end'
                    toSend = json.dumps(dataPacket_game)
                    client.sendMessage(toSend)
                elif len(clients) >= 4:


                #if client != self:
                    # send back to all clients
                    toSend = json.dumps(dataPacket_game)
                    client.sendMessage(toSend)
                if client == self:
                #else:
                    if decodedPacket['packetStatus'] == 'init':
                        index = self.id
                        dataPacket_init['id']=index

                        toSend = json.dumps(dataPacket_init)
                        client.sendMessage(toSend)

                    elif decodedPacket['packetStatus'] == 'game':
                        updatePlayersWithPlayer(decodedPacket)
                        checkIfPlayerWasHited(decodedPacket)


      def handleConnected(self):
            for client in clients:
                client.sendMessage(u'player ' + self.address[0] + u' - connected')

                # send TEST PACKET
                encodedPacket = json.dumps(dataPacket)
                client.sendMessage(encodedPacket)
            self.id = avaiableIndexes[0]
            avaiableIndexes.remove(self.id)
            clients.append(self)
            if len(clients) >= 4:
                dataPacket_game['players'][0]['score'] = 0
                dataPacket_game['players'][1]['score'] = 0
                dataPacket_game['players'][2]['score'] = 0
                dataPacket_game['players'][3]['score'] = 0


      def handleClose(self):
            index = self.id
            clients.remove(self)
            avaiableIndexes.append(index)

            for client in clients:
                client.sendMessage(u'player' + self.address[0] + u' - disconnected')

def updatePlayersWithPlayer(data):

    playerId = data['id']
    player = dataPacket_game['players'][playerId]

    player['positionPlayer']['x'] = data['positionPlayer']['x']
    player['positionPlayer']['y'] = data['positionPlayer']['y']
    player['positionBullet']['x'] = data['positionBullet']['x']
    player['positionBullet']['y'] = data['positionBullet']['y']


def checkIfPlayerWasHited(data):
    bullet_x = data['positionBullet']['x'] + 32/2
    bullet_y = data['positionBullet']['y'] + 32/2

    players = dataPacket_game['players']

    for player in players:
        index = player['id']
        width = players_size[index]['width']
        heigth = players_size[index]['height']
        x = player['positionPlayer']['x'] + width/2
        y = player['positionPlayer']['y'] + heigth/2


        if (bullet_y > y - heigth/2 - 32/2  and bullet_y < y + heigth/2 + 32/2 ) and (bullet_x > x - width/2 -32/2 and bullet_x < x + width/2 +32/2):

            if data['id'] != player['id']:
                id = data['id']
                dataPacket_game['players'][id]['score'] +=1

                if dataPacket_game['players'][id]['score'] >= 16:
                    print('>5')
                    global  endGame
                    endGame = 2
                    print(endGame)
#??????? KONIEC

if __name__ == "__main__":
   parser = OptionParser(usage="usage: %prog [options]", version="%prog 1.0")
   parser.add_option("--host", default='', type='string', action="store", dest="host", help="hostname (localhost)")
   parser.add_option("--port", default=8070, type='int', action="store", dest="port", help="port (8090)")
   parser.add_option("--example", default='game', type='string', action="store", dest="example", help="echo, game")
   parser.add_option("--ssl", default=0, type='int', action="store", dest="ssl", help="ssl (1: on, 0: off (default))")
   parser.add_option("--cert", default='./cert.pem', type='string', action="store", dest="cert", help="cert (./cert.pem)")
   parser.add_option("--key", default='./key.pem', type='string', action="store", dest="key", help="key (./key.pem)")
   parser.add_option("--ver", default=ssl.PROTOCOL_TLSv1, type=int, action="store", dest="ver", help="ssl version")

   (options, args) = parser.parse_args()

   cls = SimpleEcho
   if options.example == 'game':
      cls = SimpleGameServer

   if options.ssl == 1:
      server = SimpleSSLWebSocketServer(options.host, options.port, cls, options.cert, options.key, version=options.ver)
   else:
      server = SimpleWebSocketServer(options.host, options.port, cls)

   def close_sig_handler(signal, frame):
      server.close()
      sys.exit()

   signal.signal(signal.SIGINT, close_sig_handler)

   server.serveforever()
