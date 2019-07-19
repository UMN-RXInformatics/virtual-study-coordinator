<?php
session_start();

// determine if the ID entered is valid

	if($_REQUEST['Digits'] = "1234"){

                $_SESSION['ptnum'] = $_REQUEST['Digits'];
		echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";

		echo "<Response><Say> Thank you. Let's begin the assessment. </Say>\n";

		echo "<Play>./audio/Intromult.mp3</Play>\n";

                echo "<Gather timeout=\"10\"  numDigits=\"1\" action=\"./process-FirstDigit.php\"><Play>./audio/EnglishPhonemicVFPrompt_v1.mp3</Play></Gather></Response>";

	}else{
		echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
		echo "<Response><Say>The study number " . $_REQUEST['Digits'] . " is not valid. Please check your study number and try again.</Say></Response>\n";
		echo "<Hangup/>\n";
	}

?>
