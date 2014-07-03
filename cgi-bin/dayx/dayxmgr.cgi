#!/usr/bin/perl

## -----------------------------------------------------------------------
## DAY COUNTER-EX MANAGER v2.1
## by KENT (99/05/05)
## E-MAIL: webmaster@kent-web.com
## URL:    http://www.kent-web.com/

$ver = 'DayX v2.1';		# ����Ǵ���ﱡ���]�ץ����n�^

## [�`�N�ƶ��E�P�N�ƶ�]
## 1.�o�O�@�ӧK�O�{�ǡA�@�̹�o�ӵ{�ǥi��y�����@����G���t����d���C
## 2.����]�m�W�����D�Ш�䴩���ܪO�W�o�ݡC�@�̤��|�^������q�LE-mail�ӵo�ݪ����D�C
## ------------------------------------------------------------------------

## �򥻳]�w
$script  = "./dayxmgr.cgi";	# ���{���ɮצW
$logfile = "./dayx.dat";	# �O���ɮ�
$dayfile = "./day.dat";		# �C��O���ɮ�
$monfile = "./mon.dat";		# �C��O���ɮ�
$mcolor = "#0000E3";		# �C��X�ȼƹϪ��C��
$dcolor = "#D900D9";		# �C��X�ȼƹϪ��C��
$backurl = "#";	# �D����m
$title = "�X�ȤH�Ʋέp�@��";	# �έp�@���������D�W

# �C��X�ȼƹϪ�����
# �@�Ӥ륭�ʦ��@�d�H�W�X�ȥi��50��100�A�@�U�H�W����200��300
$mKEY = 60;

# �C��X�ȼƹϪ�����
# �@�饭�ʦ��Q�ӥH�W�X�ȥi��1��2�A�@�ʥH�W����5��10�A�@�d�H�W����30��60
$dKEY = 6;

$bground = "";			# ���Ȫ���m
$bgcolor = "#F1F1F1";	# �I����
$text  = "#000000";		# ��r��
$link  = "#0000FF";		# �s����]���X�ݡ^
$vlink = "#800080";		# �s����]�v�X�ݡ^
$alink = "#FF0000";		# �s����]�X�ݤ��^

## �]�w���F

# �޼��y����
$mode = $ENV{'QUERY_STRING'};

if ($mode eq "mon") { &mon_view; }
&day_view;

## --- �붡�|ǫǷǵ���y���
sub mon_view {
	open(IN,"$monfile");
	@mlines = <IN>;
	close(IN);

	# HTML�y���
	&header;
	print "<table border=1 cellpadding=5>\n";
	print "<caption><h4>�C��X�Ȥ@��</h4></caption>\n";
	print "<tr><th bgcolor=#D5FFD5>���</th><th bgcolor=#D5FFD5>�X�ȼ�</th>\n";
	print "<th bgcolor=#D5FFD5>�Ϫ�</th></tr>\n";

	$flag = 0;
	foreach (@mlines) {
		($y_m,$mcnt) = split(/<>/, $_);

		# Ǭ���ѴT�y���w
		$width = $mcnt / $mKEY;
		$width = int($width);

		# ��B�z
		$mcnt = &filler($mcnt);

		print "<tr><th nowrap>$y_m</th><td align=right>$mcnt</td>";
		print "<td><Table Width=$width Height=10 CellSpacing=0 CellPadding=0><Tr><Td BgColor=$mcolor><Img Width=1 Height=1></Td></Tr></Table></td></tr>\n";
	}

	print "</table>\n";
	&footer;
	exit;
}

## --- �馸�|ǫǷǵ���y���
sub day_view {
	open(IN,"$dayfile");
	@dlines = <IN>;
	close(IN);

	# HTML�y���
	&header;
	print "<table border=1 cellpadding=5>\n";
	print "<caption><h4>�C��X�Ȥ@��</h4></caption>\n";
	print "<tr><th bgcolor=#D5FFD5>���</th><th bgcolor=#D5FFD5>�X�ȼ�</th>\n";
	print "<th bgcolor=#D5FFD5>�Ϫ�</th></tr>\n";

	$flag = 0;
	foreach (@dlines) {
		($m_d,$dcnt) = split(/<>/, $_);

		# Ǭ���ѴT�y���w
		$width = $dcnt / $dKEY;
		$width = int($width);

		# ��B�z
		$dcnt = &filler($dcnt);

		print "<tr><th nowrap>$m_d</th><td align=right>$dcnt</td>\n";
		print "<td><Table Width=$width Height=10 CellSpacing=0 CellPadding=0><Tr><Td BgColor=$dcolor><Img Width=1 Height=1></Td></Tr></Table></td></tr>\n";
	}

	print "</table>\n";
	&footer;
	exit;
}

## --- HTML��ǿǼ
sub header {
	print "Content-type: text/html\n\n";
	print "<html>\n<head>\n";
	print "<META HTTP-EQUIV=\"Content-type\" CONTENT=\"text/html; charset=big5\">\n";
	print "<title>$title</title></head>\n";

	# bodyǻǬ
	if ($bground) {
		print "<body background=\"$bground\" bgcolor=$bgcolor text=$text link=$link vlink=$vlink alink=$alink>\n";
	} else {
		print "<body bgcolor=$bgcolor text=$text link=$link vlink=$vlink alink=$alink>\n";
	}

	

	# ���p���q�����R�o�r����ǫ���y���
	if ($mode eq "mon") {
		print "[<a href=\"$script\">�C��έp</a>]\n";

	} else {
		print "[<a href=\"$script?mon\">�C��έp</a>]\n";
	}

	# ǻ�~���糡�U���
	print "<table width=100%><tr><th bgcolor=#008080>\n";
	print "<font color=#FFFFFF>$title</font></th></tr></table>\n";
	print "<P><center>\n";
}

## --- HTML��ǿǻ
sub footer {
	
	print "</small></center>\n";
	print "</body></html>\n";
}

## --- ������q�B�z
sub filler {
	local($_) = $_[0];
	1 while s/(.*\d)(\d\d\d)/$1,$2/;
	return $_;
}

