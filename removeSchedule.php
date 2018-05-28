<?php
	$ini = parse_ini_file("schedule.ini",true);
	$schedule = $ini['Schedule'];
	if(isset($_POST['RemoveRecording'])){
		$remItem = $_POST['schedEdit'];
		foreach($remItem as $element){
			$elementArr = explode(',',$element);
			$timeSplit = explode(',',$schedule[$elementArr[0]]);
			$search = "[".$elementArr[1]."]";
			$idx = array_search($search,$timeSplit);
			unset($timeSplit[$idx]);
			$newString = "";
			foreach($timeSplit as $val){
				$newString .= $val.",";
			}
			$newString = substr($newString,0,strlen($newString)-1);
			$schedule[$elementArr[0]] = $newString;
		}
		$ini['Schedule'] = $schedule;
		
		$content = "";
			foreach($ini as $key => $val){
				$content.="[".$key."]\n";
				if(is_array($val)){
					foreach($val as $item => $val){
						$content.=$item." = ".$val."\n";
					}
				}
			}
			
			$sched = fopen("schedule.ini","w");
			fwrite($sched,$content);
			fclose($sched);
	}
	header('Location: index.php');
?>