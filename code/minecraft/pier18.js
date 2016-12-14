function sumDigits(number) {  var str = number.toString();  var sum = 0;
  for (var i = 0; i < str.length; i++) {    sum += parseInt(str.charAt(i), 10);  }
  return sum;}
for (i = 22808050; i < 30000000; i++) {    if (i.toString().indexOf("9") > -1 && i.toString().indexOf("9", i.toString().indexOf("9") + 1) > -1 && sumDigits(i) == 45) {    	console.log(i);    }}
