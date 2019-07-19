<?php
    header("content-type: text/xml");
    echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
?>

<Response>

	<Say voice="alice" language="en-US"> This call will be used for research. </Say>
	<Play>./audio/Intromult.mp3</Play>
	<Gather timeout="10"  numDigits="1" action="./process-FirstDigit.php">
		<Play>./audio/EnglishPhonemicVFPrompt_v1.mp3</Play>
	</Gather>

</Response>
