import { Ludo } from './ludo/ludo.js' ;
import { BASE_POSITIONS, HOME_ENTRANCE, HOME_POSITIONS, PLAYERS, SAFE_POSITIONS, START_POSITIONS, STATE, TURNING_POINTS } from './ludo/constants.js';

// Get the room code from the HTML attribute
// const roomCode = document.getElementById("game_board").getAttribute("room_code");
// console.log(roomCode);
// WebSocket connection string
const url = 'ws://' + window.location.host + '/ws/ludo/game/' ;

// // Initialize WebSocket
const ws = new WebSocket(url);
const ludo = new Ludo();
// ludo.listenDiceClick();
// console.log('dice value = ' , ludo._diceValue);
// console.log('dice 1value = ' , ludo.diceValue);

ludo.currentPositions = JSON.parse(JSON.stringify(BASE_POSITIONS));
let players = [] ;
let playerNumber = 0;
// let playerAdded = false;

ws.onopen = function(){
    console.log('opened');
    ws.send(JSON.stringify({ type: 'newClient', client: 'ClientName' }));
    // ws.send(JSON.stringify({ type: 'getPlayers' }));
    // ws.send(JSON.stringify({ type: 'players' }));
    // let playerNumber = players.length + 1;
    // let player = "P" + playerNumber;
    // players.push({ player: player, ws: this });

    // players.forEach(p => {
    //     p.ws.send(JSON.stringify(players.map(p => p.player)));
    // });
    // ws.send("Player " + player + " connected");
    // PLAYERS.forEach(player => {
    // [0, 1, 2, 3].forEach(piece => {
    //         console.log(player,ludo.currentPositions[player][piece]);
    //         ludo.setPiecePosition(player, piece, ludo.currentPositions[player][piece])
    //     })
    // });
    // this.listenDiceClick();
    // this.listenPieceClick();
    // this.resetGame();
    // ws.send("i send this message");
}

ws.onmessage = function(event){
        const data = JSON.parse(event.data);
        if (data.type === 'players') {
            players = data.players;
            console.log('Players:', players);
            while(players[playerNumber] !== undefined){
                [0, 1, 2, 3].forEach(piece => {
                         console.log(players[playerNumber],ludo.currentPositions[players[playerNumber]][piece]);
                         ludo.setPiecePosition(players[playerNumber], piece, ludo.currentPositions[players[playerNumber]][piece])
                     })
                playerNumber++;
            }
        }
      };
    // console.log(event);
    // console.log(' : message received');
    // let data = JSON.parse(event.data);
    // if (data.type === 'players') {
    //     players = data.players;
    //     console.log('palyers',players);
    //     if (!playerAdded) {
    //         let playerNumber = players.length + 1;
    //         console.log(playerNumber);
    //         let player = "P" + playerNumber;
    //         players.push({ player: player, ws: this });

    //         players.forEach(p => {
    //             p.ws.send(JSON.stringify(players.map(p => p.player)));
    //         });
    //         console.log("Player " + player + " connected");
    //         playerAdded = true;
    //     }
    // }


ws.onclose = function(event){
    console.log(event);
    console.log('closed ');
}

