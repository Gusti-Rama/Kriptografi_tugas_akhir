<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cryptography Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <?php
    require_once 'php/auth.php';
    require_once 'php/database.php';
    
    $database = new Database();
    $db = $database->getConnection();
    $auth = new Auth($db);
    
    if (!$auth->isLoggedIn()) {
        header("Location: login.php");
        exit();
    }
    ?>
    
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="#">Cryptography App</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <a class="nav-link active" href="#" data-bs-toggle="tab" data-bs-target="#messages">Messages</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#" data-bs-toggle="tab" data-bs-target="#files">Files</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#" data-bs-toggle="tab" data-bs-target="#images">Images</a>
                    </li>
                </ul>
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <span class="nav-link">Welcome, <?php echo htmlspecialchars($_SESSION['username']); ?></span>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="logout.php">Logout</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        <div class="tab-content">
            <!-- Messages Tab -->
            <div class="tab-pane fade show active" id="messages">
                <div class="card">
                    <div class="card-header">
                        <h4>Encrypted Messages</h4>
                    </div>
                    <div class="card-body">
                        <form action="send_message.php" method="post">
                            <div class="mb-3">
                                <label for="recipient" class="form-label">Recipient Username</label>
                                <input type="text" class="form-control" id="recipient" name="recipient" required>
                            </div>
                            <div class="mb-3">
                                <label for="message" class="form-label">Message</label>
                                <textarea class="form-control" id="message" name="message" rows="3" required></textarea>
                            </div>
                            <button type="submit" class="btn btn-primary">Send Encrypted Message</button>
                        </form>
                        
                        <hr>
                        
                        <h5>Received Messages</h5>
                        <div class="messages-list">
                            <!-- Messages will be loaded here -->
                        </div>
                    </div>
                </div>
            </div>

            <!-- Files Tab -->
            <div class="tab-pane fade" id="files">
                <div class="card">
                    <div class="card-header">
                        <h4>Encrypted Files</h4>
                    </div>
                    <div class="card-body">
                        <form action="upload_file.php" method="post" enctype="multipart/form-data">
                            <div class="mb-3">
                                <label for="file" class="form-label">Select File</label>
                                <input type="file" class="form-control" id="file" name="file" required>
                            </div>
                            <button type="submit" class="btn btn-primary">Upload & Encrypt File</button>
                        </form>
                        
                        <hr>
                        
                        <h5>Your Encrypted Files</h5>
                        <div class="files-list">
                            <!-- Files will be loaded here -->
                        </div>
                    </div>
                </div>
            </div>

            <!-- Images Tab -->
            <div class="tab-pane fade" id="images">
                <div class="card">
                    <div class="card-header">
                        <h4>Steganography Images</h4>
                    </div>
                    <div class="card-body">
                        <form action="process_image.php" method="post" enctype="multipart/form-data">
                            <div class="mb-3">
                                <label for="image" class="form-label">Select Image</label>
                                <input type="file" class="form-control" id="image" name="image" accept="image/jpeg" required>
                            </div>
                            <div class="mb-3">
                                <label for="hidden_message" class="form-label">Hidden Message</label>
                                <textarea class="form-control" id="hidden_message" name="hidden_message" rows="3" required></textarea>
                            </div>
                            <button type="submit" class="btn btn-primary">Process Image</button>
                        </form>
                        
                        <hr>
                        
                        <h5>Your Processed Images</h5>
                        <div class="images-list">
                            <!-- Images will be loaded here -->
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
    // Add your JavaScript for handling forms and dynamic content loading here
    </script>
</body>
</html>
