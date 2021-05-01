<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
	pageEncoding="ISO-8859-1"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="ISO-8859-1">
<meta name="viewport"
	content="width=device-width, initial-scale=1, shrink-to-fit=no">
<link href="./bootstrap/bootstrap.css" rel="stylesheet">
<link href="./css/main.css" rel="stylesheet">
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<title>Soldier Information Sheet - Login</title>
</head>
<body>

	<div class="container-fluid">
		<div id="login_form" class="row main-content bg-success text-center">
			<div class="col-md-4 text-center icorp-info">
				<span><img src="./textures/icorp.png" width="100" height="100"></span>
				<h4>ICorp Soldier Portal</h4>
			</div>
			<div class="col-md-8 col-xs-12 col-sm-12 login-form">
				<div class="container-fluid">
					<div class="row">
						<h2>Log In</h2>
					</div>
					<div class="row">
						<form action="HandleLogin" method="POST" class="form-group">
							<div class="row">
								<input type="text" name="login" id="login" class="form-input" placeholder="Username">
							</div>
							<div class="row">
								<input type="password" name="password" id="password" class="form-input" placeholder="Password">
							</div>
							<div class="row justify-content-center">
								<input type="submit" value="submit" class="btn">
							</div>
						</form>
					</div>
				</div>
			</div>
		</div>
	</div>

</body>
</html>