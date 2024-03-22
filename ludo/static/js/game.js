import { Ludo } from './ludo/Ludo.js';

// Get the room code from the HTML attribute
// const roomCode = document.getElementById("game_board").getAttribute("room_code");
// console.log(roomCode);
// WebSocket connection string
const url = 'ws://' + window.location.host + '/ws/ludo/game/' ;

// // Initialize WebSocket
const ws = new WebSocket(url);
const ludo = new Ludo();
ludo.listenDiceClick();
console.log('dice value = ' , ludo._diceValue);
console.log('dice 1value = ' , ludo.diceValue);


ws.onopen = function(){
    console.log('opened');
    ws.send("i send this message");
}

ws.onmessage = function(event){
    console.log(event);
    console.log(' : message received');
}

ws.onclose = function(event){
    console.log(event);
    console.log('closed ');
}

// Game board for maintaining the state of the game
// ludo.listenDiceClick();
// Function to send player presence to the server
// function sendPlayerPresence() {
    //     gameSocket.send(JSON.stringify({
        //         "event": "PLAYER_CONNECT",
        //         "message": ""
        //     }));
        // }
        
        // Function to handle WebSocket events
//         gameSocket.onopen = function open() {
//             // this.listenDiceClick();
//             // this.listenPieceClick();
//             // this.resetGame();
//             console.log('WebSockets connection created.');
//     // sendPlayerPresence();
// };

// gameSocket.onmessage = function (e) {
//     // On receiving a message from the server
//     const data = JSON.parse(e.data);
//     const event = data["event"];
//     const payload = data["payload"];

//     switch (event) {
//         case "UPDATE_BOARD":
//             // Update local game board with received data
//             ludo._state.
//             ludo.updateBoard(payload);
//             break;
//         case "END":
//             alert(payload.message);
//             reset();
//             break;
//         // Handle other events as needed
//     }
// };


// Function to reset the game board
// function reset() {
//     ludo.reset();
// }

// Function to make a move and send it to the server
// function makeMove(index) {
//     sendMove(index);
// }

// Call the connect function at the start
// gameSocket.onopen();

