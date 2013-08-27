#!/usr/bin/perl -w

@files = <*.JPG>;

@sorted = sort{ -M $b <=> -M $a } @files;

mkdir( "resize" );
for($i = 0; $i <= $#sorted; $i++)
{
	$j = $i+1;
	$sorted[$i] =~ s/([\s])/\\$1/g;
	`convert -resize 2048 $sorted[$i] resize/$j.JPG`
}

`ffmpeg -y -i resize/%d.JPG -r 12 -croptop 180 -cropbottom 180 -s hd720 -vcodec ffv1 movie.avi`;
