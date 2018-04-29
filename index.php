<html>
<style>
.container {
	border:2px solid #ccc;
	width:100%;
	height:50%;
	overflow-y: scroll;
	}
</style>
<?php
	$maxcols = 5;
?>
 <head>
  <title>PHP Test</title>
  <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
 </head>
 <body>
 <table width=100% height=100%>
 <col width="40%">
 <col width="20%">
 <col width="40%">
 <tr>
 <td>
	<h1>Enter the Directory</h1></br>
	<input type="text" id="directory">
	<button type='button' onclick="test()">Click!</button>
	<div class="container" id="DirList"></div>
 </td>
 <td>
 <table border=1 width=100%>
 <col width="10%">
 <col width="80%">
 <col width="10%">
 <tr>
	<th>Edit</th>
	<th>Schedule</th>
	<th>Time</th>
 </tr>
 <?php
	$ini = parse_ini_file("schedule.ini",true);
	$wed = $ini['Schedule']['wednesday'];
	$wedTimes = str_split($wed,13);
	print_r($wedTimes);
	/*while($i != $maxcols){
		echo "<tr>";
		echo "<td><input type='checkbox' name='vehicle' value='$i'></td>";
		echo "<td>MWF</td>";
		echo "<td>12:00pm - 3:00pm</td>";
		echo "</tr>";
		$i++;
	}
	echo "</table>";
	*/
 ?> 
 </td>
 <td></td>
 </tr>
 <script>
 function test(){
	 var dir = document.getElementById("directory").value;
	 var xmlhttp = new XMLHttpRequest();
	 xmlhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                document.getElementById("DirList").innerHTML = this.responseText;
            }
        };
	 xmlhttp.open("GET","getFiles.php?path="+dir,true);
	 xmlhttp.send();
 }
 </script>
 </body>
</html>