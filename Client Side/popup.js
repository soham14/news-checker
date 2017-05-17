var message = document.querySelector("#message");
message.innerText = "NEWS CHECKER";

function setScores(serverResponse) {
	var posscore = document.querySelector("#pos-score");
	posscore.innerText = "POS: " + (Math.round(serverResponse.pos * 1000) / 1000);
	var neuscore = document.querySelector("#neu-score");
	neuscore.innerText = "NEU: " + (Math.round(serverResponse.neu * 1000) / 1000);
	var negscore = document.querySelector("#neg-score");
	negscore.innerText = "NEG: " + (Math.round(serverResponse.neg * 1000) / 1000);
	var comscore = document.querySelector("#com-score");
	comscore.innerText = "COM: " + (Math.round(serverResponse.compound * 1000) / 1000);
	var words = document.querySelector("#words");
	words.innerText = serverResponse.top_words.join(", ");
	var wordCount = document.querySelector("#word-count");
	wordCount.innerText = "Words: " + serverResponse.num_words;
	var sentCount = document.querySelector("#sent-count");
	sentCount.innerText = "Sentences: " + serverResponse.num_sentences;
	var time = document.querySelector("#time");
	time.innerText = "Time: " + serverResponse.mins + "m " + serverResponse.secs + "s";
}

chrome.tabs.query({"active": true, "currentWindow": true}, function(tab) {
    chrome.tabs.sendMessage(tab[0].id, {method: "getDOM"}, function(response) {

		var http = new XMLHttpRequest();
		http.open("POST", "http://soham.io/interface.php", false);
		http.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
		var conv = new String(response.b);
		http.send(JSON.stringify({text: conv}));

		console.log(http.responseText);
		serverResponse = JSON.parse(http.responseText);
        setScores(serverResponse);
    });
});
