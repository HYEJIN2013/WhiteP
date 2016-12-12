<?php
$count = 0;
$thelist[500];
 if ($handle = opendir('.')) {
   while (false !== ($file = readdir($handle)))
      {		#IndexIgnore temp-files,hidden-files 
          if ($file != "." && $file != ".."  && (strpos($file,'~') == 0) && !(strpos($file,'.') === 0) )
	  {	$count++;
          	$thelist[$count] .= '<a href="'.$file.'">'.$file.'</a>';
          }
       }
  closedir($handle);
  }       
?>

<script type="text/javascript">
if(screen.width <= 699){
    <?php $screen = 'mobile';?>
}else{
    <?php $screen = 'default';?>
}
</script>


<!DOCTYPE html>
<html>

<head>
<title>HomeSever</title>
<link href="stylesheet.css" rel="stylesheet" type="text/css" media="all" />
</head>

<body>
<div bgcolor=red>
<h1><center><font style="color:rgba(34, 200, 253, .7)">Home Server</font></center></h1>
</div>
<hr>
<?php #path to current directory?>
<hr>

<?php
$i = $count;
$folderInARow = 4;
$j = $folderInARow;
$flag=1;
echo "<div><center><div class=\"equalmargin\">";
while($i){
#display folders
if($j == $folderInARow && $flag==1)
{echo "<table><tr>";$flag=0;}
if (strpos($thelist[$i],'.')==0)
	{
	if(strpos($thelist[$i],'ovie'))
	echo "<td><div><center><img src=\"/OtherStuff/images/Icons/folderVideos.ico\" width=150px></center></div>"; 
	elseif(strpos($thelist[$i],'ideo'))
	echo "<td><div><center><img src=\"/OtherStuff/images/Icons/folderVideos.ico\" width=150px></center></div>"; 
	elseif(strpos($thelist[$i],'ware'))
	echo "<td><div><center><img src=\"/OtherStuff/images/Icons/folderSoftwares.png\" width=150px></center></div>"; 
	elseif(strpos($thelist[$i],'cloud'))
	echo "<td><div><center><img src=\"/OtherStuff/images/Icons/ownCloud3.png\" width=150px></center></div>"; 
	elseif(strpos($thelist[$i],'obot'))
	echo "<td><div><center><img src=\"/OtherStuff/images/Icons/folderFSociety1.png\" width=150px></center></div>"; 
	elseif(strpos($thelist[$i],'Trash'))
	goto again2;
	else echo "<td><div><center><img src=\"/OtherStuff/images/Icons/folder.png\" width=150px></center></div>"; 
	echo "<div class=\"box\"><center><h3><font style=\"color:rgb(65,126,129)\">"; echo $thelist[$i]; echo "</font></h3></center></div></td>"; 
	--$j;
	again2:
	$flag=1; 
	
	}
--$i;
if($j == 0 || $i == 0)
{echo "</tr></table><br>";
$j = $folderInARow;}
}
echo "</div></center></div>";
echo "<hr>";
$i = $count;
$fileInARow = 4;
$j = $fileInARow;
$flag=1;
echo "<div><center><div class=\"equalmargin\">";
while($i){
#display files
if($j == $folderInARow && $flag==1)
	{echo "<table><tr>";$flag=0;}
if (!(strpos($thelist[$i],'.')==0))
	{if(strpos($thelist[$i],'.pdf'))
	echo "<td><div><center><img src=\"/OtherStuff/images/Icons/pdf.png\" width=150px></center></div>";
	elseif(strpos($thelist[$i],'.txt'))
	echo "<td><div><center><img src=\"/OtherStuff/images/Icons/txt.png\" width=150px></center></div>";
	elseif(strpos($thelist[$i],'.doc'))
	echo "<td><div><center><img src=\"/OtherStuff/images/Icons/doc.png\" width=150px></center></div>";
	elseif(strpos($thelist[$i],'.xls'))
	echo "<td><div><center><img src=\"/OtherStuff/images/Icons/xls.png\" width=150px></center></div>";
	elseif(strpos($thelist[$i],'.jpg'))
	echo "<td><div><center><img src=\"/OtherStuff/images/Icons/jpg.png\" width=150px></center></div>";
	elseif(strpos($thelist[$i],'.png'))
	echo "<td><div><center><img src=\"/OtherStuff/images/Icons/png.png\" width=150px></center></div>";
	elseif(strpos($thelist[$i],'.mp4'))
	echo "<td><div><center><img src=\"/OtherStuff/images/Icons/mp4.png\" width=150px></center></div>";
	elseif(strpos($thelist[$i],'.avi'))
	echo "<td><div><center><img src=\"/OtherStuff/images/Icons/avi.png\" width=150px></center></div>";
	elseif(strpos($thelist[$i],'.3gp'))
	echo "<td><div><center><img src=\"/OtherStuff/images/Icons/3gp.png\" width=150px></center></div>";
	elseif(strpos($thelist[$i],'.flv'))
	echo "<td><div><center><img src=\"/OtherStuff/images/Icons/flv.png\" width=150px></center></div>";
	elseif(strpos($thelist[$i],'.mkv'))
	echo "<td><div><center><img src=\"/OtherStuff/images/Icons/mkv.png\" width=150px></center></div>";
	elseif(strpos($thelist[$i],'.mp3'))
	echo "<td><div><center><img src=\"/OtherStuff/images/Icons/mp3.png\" width=150px></center></div>";
	elseif(strpos($thelist[$i],'.wav'))
	echo "<td><div><center><img src=\"/OtherStuff/images/Icons/wav.png\" width=150px></center></div>";
	elseif(strpos($thelist[$i],'.html'))
	echo "<td><div><center><img src=\"/OtherStuff/images/Icons/code.png\" width=150px></center></div>";
	elseif(strpos($thelist[$i],'.php'))
	goto again;
	elseif(strpos($thelist[$i],'.css'))
	goto again;
	else echo "<td><div><center><img src=\"/OtherStuff/images/Icons/folder.png\" width=150px></center></div>";
	echo "<div class=\"box\"><center><h3><font style=\"color:rgb(65,126,129)\">"; echo $thelist[$i]; echo "</font></h3></center></div></td>"; 
	--$j;$flag=1;
	again: 
	}
--$i;
if($j == 0 || $i == 0)
{echo "</tr></table><br>";
$j = $fileInARow;}
}
echo "</div></center></div>";
echo "<hr>";
echo "<hr>";
?>
</body>
</html>
