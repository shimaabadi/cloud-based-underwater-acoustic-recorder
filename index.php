<html>
<?php
/*
	To add:
	Remove time
	Add record time
	View last file uploaded
*/
?>
<style>
.container {
	border:2px solid #ccc;
	width:100%;
	height:50%;
	overflow-y: scroll;
	}
.padding{
	padding: 70px;
}
td.outer-table { 
    padding: 10px;
}
tr.cell{
	vertical-align: top;
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
 <table width=100% height=500px>
 <col width="35%">
 <col width="30%">
 <col width="35%">
 <tr class="cell" height="100px">
	<td>
		<h1>Enter the Directory</h1></br>
		<input type="text" id="directory">
		<button type='button' onclick="test()">Click!</button>
	</td>
	<td></td>
	<td></td>
 </tr>
 <tr class="cell">
 <td class="outer-table">
	<div class="container" id="DirList"></div>
 </td>
 <td>
 <form action="removeSchedule.php" method="post">
 <?php
	include 'getSchedule.php';
 ?>
 </form>
 </td>
 <td>
 <div class="padding">
 <form action="writeSchedule.php" method="post">
	<input type="time" name="start" id="start"> to <input type="time" name="stop" id="stop">
	<input type="submit" name="update" value="Update"><br>
	<table>
	<tr>
		<td><input type="checkbox" name="check[]" id="check" value="monday">Monday</td>
		<td><input type="checkbox" name="check[]" id="check" value="tuesday">Tuesday</td>
	</tr>
	<tr>
		<td><input type="checkbox" name="check[]" id="check" value="wednesday">Wednesday</td>
		<td><input type="checkbox" name="check[]" id="check" value="thursday">Thursday</td>
	</tr>
	<tr>
		<td><input type="checkbox" name="check[]" id="check" value="friday">Friday</td>
		<td><input type="checkbox" name="check[]" id="check" value="saturday">Saturday</td>
	</tr>
	<tr>
		<td><input type="checkbox" name="check[]" id="check" value="sunday">Sunday</td>
		<td></td>
	</tr>
	</table>
 </form>
 </div>
 </td>
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