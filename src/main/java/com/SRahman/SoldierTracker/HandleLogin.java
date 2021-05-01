package com.SRahman.SoldierTracker;

import java.io.IOException;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

@WebServlet("/HandleLogin")
public class HandleLogin extends HttpServlet {
	private static final long serialVersionUID = 1L;

	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// No getting required, so just send to post
		doPost(request, response);
	}


	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		String username = request.getParameter("login");
		String password = request.getParameter("password");
		
		response.getWriter().write(username + " | " + password);
		
		// TODO: attempt connection to database
			// Check for username/password
				// set attributes of loggedin and username (Best approach for security?)
				// Check if attributes were set
					// create session and redirect to tracker.jsp (Check for session hijacking?)
				// not set
					// Send to index.jsp
			// send to index.jsp if login fails
		// send to index.jsp if can't connect to database
	}

}
