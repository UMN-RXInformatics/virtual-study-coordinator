<?php
session_start();
sleep(3);
// determine if the ID entered is valid

        if($_REQUEST['RecordingUrl']){
		$fname = $_REQUEST['CallSid']."_".$_REQUEST['From']."_".$_REQUEST['To']."_".date('Y-m-d')."_".date('H-i-s')."_Animals.wav";
                // good to go - we have a URL to get the recording from
                if(!copy($_REQUEST['RecordingUrl'],"/home/data/fitbit-vftask/".$fname)){
			echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
			echo "<Response><Say> System error 6 has occured. Please report this to study personnel. </Say></Response>";
		}

                echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
                echo "<Response><Play>./audio/EnglishPromptStop.mp3</Play>\n";
                echo "<Play>./audio/WrapupAlt1.mp3</Play></Response>\n";
        }else{
                // loop
                echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
                echo "<Response><Say>Sorry, a server error has occured. Please report this to study personnel.</Say></Response>";
        }

?>

