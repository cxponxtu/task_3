<?php

session_start();
if ($_SESSION["status"] != 1) 
{
    header("Location: index.php");
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>SQLi</title>
    <link rel="stylesheet" type="text/css" href="css/home.css">
</head>
<body>
<header>
    <form action="home.php" method="post" id="head">
        <div id="left">SQL Injection</div>
        <div id="right">
            <?php
                echo "<font id=\"username\">{$_SESSION["name"]}</font>";
                if (!empty($_POST["nav"]))
                {
                    if($_POST["nav"] == "Log Out")
                    {
                        session_abort();
                        header("Location: index.php");
                    } 
                }        
            ?>
            <input class="header_button" type="submit" name="nav" value="Log Out">
            </div>      
     </form>
</header>
    <?php
    echo "<h2>Hello {$_SESSION["name"]}</h2>";
?>
<div style="display: flex; justify-content: center; align-items: center;">
    <img src="css/welcome.webp" >
</div>
</body>
</html>