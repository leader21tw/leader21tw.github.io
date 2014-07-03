#!/usr/bin/perl

## -----------------------------------------------------------------------
## DAY COUNTER-EX v2.2
## by KENT (99/06/21)
## E-MAIL: webmaster@kent-web.com
## URL:    http://www.kent-web.com/
## [�`�N�ƶ��E�P�N�ƶ�]
## 1.�o�O�@�ӧK�O�{�ǡA�@�̹�o�ӵ{�ǥi��y�����@����G���t����d���C
## 2.����]�m�W�����D�Ш�䴩���ܪO�W�o�ݡC�@�̤��|�^������q�LE-mail�ӵo�ݪ����D�C
## ------------------------------------------------------------------------
## [�b�����W��ܭp�ƾ������J��Html�N�X�@�� (�b�����s�边����ӦX�A����m�NHtml�N�X�K�W�h�D���W)]
## �`�X�ȤH��     <img src="http://ginet.virtualave.net/cgi-bin/dayx-gnet/dayx.cgi?gif">
## ����X�ȤH��   <img src="http://ginet.virtualave.net/cgi-bin/dayx-gnet/dayx.cgi?today">
## �Q��X�ȤH��   <img src="http://ginet.virtualave.net/cgi-bin/dayx-gnet/dayx.cgi?yes">
##
## [�[�ݨC����C��έp���G��k�@�� (�b�s���������}�椤�p�U��J�Y�i�[�ݵ��G�C��)]
##    http://ginet.virtualave.net/cgi-bin/dayx-gnet/dayxmgr.cgi
##
## [���յ{�Ǧw�˪��p�@�� (�b�s���������}�椤�p�U��J�Y�i�[�ݵ��G�C��)]
##    http://neoranga.musasino.com/cgi-bin/dayx/dayx.cgi?check
## ------------------------------------------------------------------------
## [�]�m��] �A�������O�ɮת��X���v����
##
##    public_html / index.html (�D��)
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

require './gifcat.pl';  # ��ܼƦr�Ϯץήw���

## �򥻳]�w
$figure1 = 6;			# �`�X�ȤH�ƭp�ƾ������
$figure2 = 3;			# ������Q��X�ȤH�ƭp�ƾ������
$logfile = "./dayx.dat";	# �O���ɮ�
$dayfile = "./day.dat";		# �C��O���ɮ�
$monfile = "./mon.dat";		# �C��O���ɮ�
$gif_path1 = "./gif1";		# �`�X�ȤH�ƭp�ƾ��ϥΪ�GIF�ϮשҦb���ؿ�
$gif_path2 = "./gif2";		# ������Q��X�ȤH�ƭp�ƾ��ϥΪ�GIF�ϮשҦb���ؿ�
$lockkey = 2;			# �@File Lock�覡 (0=no 1=symlink 2=open)
$lockfile = "dayx.lock";	# Lock File�W
$lock_dir = ".";		# Lock File�Ҧb���ؿ�
$type = 1;			# ��ܤ覡 (������`�X�ȤH�Ʈɬ� 0 )
$ip_key = 1;			# IP�a�}�ˬd (0=���ˬd 1=�C��@�� 2=�C�p�ɤ@��)
## �]�w���F

# �޼��y����
$mode = $ENV{'QUERY_STRING'};

# ��ǿǫ���{�~���y�w�q
$lockfile = "$lock_dir\/$lockfile";

# ��s�t�B�z�N�Q���Q�p�W2-3����F�B�r
if ($type == 1 && $mode eq "yes") { sleep(3); }
elsif ($type == 1 && $mode eq "today") { sleep(2); }
elsif ($type == 0 && $mode eq "yes") { sleep(2); }

# ��ǿǫ�}�l
if ($type == 1 && $mode eq "gif" && $lockkey == 1) { &lock1; }
elsif ($type == 0 && $mode eq "today" && $lockkey == 1) { &lock1; }
elsif ($type == 1 && $mode eq "gif" && $lockkey == 2) { &lock2; }
elsif ($type == 0 && $mode eq "today" && $lockkey == 2) { &lock2; }

# ǽǣǿǫ������
if (!$mode || $mode eq 'check') { &check; }

# �O�����{�~�����pŪ�fȦ�f
open(IN,"$logfile") || die "Can't open $logfile : $!";
@lines = <IN>;
close(IN);

$lines[0] =~ s/\n//;

# �O�����{�~���y����
($day_key,$yes,$today,$count,$youbi,$hr) = split(/<>/, $lines[0]);

# ���a�ɶ�
$ENV{'TZ'} = "JST-8";
($sec,$min,$hour,$mday,$mon,$year,$wday) = localtime(time);
$mon++;
$thisday = (Sun,Mon,Tue,Wed,Thu,Fri,Sat) [$wday];
if ($mon < 10) { $mon = "0$mon"; }
$date = "$year\/$mon";

# �����UǧǢ���ļ��yǩ���RǧǢ�����|ǿ��
if (($type == 1 && $mode eq 'gif') || ($type == 0 && $mode eq 'today')) {

	$newcnt = $count + 1;

	## ���B�z
	if ($day_key == $mday) {
		$today++;

		# ��Ǭ�y��ǥ����ǿ��
		$lines[0] = "$mday<>$yes<>$today<>$newcnt<>$thisday<>$hour<>\n";

		# IP�|����ǵ���p��Ǭǽǣǿǫ
		$ipflag = 0;
		$addr = $ENV{'REMOTE_ADDR'};

		if ($ip_key == 1) { &ip_check1;	}
		elsif ($ip_key == 2) { &ip_check2; }

	}
	## �ݤ�B�z
	else {
		# ��Ǭ�y��ǥ����ǿ��
		$new[0] = "$mday<>$today<>1<>$newcnt<>$thisday<>$hour<>\n";
		if ($ip_key) { $new[1] = "$ENV{'REMOTE_ADDR'}\n"; }
		@lines = @new;

		&day_count;
		&mon_count;

		$today = 1;
	}

	# ��Ǭ�y��s
	if ($ipflag == 0) {
		&renew;

		$count++;
	}
}

