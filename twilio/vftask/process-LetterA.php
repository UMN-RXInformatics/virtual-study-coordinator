<?php
session_start();
sleep(3);
// determine if the ID entered is valid

        if($_REQUEST['RecordingUrl']){
		$fname = $_REQUEST['CallSid']."_".$_REQUEST['From']."_".$_REQUEST['To']."_".date('Y-m-d')."_".date('H-i-s')."_A.wav";

                // good to go - we have a URL to get the recording from
                if(!copy($_REQUEST['RecordingUrl'],"/home/data/fitbit-vftask/".$fname)){
			echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
                	echo "<Response><Say>System error 5  has occured. Please report this to study personnel.</Say></Response>";
		}

                echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
                echo "<Response><Play>./audio/EnglishPromptStop.mp3</Play>\n";

                echo "<Gather timeout=\"10\"  numDigits=\"1\" action=\"./process-SecondDigit.php\"><Play>./audio/EnglishSemanticVFPrompt_v1.mp3</Play></Gather></Response>";
        }else{
                // loop
                echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
                echo "<Response><Say>Sorry, a server error has occured. Please report this to study personnel.</Say></Response>";
        }

?>

