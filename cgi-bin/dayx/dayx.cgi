#!/usr/bin/perl

## -----------------------------------------------------------------------
## DAY COUNTER-EX v2.2
## by KENT (99/06/21)
## E-MAIL: webmaster@kent-web.com
## URL:    http://www.kent-web.com/
## [注意事項‧同意事項]
## 1.這是一個免費程序，作者對這個程序可能造成的一切後果不負任何責任。
## 2.關於設置上的問題請到支援揭示板上發問。作者不會回答任何通過E-mail來發問的問題。
## ------------------------------------------------------------------------
## [在網頁上顯示計數器應插入的Html代碼一例 (在網頁編輯器中找個合適的住置將Html代碼貼上去主頁上)]
## 總訪客人數     <img src="http://ginet.virtualave.net/cgi-bin/dayx-gnet/dayx.cgi?gif">
## 本日訪客人數   <img src="http://ginet.virtualave.net/cgi-bin/dayx-gnet/dayx.cgi?today">
## 昨日訪客人數   <img src="http://ginet.virtualave.net/cgi-bin/dayx-gnet/dayx.cgi?yes">
##
## [觀看每日／每月統計結果方法一例 (在瀏覽器的網址欄中如下輸入即可觀看結果列表)]
##    http://ginet.virtualave.net/cgi-bin/dayx-gnet/dayxmgr.cgi
##
## [測試程序安裝狀況一例 (在瀏覽器的網址欄中如下輸入即可觀看結果列表)]
##    http://neoranga.musasino.com/cgi-bin/dayx/dayx.cgi?check
## ------------------------------------------------------------------------
## [設置例] 括號內的是檔案的訪問權限值
##
##    public_html / index.html (主頁)
##        |
##        +-- cgi-bin /  dayx [777] / dayx.cgi    [755]
##                         |          dayxmgr.cgi [755]
##                         |          gifcat.pl   [755]
##                         |          dayx.dat    [666]
##                         |          day.dat     [666]
##                         |          mon.dat     [666]
##                         |
##                         +-- gif1 / 1.gif 2.gif ... 0.gif
##                         |
##                         +-- gif2 / 1.gif 2.gif ... 0.gif
##
## -------------------------------------------------------------------

require './gifcat.pl';  # 顯示數字圖案用庫文件

## 基本設定
$figure1 = 6;			# 總訪客人數計數器的桁數
$figure2 = 3;			# 本日／昨日訪客人數計數器的桁數
$logfile = "./dayx.dat";	# 記錄檔案
$dayfile = "./day.dat";		# 每日記錄檔案
$monfile = "./mon.dat";		# 每月記錄檔案
$gif_path1 = "./gif1";		# 總訪客人數計數器使用的GIF圖案所在的目錄
$gif_path2 = "./gif2";		# 本日／昨日訪客人數計數器使用的GIF圖案所在的目錄
$lockkey = 2;			# 　File Lock方式 (0=no 1=symlink 2=open)
$lockfile = "dayx.lock";	# Lock File名
$lock_dir = ".";		# Lock File所在的目錄
$type = 1;			# 顯示方式 (不顯示總訪客人數時為 0 )
$ip_key = 1;			# IP地址檢查 (0=不檢查 1=每日一次 2=每小時一次)
## 設定完了

# 引數メ解釋
$mode = $ENV{'QUERY_STRING'};

# ①Чヱиャユюメ定義
$lockfile = "$lock_dir\/$lockfile";

# 更新系處理ザスゆスヘタ2-3秒待ギオペ
if ($type == 1 && $mode eq "yes") { sleep(3); }
elsif ($type == 1 && $mode eq "today") { sleep(2); }
elsif ($type == 0 && $mode eq "yes") { sleep(2); }

# ①Чヱ開始
if ($type == 1 && $mode eq "gif" && $lockkey == 1) { &lock1; }
elsif ($type == 0 && $mode eq "today" && $lockkey == 1) { &lock1; }
elsif ($type == 1 && $mode eq "gif" && $lockkey == 2) { &lock2; }
elsif ($type == 0 && $mode eq "today" && $lockkey == 2) { &lock2; }

# ХラЧヱхみЭ
if (!$mode || $mode eq 'check') { &check; }

# 記錄иャユюろヘ讀ノ�灰f
open(IN,"$logfile") || die "Can't open $logfile : $!";
@lines = <IN>;
close(IN);

