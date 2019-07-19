<?php
if(!session_id()) session_start(); // session start
include("globals.php");

    header("content-type: text/xml");
    echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";

    $fname = $_REQUEST['CallSid']."_".$_REQUEST['From']."_".$_REQUEST['To'].".dat";
    $fname = str_replace('+','',$fname);
    $response_file = fopen("/home/data/fitbit-serialsevens/$fname","a");
    

    #$_REQUEST['Digits'] = 879;
    #$_GET['initTime'] = 2505414900;

    if($_GET['Counter'] == 0)
    {
	fwrite($response_file,"***SESSION_START|".date("Y-m-d")."|".date("H:i:s")."|".round(microtime(true) * 1000)."|".$_REQUEST['From']."|".$_REQUEST['To']."\n");
	$_GET['initTime'] = microtime(true);
    }

    $duration = microtime(true) - $_GET['initTime']; 

    if ($_GET['Counter'] >  49 or $duration > 120 ){ 

        fwrite($response_file,"***SESSION_COMPLETE\n");
	echo "<Response> <Say voice='alice' language='en-US'> Time is up... Please stop... Thank you... Goodbye... </Say> </Response>";

    }elseif ($_GET['Counter'] == 0 and $_REQUEST['Digits'] == 879 or
	$_GET['Counter'] == 1 and $_REQUEST['Digits'] == 872 or
        $_GET['Counter'] == 2 and $_REQUEST['Digits'] == 865 or
        $_GET['Counter'] == 3 and $_REQUEST['Digits'] == 858 or
        $_GET['Counter'] == 4 and $_REQUEST['Digits'] == 851 or
        $_GET['Counter'] == 5 and $_REQUEST['Digits'] == 844 or
        $_GET['Counter'] == 6 and $_REQUEST['Digits'] == 837 or
        $_GET['Counter'] == 7 and $_REQUEST['Digits'] == 830 or
        $_GET['Counter'] == 8 and $_REQUEST['Digits'] == 823 or
        $_GET['Counter'] == 9 and $_REQUEST['Digits'] == 816 or
        $_GET['Counter'] == 10 and $_REQUEST['Digits'] == 809 or
        $_GET['Counter'] == 11 and $_REQUEST['Digits'] == 802 or
        $_GET['Counter'] == 12 and $_REQUEST['Digits'] == 795 or
        $_GET['Counter'] == 13 and $_REQUEST['Digits'] == 788 or
        $_GET['Counter'] == 14 and $_REQUEST['Digits'] == 781 or
        $_GET['Counter'] == 15 and $_REQUEST['Digits'] == 774 or
        $_GET['Counter'] == 16 and $_REQUEST['Digits'] == 767 or
        $_GET['Counter'] == 17 and $_REQUEST['Digits'] == 760 or
        $_GET['Counter'] == 18 and $_REQUEST['Digits'] == 753 or
        $_GET['Counter'] == 19 and $_REQUEST['Digits'] == 746 or
        $_GET['Counter'] == 20 and $_REQUEST['Digits'] == 739 or
        $_GET['Counter'] == 21 and $_REQUEST['Digits'] == 732 or
        $_GET['Counter'] == 22 and $_REQUEST['Digits'] == 725 or
        $_GET['Counter'] == 23 and $_REQUEST['Digits'] == 718 or
        $_GET['Counter'] == 24 and $_REQUEST['Digits'] == 711 or
        $_GET['Counter'] == 25 and $_REQUEST['Digits'] == 697 or
        $_GET['Counter'] == 26 and $_REQUEST['Digits'] == 690 or
        $_GET['Counter'] == 27 and $_REQUEST['Digits'] == 683 or
        $_GET['Counter'] == 28 and $_REQUEST['Digits'] == 676 or
        $_GET['Counter'] == 29 and $_REQUEST['Digits'] == 669 or
        $_GET['Counter'] == 30 and $_REQUEST['Digits'] == 662 or
        $_GET['Counter'] == 31 and $_REQUEST['Digits'] == 655 or
        $_GET['Counter'] == 32 and $_REQUEST['Digits'] == 648 or
        $_GET['Counter'] == 33 and $_REQUEST['Digits'] == 641 or
        $_GET['Counter'] == 34 and $_REQUEST['Digits'] == 634 or
        $_GET['Counter'] == 35 and $_REQUEST['Digits'] == 627 or
        $_GET['Counter'] == 36 and $_REQUEST['Digits'] == 620 or
        $_GET['Counter'] == 37 and $_REQUEST['Digits'] == 613 or
        $_GET['Counter'] == 38 and $_REQUEST['Digits'] == 606 or
        $_GET['Counter'] == 39 and $_REQUEST['Digits'] == 599 or
        $_GET['Counter'] == 40 and $_REQUEST['Digits'] == 592 or
        $_GET['Counter'] == 41 and $_REQUEST['Digits'] == 585 or
        $_GET['Counter'] == 42 and $_REQUEST['Digits'] == 578 or
        $_GET['Counter'] == 43 and $_REQUEST['Digits'] == 571 or
        $_GET['Counter'] == 44 and $_REQUEST['Digits'] == 564 or
        $_GET['Counter'] == 45 and $_REQUEST['Digits'] == 557 or
        $_GET['Counter'] == 46 and $_REQUEST['Digits'] == 550 or
        $_GET['Counter'] == 47 and $_REQUEST['Digits'] == 543 or
        $_GET['Counter'] == 48 and $_REQUEST['Digits'] == 536 or
        $_GET['Counter'] == 49 and $_REQUEST['Digits'] == 529 or
        $_GET['Counter'] == 50 and $_REQUEST['Digits'] == 522)
    {
	
	$_SESSION['lastCorrect'] = $_REQUEST['Digits'];
	fwrite($response_file,round(microtime(true) * 1000)."|".$_GET['Counter']."|".$_REQUEST['Digits']."|C\n");

	echo "<Response> 
                <Gather input='dtmf' timeout='10' numDigits='3' action='handleKey.php?Counter=" . ++$_GET['Counter'] ."&amp;initTime=".$_GET['initTime']."'> 
                <Say voice='alice' language='en-US'> ". $_REQUEST['Digits'] ." Is correct. You have 10 seconds to enter the next answer. </Say>
                </Gather>
                <Gather input='dtmf' timeout='10' numDigits='3' action='handleKey.php?Counter=" . $_GET['Counter'] ."&amp;initTime=".$_GET['initTime']."'> 
                <Say voice='alice' language='en-US'> No input detected. You have 10 seconds to enter the next answer. Last correct number was ". $_SESSION['lastCorrect'] ." </Say>
                </Gather> 
		</Response>";
    }
    else
    {

	fwrite($response_file,round(microtime(true) * 1000)."|".$_GET['Counter']."|".$_REQUEST['Digits']."|I\n");
	echo "<Response> 
		<Gather input='dtmf' timeout='10' numDigits='3' action='handleKey.php?Counter=" . $_GET['Counter'] ."&amp;initTime=". $_GET['initTime'] ."&amp;lastCorrect=". $lastCorrect  ."'> 
		<Say voice='alice' language='en-US'> ". $_REQUEST['Digits'] ." Is not correct. Please try again. Last correct number was ". $_SESSION['lastCorrect'] ." </Say>
		</Gather> 
                <Gather input='dtmf' timeout='10' numDigits='3' action='handleKey.php?Counter=" . $_GET['Counter'] ."&amp;initTime=".$_GET['initTime']."'> 
                <Say voice='alice' language='en-US'> No input detected. You have 10 seconds to enter the next answer. Last correct number was ". $_SESSION['lastCorrect'] ." </Say>
                </Gather> 
		</Response>";
    }
    fclose($response_file);

?>
