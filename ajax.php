<?php
	if(isset($_POST['insert'])){
		$box = $_POST['check'];
		$sTime = $_POST['Start'];
		
		if(!empty($box)){
			foreach($box as $check){
				echo $check."<br>";
				echo $sTime."<br>";
			}
		}
    }
?>