$lines[0] =~ s/\n//;

# 記錄иャユюメ分解
($day_key,$yes,$today,$count,$youbi,$hr) = split(/<>/, $lines[0]);

# 本地時間
$ENV{'TZ'} = "JST-8";
($sec,$min,$hour,$mday,$mon,$year,$wday) = localtime(time);
$mon++;
$thisday = (Sun,Mon,Tue,Wed,Thu,Fri,Sat) [$wday];
if ($mon < 10) { $mon = "0$mon"; }
$date = "$year\/$mon";

# 本日ソロヨ⑦Ь數メワみズロヨ⑦ЬヤЧк
if (($type == 1 && $mode eq 'gif') || ($type == 0 && $mode eq 'today')) {

	$newcnt = $count + 1;

	## 當日處理
	if ($day_key == $mday) {
		$today++;

		# ①ヲメиルみсЧЬ
		$lines[0] = "$mday<>$yes<>$today<>$newcnt<>$thisday<>$hour<>\n";

		# IPヤЭяЗろヘ①ヲХラЧヱ
		$ipflag = 0;
		$addr = $ENV{'REMOTE_ADDR'};

		if ($ip_key == 1) { &ip_check1;	}
		elsif ($ip_key == 2) { &ip_check2; }

	}
	## 翌日處理
	else {
		# ①ヲメиルみсЧЬ
		$new[0] = "$mday<>$today<>1<>$newcnt<>$thisday<>$hour<>\n";
		if ($ip_key) { $new[1] = "$ENV{'REMOTE_ADDR'}\n"; }
		@lines = @new;

		&day_count;
		&mon_count;

		$today = 1;
	}

	# ①ヲメ更新
	if ($ipflag == 0) {
		&renew;

		$count++;
	}
}

# ①Чヱ解除
if ($type == 1 && $mode eq 'gif' || $type == 0 && $mode eq 'today') {
	unlink($lockfile) if (-e $lockfile);
}

# ロヨ⑦У畫像出力
&count_view;

exit;

## --- ロヨ⑦Уみ出力處理
##  (シナナイモソ wwwcounterメ參考ズイオサゆギクわネウギ)
sub count_view {
	$count += 0;

	$cntstr  = sprintf(sprintf("%%0%dld", $figure1), $count);
	$cntstr2 = sprintf(sprintf("%%0%dld", $figure2), $today);
	$cntstr3 = sprintf(sprintf("%%0%dld", $figure2), $yes);

	if ($mode eq "gif") {
		printf("Content-type: image/gif\n");
		printf("\n");
		for ($i=0; $i<length($cntstr); $i++) {
			$n = substr($cntstr, $i, 1);
			push(@files, "$gif_path1/$n.gif");
		}
	} elsif ($mode eq "today") {
		printf("Content-type: image/gif\n");
		printf("\n");
		for ($i=0; $i<length($cntstr2); $i++) {
			$n = substr($cntstr2, $i, 1);
			push(@files, "$gif_path2/$n.gif");
		}
	} elsif ($mode eq "yes") {
		printf("Content-type: image/gif\n");
		printf("\n");
		for ($i=0; $i<length($cntstr3); $i++) {
			$n = substr($cntstr3, $i, 1);
			push(@files, "$gif_path2/$n.gif");
		}
	}

	# 畫像出力
	binmode(STDOUT);
	print &gifcat'gifcat(@files);
}

## --- ①Чヱиャユю（symlink關數）
sub lock1 { 
	local($retry) = 5;
	while (!symlink(".", $lockfile)) {
		if (--$retry <= 0) {
			unlink($lockfile) if (-e $lockfile);
			die "BUSY : $!";
		}
		sleep(1);
	}
}

## --- ①Чヱиャユю（open關數）
sub lock2 { 
	local($flag) = 0;
	foreach (1 .. 5) {
		if (-e $lockfile) { sleep(1); }
		else {
			open(LOCK,">$lockfile");
			close(LOCK) || die "Can't write $lockfile : $!";
			$flag = 1;
			last;
		}
	}
	if ($flag == 0) { die "BUSY : $!"; }
}

