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
			
		} else {
			echo "Please fill out all fields";
		}
    }
	header('Location: index.php');
?>