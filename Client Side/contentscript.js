var html = document.all[0];

chrome.runtime.onMessage.addListener(
	function(request, sender, sendResponse) {
		sendResponse({"b": html.innerText});
	});