## --- 日次ロヨ⑦Ь數ソ處理
sub day_count {
	# ①ヲソ日次ワみプベ本日ソ日ゎ小イんホタ月ゎ變マゲギシ判斷エペ
	if ($mday < $day_key) {
		open(DB,">$dayfile");
		print DB "";
		close(DB);
	}
	# 月內ザソ處理
	else {
		if ($day_key < 10) { $day_key = "0$day_key"; }
		open(DB,">>$dayfile");
		print DB "$mon\/$day_key \($youbi\)<>$today<>\n";
		close(DB);
	}
}

## --- 月間ロヨ⑦Ь數ソ處理
sub mon_count {
	# 初バサソヤヱЙЗソ場合
	if (-z $monfile) {
		$mons[0] = "$date<>$today<>\n";
	}

	else {
		open(IN,"$monfile");
		@mons = <IN>;
		close(IN);

		# ①ヲ配列ソ最終行メ分解
		$mons[$#mons] =~ s/\n//;
		($y_m,$cnt) = split(/<>/,$mons[$#mons]);

		# 當月處理
		if ($y_m eq "$date") {
			$cnt = $cnt + $today;
			$mons[$#mons] = "$y_m<>$cnt<>\n";
		}
		# 翌月處理
		#（①ヲ配列ソ最終行ゎ $dateシ異スホタ、月ゎ變ゲギシ判斷エペ）
		else {
			$cnt = $cnt + $today;
			$mons[$#mons] = "$y_m<>$cnt<>\n";
			push(@mons,"$date<>0<>\n");
		}
	}

	# ①ヲиャユюメ更新
	open(OUT,">$monfile");
	print OUT @mons;
	close(OUT);
}

## --- IPヤЭяЗメХラЧヱ（日單位）
sub ip_check1 {
	@ipdata = @lines;
	shift(@ipdata);

	foreach (@ipdata) {
		chop($_);
		if ($addr eq "$_") { $ipflag=1; last; }
	}

	push(@lines,"$addr\n");
}

## --- IPヤЭяЗメХラЧヱ（時間單位）
sub ip_check2 {
	if ($hour eq "$hr") { &ip_check1; }
	else {
		$temp = $lines[0];
		@lines = ();
		$lines[0] = "$temp";
		$lines[1] = "$addr" . "\n";
	}
}

## --- ЫみУ更新處理
sub renew {
	# Ъ⑦рьэみиャユюメ定義
	$prono = "$$";
	if ($prono eq "") {
		srand;
		$prono =  1000000000000000 * rand;
	}
	$tmpfile = "$lock_dir\/$prono\.tmp";

	# Ъ⑦рьэみиャユюメ作成
	if (!open(OUT,">$tmpfile")) {
		if (-e $lockfile) { unlink($lockfile); }
		die "Can't write tempfile : $!";
	}
	print OUT @lines;
	close(OUT);
	chmod(0666,$tmpfile);

	# эбみу處理
	rename($tmpfile,$logfile);

	# パウЪ⑦рьэみиャユюゎ殘ゲサゆギヘ削除
	if (-e $tmpfile) { unlink($tmpfile); }
}

## --- ХラЧヱхみЭ
sub check {
	print "Content-type: text/html\n\n";
	print "<html><head><title>DAY COUNTER-EX</title></head>\n";
	print "<body>\n<UL>\n";

	# ①ヲиャユюソеЗ確認
	if (-e $logfile) {
		print "<LI>記錄檔案的路徑 : OK!";
	} else {
		print "<LI>找不到記錄檔案。";
	}

	# ①ヲиャユюソеみтЧЁъ⑦（讀ノアノ）
	if (-r $logfile) {
		print "<LI>記錄檔案的讀取權限值設定 : OK!";
	} else {
		print "<LI>記錄檔案的讀取權限值設定不定確。";
	}

	# ①ヲиャユюソеみтЧЁъ⑦（書わアノ）
	if (-w $logfile) {
		print "<LI>記錄檔案的寫入權限值設定 : OK!";
	} else {
		print "<LI>記錄檔案的寫入權限值設定不定確。";
	}

	# 畫像ЫュяヱЬэ１ソеЗ確認
	if (-d $gif_path1) {
		print "<LI>gif1目錄路徑 : OK!";
	} else {
		print "<LI>沒有gif1這個目錄。";
	}

	# 畫像ЫュяヱЬэ２ソеЗ確認
	if (-d $gif_path2) {
		print "<LI>gif2目錄路徑 : OK!";
	} else {
		print "<LI>沒有gif2這個目錄。";
	}

	print "</UL>\n</body></html>\n";
	exit;
}
