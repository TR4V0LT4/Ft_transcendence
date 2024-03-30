import { Ludo } from './ludo/ludo.js' ;
import { BASE_POSITIONS, HOME_ENTRANCE, HOME_POSITIONS, PLAYERS, SAFE_POSITIONS, START_POSITIONS, STATE, TURNING_POINTS } from './ludo/constants.js';
let gamestart = new Audio('/static/audio/gamestart.mp3');
gamestart.play(); 
const ludo = new Ludo();


