<html>
<head>
<title>I hope you enjoy snake-guice</title>
</head>
<body>
<h1>How was your cup of snake-guice?</h1>
Hello ${name},<br/><br/>
Thank you for taking a look at the snake-web example that's bundled with
<a href="http://code.google.com/p/snake-guice/">snake-guice</a>!
% if past_experience:
Since you know why DI is good what's holding you back? Please consider using
snake-guice.
% else:
DI is good and there's a good change that you should be using it.
% endif
</body>
</html>
