<?php

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
    <Say>Welcome to VFMeter. A system for automated verbal fluency assessment.</Say>
    <Play>./RecordingNotice.mp3</Play>
    <Play>./IDPrompt.mp3</Play>

</Response>

