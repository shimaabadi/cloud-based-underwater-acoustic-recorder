<?php
	$ini = parse_ini_file("schedule.ini",true);
	if(isset($_POST['update'])){
		$box = $_POST['check'];
		$startTime = $_POST['start'];
		$stopTime = $_POST['stop'];
		
		if(!empty($box) && (strlen($startTime) > 0) && (strlen($stopTime) > 0)){
			foreach($box as $check){
				$newTime = "[".$startTime." ".$stopTime."]";
				if(strlen($ini['Schedule'][$check]) > 0){
					$newTime =  ",".$newTime;
				}
				$ini['Schedule'][$check].=$newTime;
			}
			
			if (!$handle = fopen("schedule.ini", 'w')) { 
				return false; 
			}
 
			$success = fwrite($handle, $ini);
			fclose($handle);
		} else {
			echo "Please fill out all fields";
		}
		
		
    }
?>