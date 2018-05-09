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
.border{
	padding: 70px;
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
 <col width="35%">
 <col width="30%">
 <col width="35%">
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
 <col width="20%">
 <col width="70%">
 <tr>
	<th>Edit</th>
	<th>Schedule</th>
	<th>Time</th>
 </tr>
 <?php
	include 'getSchedule.php';
 ?>
 <br>
 <button type="button" onclick="loadSchedule">Update Schedule</button>
 </td>
 <td>
 <div class="border">
 <form "method="post">
	Sunday <input type="checkbox" name="check[]" id="check" value="sunday"><br>
	Monday <input type="checkbox" name="check[]" id="check" value="monday"><br>
	Tuesday <input type="checkbox" name="check[]" id="check" value="tuesday"><br>
	Wednesday <input type="checkbox" name="check[]" id="check" value="wednesday"><br>
	Thursday <input type="checkbox" name="check[]" id="check" value="thursday"><br>
	Friday <input type="checkbox" name="check[]" id="check" value="friday"><br>
	Saturday <input type="checkbox" name="check[]" id="check" value="saturday"><br>
	<input type="time" name="Start" id="Start"><br>
    <input type="submit" name="insert" value="insert"><br>
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