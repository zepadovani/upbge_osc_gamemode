
// 1. Run a routine to move the cube:
(
~n = NetAddr("127.0.0.1", 13333);//sending port

~t1 = Routine({
	var timewait, endOSC;
	inf.do({
		endOSC = "/move";
		timewait = rrand(0.1,0.5);
		~n.sendMsg(endOSC, rrand(-0.2,0.2), rrand(-0.2,0.2), 0);
		timewait.wait;
	});
}).play();

)

// 2. Stop the routine
~t1.stop();

// 3. Stop the server and quit the game
~n.sendMsg("/quit",1);