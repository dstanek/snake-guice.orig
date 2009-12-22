<html>
<head>
<title>The snake-web example</title>
</head>
<body>
<h1>The snake-web example</h1>
snake-web uses the following open source software:
<ul>
<li><a href="http://code.google.com/p/snake-guice/">snake-guice</a></li>
<li><a href="http://routes.groovie.org/">routes</a></li>
<li><a href="http://pythonpaste.org/webob/">webob</a></li>
</ul>

In this example app I have also used
<ul>
<li><a href="http://www.makotemplates.org/">mako</a></li>
</ul>

<h2>Want to see a form?</h2>
% if errors:
<ul>
% for err in errors.values():
<li>${err}</li>
% endfor
</ul>
% endif
<form action="/form" method="post">
% if 'name' in errors:
<font color="red">*</font>
% endif
Your name: <input type="text" name="name" value="${name}"/><br/>
% if 'email' in errors:
<font color="red">*</font>
% endif
Your email:<input type="text" name="email" value="${email}"/><br/>
Yes I have used dependency injection in past projects <input type="checkbox" name="past_experience"/><br/>
<input type="submit" value="Go"/>
</form>
</html>
