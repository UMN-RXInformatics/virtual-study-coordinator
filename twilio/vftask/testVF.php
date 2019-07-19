<?php

use Twilio\Twiml;
    require 'twilio-php/Services/Twilio.php';

    header("content-type: text/xml");

   $_REQUEST['email'] = "spakh001@gmail.com";

   if (!isset($_REQUEST['email'])) {
        echo "Must specify email address";
        die;
    }
    echo('<?xml version="1.0" encoding="UTF-8"?>');

?>

<Response>
    <Pause length="1"/>
    <Say>Welcome to automated verbal fluency assessment.</Say>
    <Say>This call will be audio recorded for research purposes.</Say> 
    <Gather timeout="10" finishOnKey="#" action="./process-ID.php">
	<Say>Please enter your study number followed by the pound key.</Say>
    </Gather>


    
</Response>

