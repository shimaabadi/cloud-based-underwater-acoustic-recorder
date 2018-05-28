<?php
	$ini = parse_ini_file("schedule.ini",true);
	$days = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday'];
	$schedule = $ini['Schedule'];
	echo "<table border=1 width=100%>";
	echo "<col width='20%'>";
	echo "<col width='80%'>";
	echo "<tr><th>Schedule</th><th>Time</th></tr>";
	foreach($days as $day){
		echo "<tr>";
		echo "<td>".$day."</td>";
		if(strlen($schedule[$day]) > 0){
			$times = explode(',',$schedule[$day]);
			echo "<td>";
			$count = 0;
			foreach($times as $time){
				$finalTime = '';
				for($i = 1; $i < strlen($time) - 1;$i++){
					if($time[$i] == " "){
						$finalTime .= " - ";
					} else {
						$finalTime .= $time[$i];
					}
				}
				$formatTemp = explode('- ',$finalTime);
				$valId = $day.",".$formatTemp[0].$formatTemp[1];
				echo "<input type='checkbox' name='schedEdit[]' id='schedEdit' value='".$valId."'>".date('h:i a',strtotime($formatTemp[0]))." - ".date('h:i a',strtotime($formatTemp[1]))."<br>";
				$count++;
			}
			echo "</td>";
		}
		else {
			echo "<td></td>";
		}
		echo "</tr>";
	}
	echo "</table>";
	echo "<br>";
	echo "<input type='submit' id='RemoveRecording' name='RemoveRecording' value='Remove'>";
 ?> 