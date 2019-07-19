<?php
    if (!isset($_REQUEST['email'])) {
        echo "Must specify email address";
        die;
    }
     
    if (!isset($_REQUEST['RecordingUrl'])) {
        echo "Must specify recording url";
        die;
    }
     
    if (!isset($_REQUEST['TranscriptionStatus'])) {
        echo "Must specify transcription status";
        die;
    }
     
    if (strtolower($_REQUEST['TranscriptionStatus']) != "completed") {
        $subject = "Error transcribing voicemail from ${_REQUEST['Caller']}";
        $body = "New have a new voicemail from ${_REQUEST['Caller']}\n\n";
        $body .= "Click this link to listen to the message:\n";
        $body .= $_REQUEST['RecordingUrl'];
    } else {
        $subject = "New voicemail from ${_REQUEST['Caller']}";
        $body = "New have a new voicemail from ${_REQUEST['Caller']}\n\n";
        $body .= "Text of the Twilio transcribed voicemail:\n";
        $body .= $_REQUEST['TranscriptionText']."\n\n";
        $body .= "Click this link to listen to the message:\n";
        $body .= $_REQUEST['RecordingUrl'];
    }
     
    $headers = 'From: help@twilio.com' . "\r\n" .
        'Reply-To: help@twilio.com' . "\r\n" .
        'X-Mailer: Twilio';
    mail($_REQUEST['email'], $subject, $body, $headers);
?>
