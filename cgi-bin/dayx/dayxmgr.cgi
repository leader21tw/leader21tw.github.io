#!/usr/bin/perl

## -----------------------------------------------------------------------
## DAY COUNTER-EX MANAGER v2.1
## by KENT (99/05/05)
## E-MAIL: webmaster@kent-web.com
## URL:    http://www.kent-web.com/

$ver = 'DayX v2.1';		# дみЖъ⑦情報（修正不要）

## [注意事項‧同意事項]
## 1.這是一個免費程序，作者對這個程序可能造成的一切後果不負任何責任。
## 2.關於設置上的問題請到支援揭示板上發問。作者不會回答任何通過E-mail來發問的問題。
## ------------------------------------------------------------------------

## 基本設定
$script  = "./dayxmgr.cgi";	# 本程序檔案名
$logfile = "./dayx.dat";	# 記錄檔案
$dayfile = "./day.dat";		# 每日記錄檔案
$monfile = "./mon.dat";		# 每月記錄檔案
$mcolor = "#0000E3";		# 每月訪客數圖表顏色
$dcolor = "#D900D9";		# 每日訪客數圖表顏色
$backurl = "#";	# 主頁位置
$title = "訪客人數統計一覽";	# 統計一覽頁的標題名

# 每月訪客數圖表的長度
# 一個月平圴有一千以上訪客可選50至100，一萬以上應選200～300
$mKEY = 60;

# 每日訪客數圖表的長度
# 一日平圴有十個以上訪客可選1到2，一百以上應選5到10，一千以上應選30到60
$dKEY = 6;

$bground = "";			# 壁紙的住置
$bgcolor = "#F1F1F1";	# 背景色
$text  = "#000000";		# 文字色
$link  = "#0000FF";		# 連結色（未訪問）
$vlink = "#800080";		# 連結色（己訪問）
$alink = "#FF0000";		# 連結色（訪問中）

## 設定完了

# 引數メ解釋
$mode = $ENV{'QUERY_STRING'};

if ($mode eq "mon") { &mon_view; }
&day_view;

## --- 月間ヤヱЙЗ數メ表示
sub mon_view {
	open(IN,"$monfile");
	@mlines = <IN>;
	close(IN);

	# HTMLメ表示
	&header;
	print "<table border=1 cellpadding=5>\n";
	print "<caption><h4>每月訪客一覽</h4></caption>\n";
	print "<tr><th bgcolor=#D5FFD5>月份</th><th bgcolor=#D5FFD5>訪客數</th>\n";
	print "<th bgcolor=#D5FFD5>圖表</th></tr>\n";

	$flag = 0;
	foreach (@mlines) {
		($y_m,$mcnt) = split(/<>/, $_);

		# ヲьи幅メ指定
		$width = $mcnt / $mKEY;
		$width = int($width);

		# 桁處理
		$mcnt = &filler($mcnt);

		print "<tr><th nowrap>$y_m</th><td align=right>$mcnt</td>";
		print "<td><Table Width=$width Height=10 CellSpacing=0 CellPadding=0><Tr><Td BgColor=$mcolor><Img Width=1 Height=1></Td></Tr></Table></td></tr>\n";
	}

	print "</table>\n";
	&footer;
	exit;
}

## --- 日次ヤヱЙЗ數メ表示
sub day_view {
	open(IN,"$dayfile");
	@dlines = <IN>;
	close(IN);

	# HTMLメ表示
	&header;
	print "<table border=1 cellpadding=5>\n";
	print "<caption><h4>每日訪客一覽</h4></caption>\n";
	print "<tr><th bgcolor=#D5FFD5>日期</th><th bgcolor=#D5FFD5>訪客數</th>\n";
	print "<th bgcolor=#D5FFD5>圖表</th></tr>\n";

	$flag = 0;
	foreach (@dlines) {
		($m_d,$dcnt) = split(/<>/, $_);

		# ヲьи幅メ指定
		$width = $dcnt / $dKEY;
		$width = int($width);

		# 桁處理
		$dcnt = &filler($dcnt);

		print "<tr><th nowrap>$m_d</th><td align=right>$dcnt</td>\n";
		print "<td><Table Width=$width Height=10 CellSpacing=0 CellPadding=0><Tr><Td BgColor=$dcolor><Img Width=1 Height=1></Td></Tr></Table></td></tr>\n";
	}

	print "</table>\n";
	&footer;
	exit;
}

## --- HTMLлЧФ
sub header {
	print "Content-type: text/html\n\n";
	print "<html>\n<head>\n";
	print "<META HTTP-EQUIV=\"Content-type\" CONTENT=\"text/html; charset=big5\">\n";
	print "<title>$title</title></head>\n";

	# bodyУヲ
	if ($bground) {
		print "<body background=\"$bground\" bgcolor=$bgcolor text=$text link=$link vlink=$vlink alink=$alink>\n";
	} else {
		print "<body bgcolor=$bgcolor text=$text link=$link vlink=$vlink alink=$alink>\n";
	}

	

	# 集計切ベ替りズプペэ⑦ヱ部メ表示
	if ($mode eq "mon") {
		print "[<a href=\"$script\">每日統計</a>]\n";

	} else {
		print "[<a href=\"$script?mon\">每月統計</a>]\n";
	}

	# УユЬю部ソ表示
	print "<table width=100%><tr><th bgcolor=#008080>\n";
	print "<font color=#FFFFFF>$title</font></th></tr></table>\n";
	print "<P><center>\n";
}

## --- HTMLиЧУ
sub footer {
	
	print "</small></center>\n";
	print "</body></html>\n";
}

## --- 桁區わベ處理
sub filler {
	local($_) = $_[0];
	1 while s/(.*\d)(\d\d\d)/$1,$2/;
	return $_;
}

