<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
    pageEncoding="ISO-8859-1"%>
<!DOCTYPE html>
<html lang="en">

<%
if (session.getAttribute("user") == null || session.getAttribute("user") == "") {
	response.sendRedirect("index.jsp");
	return;
}
%>

<head>
<meta charset="utf-8">

<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
<link href="./bootstrap/bootstrap.css" rel="stylesheet" />
<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.11.2/css/all.css" />
<link rel="stylesheet" href="./css/mdb.min.css" />
<link href="./css/admin.css" rel="stylesheet">
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<title>Tracker</title>
</head>
<body>

	<header>
		<nav id="sidebarMenu" class="collapse d-lg-block sidebar collapse">
			<div class="position-sticky">
				<div class="list-group list-group-flush mx-3 mt-4">
					<a href="#"
						class="list-group-item list-group-item-action py-2 ripple"
						aria-current="true">
						<i class="fas fa-server fa-fw me-3"><span>Dashboard</span></i>
					</a>
				</div>
			</div>
		</nav>
	</header>
	<script src="./bootstrap/bootstrap.js"></script>
	<script type="text/javascript" src="./js/mdb.min.js"></script>
</body>
</html>