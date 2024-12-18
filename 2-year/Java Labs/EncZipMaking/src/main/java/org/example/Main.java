package org.example;

import javax.crypto.*;
import javax.crypto.spec.SecretKeySpec;
import javax.crypto.spec.IvParameterSpec;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.Base64;

public class Main {

    private static final String ALGORITHM = "AES";
    private static final String SECRET_KEY = "1234567890123456"; // 16 байт для AES-128

    public static void main(String[] args) {
        try {
            // Генерация ключа (или используйте заранее сгенерированный)
            SecretKey secretKey = new SecretKeySpec(SECRET_KEY.getBytes(), ALGORITHM);

            // Шифрование данных и запись в файл
            String originalText = "Hello, World! This is a secret message.";
            String encryptedFilePath = "encrypted.txt";
            encryptToFile(originalText, secretKey, encryptedFilePath);

            // Расшифровка данных из файла
            String decryptedText = decryptFromFile(secretKey, encryptedFilePath);
            System.out.println("Decrypted Text: " + decryptedText);
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }

    private static void encryptToFile(String data, SecretKey secretKey, String filePath) throws Exception {
        Cipher cipher = Cipher.getInstance(ALGORITHM);
        cipher.init(Cipher.ENCRYPT_MODE, secretKey);

        try (OutputStream outputStream = new FileOutputStream(filePath);
             CipherOutputStream cipherOutputStream = new CipherOutputStream(outputStream, cipher)) {
            cipherOutputStream.write(data.getBytes());
        }
    }

    private static String decryptFromFile(SecretKey secretKey, String filePath) throws Exception {
        Cipher cipher = Cipher.getInstance(ALGORITHM);
        cipher.init(Cipher.DECRYPT_MODE, secretKey);

        try (InputStream inputStream = new FileInputStream(filePath);
             CipherInputStream cipherInputStream = new CipherInputStream(inputStream, cipher)) {
            StringBuilder decryptedText = new StringBuilder();
            int byteRead;
            while ((byteRead = cipherInputStream.read()) != -1) {
                decryptedText.append((char) byteRead);
            }
            return decryptedText.toString();
        }
    }
}