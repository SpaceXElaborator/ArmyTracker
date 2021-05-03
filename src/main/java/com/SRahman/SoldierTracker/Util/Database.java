package com.SRahman.SoldierTracker.Util;

import java.io.File;
import java.io.IOException;
import java.security.NoSuchAlgorithmException;
import java.security.spec.InvalidKeySpecException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

import javax.crypto.SecretKey;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.PBEKeySpec;

import org.apache.commons.codec.binary.Hex;

public class Database {
	
	public static void checkSetup() throws ClassNotFoundException, SQLException {
		
		File f = new File(System.getProperty("user.home"), "LTProject");
		
		if(!f.exists()) {
			f.mkdir();
			File database = new File(f, "SqliteLTDatabase.db");
			try {
				database.createNewFile();
			} catch (IOException e) {
				e.printStackTrace();
			}
			Class.forName("org.sqlite.JDBC");
			Connection conn = DriverManager.getConnection("jdbc:sqlite:" + System.getProperty("user.home") + "\\LTProject\\SqliteLTDatabase.db");
			PreparedStatement stat = conn.prepareStatement("CREATE TABLE IF NOT EXISTS users (id integer PRIMARY KEY, username varchar(255), password longtext);");
			stat.execute();
			
			// Check if the Admin user is present.
			PreparedStatement checkAdmin = conn.prepareStatement("SELECT * FROM users WHERE username = ?");
			checkAdmin.setString(1, "admin");
			ResultSet rs = checkAdmin.executeQuery();
			if(!rs.next()) {
				// If there is no admin, add the user with a default password
				String username = "admin";
				String password = "";
				try {
					password = hashPassword("AdminTestPass");
				} catch (InvalidKeySpecException | NoSuchAlgorithmException e) {
					e.printStackTrace();
				}
				PreparedStatement addAdmin = conn.prepareStatement("INSERT INTO users (username, password) values (?, ?)");
				addAdmin.setString(1, username);
				addAdmin.setString(2, password);
				addAdmin.executeUpdate();
			}
			conn.close();
		}
	}
	
	// Create hashed password with the given string and added salt.
	private static String hashPassword(String pass) throws InvalidKeySpecException, NoSuchAlgorithmException {
		SecretKeyFactory skf = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA512");
		PBEKeySpec spec = new PBEKeySpec(pass.toCharArray(), "5I4a2NZ6wIQHlwah".getBytes(), 10000, 512);
		SecretKey key = skf.generateSecret(spec);
		byte[] res = key.getEncoded();
		return Hex.encodeHexString(res);
	}
	
	public static void addUser(String username, String password) throws ClassNotFoundException, SQLException, InvalidKeySpecException, NoSuchAlgorithmException {
		checkSetup();
		Class.forName("org.sqlite.JDBC");
		Connection conn = DriverManager.getConnection("jdbc:sqlite:" + System.getProperty("user.home") + "\\LTProject\\SqliteLTDatabase.db");
		PreparedStatement stat = conn.prepareStatement("INSERT INTO users(username, password) VALUES (?,?)");
		stat.setString(1, username);
		stat.setString(2, hashPassword(password));
		stat.executeUpdate();
		conn.close();
	}
	
	public static boolean checkLogin(String username, String password) throws ClassNotFoundException, SQLException {
		checkSetup();
		Class.forName("org.sqlite.JDBC");
		Connection conn = DriverManager.getConnection("jdbc:sqlite:" + System.getProperty("user.home") + "\\LTProject\\SqliteLTDatabase.db");
		PreparedStatement stat = conn.prepareStatement("SELECT * FROM users WHERE username = ?");
		stat.setString(1, username);
		ResultSet result = stat.executeQuery();
		if(result.next()) {
			String pass = result.getString("password");
			try {
				if(pass.equals(hashPassword(password))) {
					conn.close();
					return true;
				}
			} catch (InvalidKeySpecException | NoSuchAlgorithmException e) {
				e.printStackTrace();
			}
		}
		conn.close();
		return false;
	}
	
}