function barChart(dateValue, modelKey, modelValue, wordValue) {
	document.getElementById("dateValue").innerHTML = "<b>" + dateValue[0] + " ~ " + dateValue[1] + "</b>";

	console.log(wordValue.length);

	for(i=0; i<wordValue.length; i++) {		
		document.getElementById("wordValue").innerHTML = "<b>" + wordValue[i] + "</b>&nbsp";
	}
	
	new Chart(document.getElementById("canvas"), {
    type: 'horizontalBar',
    data: {
        labels: modelKey,
        datasets: [{
            
            data: modelValue,
            backgroundColor: [
		      'rgba(255, 99, 132, 0.2)',
		      'rgba(255, 159, 64, 0.2)',
		      'rgba(255, 205, 86, 0.2)',
		      'rgba(75, 192, 192, 0.2)',
		      'rgba(54, 162, 235, 0.2)',
		      'rgba(153, 102, 255, 0.2)',
		      'rgba(201, 203, 207, 0.2)'],
		    borderColor: [
		      'rgb(255, 99, 132)',
		      'rgb(255, 159, 64)',
		      'rgb(255, 205, 86)',
		      'rgb(75, 192, 192)',
		      'rgb(54, 162, 235)',
		      'rgb(153, 102, 255)',
		      'rgb(201, 203, 207)']
        }]
    }
});	
}