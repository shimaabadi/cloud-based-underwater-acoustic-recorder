<?php
	$path = $_REQUEST["path"];
	if(is_dir($path)){
		if($dh = opendir($path)){
			while(($file = readdir($dh)) != false){
				echo '<input type="checkbox">'.$file.'<br/>';
			}
			closedir($dh);
		}
	}
	
?>