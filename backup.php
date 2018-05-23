<!--
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
 <button type="button" onclick="loadSchedule">Load Schedule</button>
 <div id="Schedule"></div>
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
	$ini = parse_ini_file("schedule.ini",true);
	$days = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday'];
	$schedule = $ini['Schedule'];
	foreach($days as $day){
		echo "<tr>";
		echo "<td><input type='checkbox'></td>";
		echo "<td>".$day."</td>";
		if(strlen($schedule[$day]) > 0){
			$times = explode(',',$schedule[$day]);
			echo "<td>";
			foreach($times as $time){
				$finalTime = '';
				for($i = 1; $i < strlen($time) - 1;$i++){
					if($time[$i] == " "){
						$finalTime .= " - ";
					} else {
						$finalTime .= $time[$i];
					}
				}
				echo $finalTime."<br>";
			}
			echo "</td>";
		}
		echo "</tr>";
	}
	echo "</table>";
	/*
	while($i != $maxcols){
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
 -->