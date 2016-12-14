// Script to calculate distances for pier 16// Best run with `nodejs calcPier16.js > pier16.txt`// Also possible to paste into JS console of browser
function sumDigits(number) {  var str = number.toString();  var sum = 0;
  for (var i = 0; i < str.length; i++) {    sum += parseInt(str.charAt(i), 10);  }
  return sum;}
for (i = 20270902; i < 30000000; i++) {    if (i.toString().indexOf("00") > -1 && sumDigits(i) == 9) {    	console.log(i);    }}
