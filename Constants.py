BASE = 0

STARTOFFSET = 5
BASEOFFSET = 17
BOARDLENGTH = BASEOFFSET*4
HOMEPATHLENGTH = 8
HOME = BOARDLENGTH + HOMEPATHLENGTH

SAFE_POSITIONS = [0, 5, 12, 17, 22, 29, 34, 39, 46, 51, 56, 63]

RED = 'RED'
BLUE = 'BLUE'
YELLOW = 'YELLOW'
GREEN = 'GREEN'
COLORS = [RED, BLUE, YELLOW, GREEN]

START_ROLL = 5

# Move Options
START_PIECE = 'START_PIECE'
GET_SAFE = 'GET_SAFE'
GET_HOME = 'GET_HOME'
MAKE_KILL = 'MAKE_KILL'
MAKE_BLOCKADE = 'MAKE_BLOCKADE'
MOVE_FORWARD = 'MOVE_FORWARD'

# STRATEGIES
STRATEGY_KILL = 'STRATEGY_KILL'
STRATEGY_PLAY_IT_SAFE = 'STRATEGY_PLAY_IT_SAFE'
STRATEGY_SPEED = 'STRATEGY_SPEED'

STRATEGIES = {
	STRATEGY_KILL: {
	    MAKE_KILL: 2,
	    GET_HOME: 1
	},
	STRATEGY_PLAY_IT_SAFE: {
	    GET_SAFE: 3,
	    GET_HOME: 2,
	    MOVE_FORWARD: 1,
	},
	STRATEGY_SPEED: {
	    START_PIECE: 3,
	    MOVE_FORWARD: 2,
	    GET_HOME: 1,
	}
}