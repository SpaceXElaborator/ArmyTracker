package com.SRahman.SoldierTracker;

import java.io.IOException;
import java.sql.SQLException;

import com.SRahman.SoldierTracker.Util.Database;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;

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
		
		try {
			if(Database.checkLogin(username, password)) {
				HttpSession sess = request.getSession();
				sess.setAttribute("user", username);
				sess.setMaxInactiveInterval(30*60);
				if(sess.getAttribute("user") != null || sess.getAttribute("user") != "") {
					response.sendRedirect("tracker.jsp");
					response.getWriter().write("Will Send to Tracker webpage");
					return;
				} else {
					response.sendRedirect("index.jsp");
					return;
				}
			} else {
				response.sendRedirect("index.jsp");
				return;
			}
		} catch (ClassNotFoundException | SQLException e) {
			e.printStackTrace();
			response.sendRedirect("index.jsp");
			return;
		}
	}

}
