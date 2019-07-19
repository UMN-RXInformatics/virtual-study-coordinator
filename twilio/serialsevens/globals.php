<?php
#if(!session_id()) session_start();
$lastCorrect = "866"; # last correct number entered
if(!isset($_SESSION['lastCorrect'])) {
    $_SESSION['lastCorrect'] = $lastCorrect;
}
?>
