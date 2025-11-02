<?php
session_start();
require_once __DIR__ . '/database.php';
require_once __DIR__ . '/auth.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'];
    $password = $_POST['password'];

    $database = new Database();
    $db = $database->getConnection();
    $auth = new Auth($db);
    $result = $auth->login($username, $password);

    if ($result === true) {
        $_SESSION['username'] = $username;
        header('Location: ../index.php');
        exit;
    } else {
        header('Location: ../login.php?error=1');
        exit;
    }
} else {
    header('Location: ../login.php');
    exit;
}