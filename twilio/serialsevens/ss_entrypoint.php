<?php
    header("content-type: text/xml");
    echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
?>

<Response>
    <Say voice="alice" language="en-US"> This call will be used for research. </Say>    
    <Say voice="alice" language="en-US"> This system will test your math skills. </Say>
    <Pause length="1"/>
    <Say voice="alice" language="en-US"> Your task is to keep subtracting number seven from nine hundred for two minutes and enter your answers using the keypad after the prompt.</Say>
    <Pause length="1"/>
    <Say voice="alice" language="en-US"> You will have 10 seconds to enter each answer. </Say>
    <Pause length="1"/>
    <Say voice="alice" language="en-US"> To get you started, the first answer is eight ninety three. </Say>
    <Pause length="1"/>
    <Say voice="alice" language="en-US"> The second answer is eight eighty six. </Say>
    <Pause length="1"/>

    <Gather input="dtmf" timeout="10" numDigits="3" action="handleKey.php?Counter=0">
	    <Say voice="alice" language="en-US"> You have 10 seconds to enter the next answer on your keypad. </Say>
    </Gather>
    <Gather input="dtmf" timeout="10" numDigits="3" action="handleKey.php?Counter=0">
            <Say voice="alice" language="en-US"> No input detected. You have 10 seconds to enter the next answer on your keypad. </Say>
    </Gather>
    <Gather input="dtmf" timeout="10" numDigits="3" action="handleKey.php?Counter=0">
            <Say voice="alice" language="en-US"> No input detected. This is the last attempt. You have 10 seconds to enter the next answer on your keypad. </Say>
    </Gather>
    <Say voice="alice" language="en-US"> Sorry, the system did not detect any input from you and cannot continue. Good bye! </Say>
    

</Response>

