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
    $result = $auth->register($username, $password);

    if ($result === true) {
        header('Location: ../login.php?registered=1');
        exit;
    } else {
        header('Location: ../register.php?error=1');
        exit;
    }
} else {
    header('Location: ../register.php');
    exit;
}