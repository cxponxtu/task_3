
<!DOCTYPE HTML>
<html>

<head>
<title>User Login</title>
<link rel="stylesheet" type="text/css" href="css/index.css">
</head>

<body >
<form action="index.php" method="post" class="form">
    <h2>SQL Injection</h2>
    <label for="username">Username</label>
    <input type="text" id="username" name="user"><br>
    <label for="password">Password</label>
    <input type="password" id="pass" name="pass"><br>   
    <input type="submit" name="submit" value="Log In" class="button"> 
    <div id="response">
<?php 

session_start();
$duser='root';
$dpass='1234';
$dhost='127.0.0.1';
$dbname="sqli";

$conn = mysqli_connect($dhost,$duser,$dpass,$dbname);

if(!empty($_POST["submit"]))
{
    $_SESSION["status"] = 0;
    $user = $_POST["user"];     
    $pass = $_POST["pass"];
    if(!empty($user) && !empty($pass))
    {
        $sql = "SELECT name FROM users WHERE uname = '$user' AND pass = '$pass'";
        $result = mysqli_query($conn,$sql);
        if(mysqli_num_rows($result) > 0)
        {
            $_SESSION["user"] = $user;
            $_SESSION["name"] = mysqli_fetch_assoc($result)["name"];
            $_SESSION["status"] = 1;
            header("Location: home.php");
        }
        else
        {
            echo "Incorrect Username/Password";
        }        
    }

    else
    {
        echo "Enter valid Username/Password";
    }
}

mysqli_close($conn);
?>
</div>
</form>

</body>
</html>
