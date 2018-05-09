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
		else {
			echo "<td></td>";
		}
		echo "</tr>";
	}
	echo "</table>";
 ?> 