<?php
// Ensure a session is started when auth is included
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

require_once __DIR__ . '/database.php';

class Auth {
    private $conn;
    
    public function __construct($db) {
        $this->conn = $db;
    }
    
    // Register new user with SHA-256 hashed password
    public function register($username, $password) {
        // Hash the password using SHA-256
        $hashed_password = hash('sha256', $password);
        
        $query = "INSERT INTO users (username, password) VALUES (?, ?)";
        $stmt = $this->conn->prepare($query);
        
        if ($stmt->execute([$username, $hashed_password])) {
            return true;
        }
        return false;
    }
    
    // Login user with SHA-256 password verification
    public function login($username, $password) {
        $query = "SELECT id, username, password FROM users WHERE username = ?";
        $stmt = $this->conn->prepare($query);
        $stmt->execute([$username]);
        
        if ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
            $hashed_password = hash('sha256', $password);
            if ($hashed_password === $row['password']) {
                $_SESSION['user_id'] = $row['id'];
                $_SESSION['username'] = $row['username'];
                return true;
            }
        }
        return false;
    }
    
    // Logout user
    public function logout() {
        session_destroy();
        return true;
    }
    
    // Check if user is logged in
    public function isLoggedIn() {
        return isset($_SESSION['user_id']);
    }
}

// Encryption class for messages (Super Encryption: Caesar Cipher + AES)
class MessageEncryption {
    private $aes_key;
    private $caesar_shift;
    
    public function __construct($aes_key = 'your_secret_key_32_chars_long_123', $caesar_shift = 3) {
        $this->aes_key = $aes_key;
        $this->caesar_shift = $caesar_shift;
    }
    
    // Caesar Cipher encryption
    private function caesarEncrypt($text) {
        $result = '';
        for ($i = 0; $i < strlen($text); $i++) {
            $char = $text[$i];
            if (ctype_alpha($char)) {
                $ascii = ord(strtoupper($char));
                $ascii = (($ascii - 65 + $this->caesar_shift) % 26) + 65;
                $result .= chr($ascii);
            } else {
                $result .= $char;
            }
        }
        return $result;
    }
    
    // Caesar Cipher decryption
    private function caesarDecrypt($text) {
        $this->caesar_shift = 26 - $this->caesar_shift;
        $result = $this->caesarEncrypt($text);
        $this->caesar_shift = 26 - $this->caesar_shift;
        return $result;
    }
    
    // AES encryption
    private function aesEncrypt($text) {
        $iv = openssl_random_pseudo_bytes(openssl_cipher_iv_length('aes-256-cbc'));
        $encrypted = openssl_encrypt($text, 'aes-256-cbc', $this->aes_key, 0, $iv);
        return base64_encode($encrypted . '::' . $iv);
    }
    
    // AES decryption
    private function aesDecrypt($encrypted_text) {
        list($encrypted_data, $iv) = explode('::', base64_decode($encrypted_text), 2);
        return openssl_decrypt($encrypted_data, 'aes-256-cbc', $this->aes_key, 0, $iv);
    }
    
    // Super encryption (Caesar + AES)
    public function superEncrypt($text) {
        $caesar = $this->caesarEncrypt($text);
        return $this->aesEncrypt($caesar);
    }
    
    // Super decryption (AES + Caesar)
    public function superDecrypt($encrypted_text) {
        $aes = $this->aesDecrypt($encrypted_text);
        return $this->caesarDecrypt($aes);
    }
}

// File encryption class (RSA)
class FileEncryption {
    private $private_key;
    private $public_key;
    
    public function __construct() {
        // Generate RSA key pair
        $config = array(
            "private_key_bits" => 2048,
            "private_key_type" => OPENSSL_KEYTYPE_RSA,
        );
        $res = openssl_pkey_new($config);
        openssl_pkey_export($res, $this->private_key);
        $this->public_key = openssl_pkey_get_details($res)['key'];
    }
    
    public function encryptFile($file_content) {
        $encrypted = '';
        if (openssl_public_encrypt($file_content, $encrypted, $this->public_key)) {
            return base64_encode($encrypted);
        }
        return false;
    }
    
    public function decryptFile($encrypted_content) {
        $decrypted = '';
        if (openssl_private_decrypt(base64_decode($encrypted_content), $decrypted, $this->private_key)) {
            return $decrypted;
        }
        return false;
    }
}

// Image Steganography class
class ImageSteganography {
    public function embedMessage($image_path, $message) {
        $img = imagecreatefromjpeg($image_path);
        if (!$img) return false;
        
        $width = imagesx($img);
        $height = imagesy($img);
        
        $message_length = strlen($message);
        $message_bits = '';
        
        // Convert message to binary
        for ($i = 0; $i < $message_length; $i++) {
            $message_bits .= str_pad(decbin(ord($message[$i])), 8, '0', STR_PAD_LEFT);
        }
        
        $message_bits .= str_repeat('0', 8); // End marker
        
        $bit_count = 0;
        $message_length = strlen($message_bits);
        
        // Embed message bits in least significant bits of image pixels
        for ($y = 0; $y < $height && $bit_count < $message_length; $y++) {
            for ($x = 0; $x < $width && $bit_count < $message_length; $x++) {
                $rgb = imagecolorat($img, $x, $y);
                $r = ($rgb >> 16) & 0xFF;
                $g = ($rgb >> 8) & 0xFF;
                $b = $rgb & 0xFF;
                
                $r = $r & 0xFE | (int)$message_bits[$bit_count++];
                
                $new_color = imagecolorallocate($img, $r, $g, $b);
                imagesetpixel($img, $x, $y, $new_color);
            }
        }
        
        ob_start();
        imagejpeg($img);
        $stego_image = ob_get_contents();
        ob_end_clean();
        
        imagedestroy($img);
        return $stego_image;
    }
    
    public function extractMessage($stego_image_path) {
        $img = imagecreatefromjpeg($stego_image_path);
        if (!$img) return false;
        
        $width = imagesx($img);
        $height = imagesy($img);
        
        $message_bits = '';
        $message = '';
        
        // Extract message bits from least significant bits of image pixels
        for ($y = 0; $y < $height; $y++) {
            for ($x = 0; $x < $width; $x++) {
                $rgb = imagecolorat($img, $x, $y);
                $r = ($rgb >> 16) & 0xFF;
                
                $message_bits .= $r & 0x01;
                
                if (strlen($message_bits) >= 8) {
                    $ascii = bindec(substr($message_bits, 0, 8));
                    if ($ascii === 0) {
                        imagedestroy($img);
                        return $message;
                    }
                    $message .= chr($ascii);
                    $message_bits = substr($message_bits, 8);
                }
            }
        }
        
        imagedestroy($img);
        return $message;
    }
}
?>