# ��ǿǫ�Ѱ�
if ($type == 1 && $mode eq 'gif' || $type == 0 && $mode eq 'today') {
	unlink($lockfile) if (-e $lockfile);
}

# ǧǢ��ǻ�e���X�O
&count_view;

exit;

## --- ǧǢ��ǻ��X�O�B�z
##  (�O�b�b���z�U wwwcounter�y�Ѧ��R���B�M���F�G���e���F)
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

	# �e���X�O
	binmode(STDOUT);
	print &gifcat'gifcat(@files);
}

## --- ��ǿǫ���{�~��]symlink���ơ^
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

## --- ��ǿǫ���{�~��]open���ơ^
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

## --- �馸ǧǢ���ļ��U�B�z
sub day_count {
	# ��Ǭ�U�馸ǩ���o�q�����U����p�����s�W�������v�J�F�O�P�_�@�r
	if ($mday < $day_key) {
		open(DB,">$dayfile");
		print DB "";
		close(DB);
	}
	# �뤺�N�U�B�z
	else {
		if ($day_key < 10) { $day_key = "0$day_key"; }
		open(DB,">>$dayfile");
		print DB "$mon\/$day_key \($youbi\)<>$today<>\n";
		close(DB);
	}
}

## --- �붡ǧǢ���ļ��U�B�z
sub mon_count {
	# ���h�M�U�|ǫǷǵ�U���X
	if (-z $monfile) {
		$mons[0] = "$date<>$today<>\n";
	}

	else {
		open(IN,"$monfile");
		@mons = <IN>;
		close(IN);

		# ��Ǭ�t�C�U�̲צ��y����
		$mons[$#mons] =~ s/\n//;
		($y_m,$cnt) = split(/<>/,$mons[$#mons]);

		# ���B�z
		if ($y_m eq "$date") {
			$cnt = $cnt + $today;
			$mons[$#mons] = "$y_m<>$cnt<>\n";
		}
		# �ݤ�B�z
		#�]��Ǭ�t�C�U�̲צ��� $date�O���Q�s�W�B�������J�F�O�P�_�@�r�^
		else {
			$cnt = $cnt + $today;
			$mons[$#mons] = "$y_m<>$cnt<>\n";
			push(@mons,"$date<>0<>\n");
		}
	}

	# ��Ǭ���{�~���y��s
	open(OUT,">$monfile");
	print OUT @mons;
	close(OUT);
}

## --- IP�|����ǵ�yǽǣǿǫ�]����^
sub ip_check1 {
	@ipdata = @lines;
	shift(@ipdata);

	foreach (@ipdata) {
		chop($_);
		if ($addr eq "$_") { $ipflag=1; last; }
	}

	push(@lines,"$addr\n");
}

## --- IP�|����ǵ�yǽǣǿǫ�]�ɶ����^
sub ip_check2 {
	if ($hour eq "$hr") { &ip_check1; }
	else {
		$temp = $lines[0];
		@lines = ();
		$lines[0] = "$temp";
		$lines[1] = "$addr" . "\n";
	}
}

## --- ����ǻ��s�B�z
sub renew {
	# ���������������{�~���y�w�q
	$prono = "$$";
	if ($prono eq "") {
		srand;
		$prono =  1000000000000000 * rand;
	}
	$tmpfile = "$lock_dir\/$prono\.tmp";

	# ���������������{�~���y�@��
	if (!open(OUT,">$tmpfile")) {
		if (-e $lockfile) { unlink($lockfile); }
		die "Can't write tempfile : $!";
	}
	print OUT @lines;
	close(OUT);
	chmod(0666,$tmpfile);

	# �������ܳB�z
	rename($tmpfile,$logfile);

	# �i�����������������{�~������J�M���F�p�d��
	if (-e $tmpfile) { unlink($tmpfile); }
}

## --- ǽǣǿǫ������
sub check {
	print "Content-type: text/html\n\n";
	print "<html><head><title>DAY COUNTER-EX</title></head>\n";
	print "<body>\n<UL>\n";

	# ��Ǭ���{�~���U��ǵ�T�{
	if (-e $logfile) {
		print "<LI>�O���ɮת����| : OK!";
	} else {
		print "<LI>�䤣��O���ɮסC";
	}

	# ��Ǭ���{�~���U������ǿǳ����]Ū�f���f�^
	if (-r $logfile) {
		print "<LI>�O���ɮת�Ū���v���ȳ]�w : OK!";
	} else {
		print "<LI>�O���ɮת�Ū���v���ȳ]�w���w�T�C";
	}

	# ��Ǭ���{�~���U������ǿǳ����]�������f�^
	if (-w $logfile) {
		print "<LI>�O���ɮת��g�J�v���ȳ]�w : OK!";
	} else {
		print "<LI>�O���ɮת��g�J�v���ȳ]�w���w�T�C";
	}

	# �e�����}��ǫ���械�U��ǵ�T�{
	if (-d $gif_path1) {
		print "<LI>gif1�ؿ����| : OK!";
	} else {
		print "<LI>�S��gif1�o�ӥؿ��C";
	}

	# �e�����}��ǫ���梱�U��ǵ�T�{
	if (-d $gif_path2) {
		print "<LI>gif2�ؿ����| : OK!";
	} else {
		print "<LI>�S��gif2�o�ӥؿ��C";
	}

	print "</UL>\n</body></html>\n";
	exit;
}
