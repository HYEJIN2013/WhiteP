<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf8" />
<title>TheVille Server Information</title>
<link rel="stylesheet" type="text/css" href="serverlist.css" />
<script src="serverlist.js"></script>
</head>
<body>

<body link=#ffffff vlink=#ffffff>
<table width=100%><tr><td align=center>
<table border=0 class='servers' width=100%>
<?php

require(__DIR__ . '/mcstat/mcstat.php');

// Settings
// This array has 3 parts - the host, port and description
$servers = array(
	array("66.240.202.11", 25565, "V - Minecraft")
);

foreach ($servers as $server) {
	# Grab the stats
	$query = new MinecraftStatus($server[0], $server[1]);
	$stats = $query->ping(false);

	# Generate the tooltip
	$current_players = "";
	foreach ($stats['players'] as $player) {
		$current_players .= '<tr><td class=players>' . rawurlencode($player) . '</td></tr>';
	}

	echo <<<EOF
<tr>
	<td valign=absmiddle class='servers' align=center width=36>
		<img src='http://www.theville.org/lgsln/icons/minecraft.png'>
	</td>
	<td class='servers' align=left>TheVille.org {$server[2]}<br>
		<span class=servername>{$server[0]}:{$server[1]}</span>
	</td>
	<td class='servers' align=right>{$stats['player_count']}/{$stats['player_max']}</td>
	<td class='servers' align=left>
		<a href='#' class="tip" onmouseover="tooltip('<span class=servertitle>Current Players</span><br><hr><table border=0 cellpadding=2 cellspacing=2 width=100%>$current_players</table>');"onmouseout="tipexit();">
EOF;

	// The first light has a different image, so we handle that first
	$url = 'http://www.theville.org/lgsln/other/first_slot.gif';
	if ($stats['player_count'] > 0) {
		$url = 'http://www.theville.org/lgsln/other/first_player.gif';
	}
	echo "<img title='Dogs Lights' class='si_players' src='$url'>";

	// Loop through the number of players, updating the lights
	for ($i = 1; $i < $stats['player_max']; $i++) {
		$url = 'http://www.theville.org/lgsln/other/mid_slot.gif';
		if ($i < $stats['player_count']) {
			$url = 'http://www.theville.org/lgsln/other/mid_player.gif';
		}
		echo "<img src='$url'>";
	}

	echo "</a></td></tr>";
}

?>
</table>
</td></tr></table>
</body>
</html>
