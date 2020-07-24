#! /usr/bin/perl -w

use strict;
use warnings;

use File::Path qw( make_path );
use IPC::Open3 qw( open3 );
use Symbol qw( gensym );

if ( !$ARGV[0] ) {
    die "Usage: $0 [PACKAGE NAME] ([PACKAGE NAME]...)";
}

if ( $ENV{'HOME'} =~ m!^(/(?:\w+/)*\w+)$! ) {
    $ENV{'HOME'} = $1;
    print "HOME=$ENV{'HOME'}\n";
}
else {
    die "Invalid HOME path: $ENV{'HOME'}";
}

if ( $ENV{'PATH'} ) {
    print "PATH=$ENV{'PATH'}\n";
}
else {
    die "Invalid PATH path: $ENV{'PATH'}";
}

my $gitdir    = $ENV{'HOME'} . '/git';
my $fedpkgdir = $gitdir . '/fedpkg';

if ( !-d $gitdir ) {
    make_path $gitdir or die "Failed to create path: $gitdir";
}

if ( !-d $fedpkgdir ) {
    make_path $fedpkgdir or die "Failed to create path: $fedpkgdir";
}

my $cmd;
my $status;
my $pid;
my $stdin;
my $stdout;
my $stderr;

sub runcmd {
    print "Running: $cmd\n";
    $pid = open3( *MYSTDIN, *MYSTDOUT, *MYSTDERR = gensym, $cmd );
    waitpid( $pid, 0 );
    close(MYSTDIN);
    my @stdout = <MYSTDOUT>;
    my @stderr = <MYSTDERR>;
    $status = $? >> 8;
    if ( $status ne 0 ) {
        print "Failure running: \"$cmd\": exit $status\n";
        print "===== STDOUT =====\n";
        print "@stdout\n";
        print "===== STDERR =====\n";
        print "@stderr\n";
        exit $status;
    }
    else {
        print "@stdout\n";
    }
}

foreach my $pkg (@ARGV) {
    chdir($fedpkgdir) or die "Cannot change to path: $fedpkgdir";
    print "Processing $pkg\n";

    if ( !-d $pkg ) {
        $cmd = "fedpkg co $pkg";
        runcmd();
    }

    chdir($pkg);

    $cmd = "fedpkg switch-branch master";
    runcmd();

    $cmd = "fedpkg pull";
    runcmd();

    $cmd = "fedpkg sources";
    runcmd();

    my $spec    = "$pkg.spec";
    my $oldspec = "$spec.old";
    my $newspec = "$spec.new";

    unless ( open( SPEC, "$spec" ) ) {
        die "Cannot open $spec for reading";
    }

    my $goipath;
    my $goaltipaths;
    my $version;

    foreach (<SPEC>) {
        if ( $_ =~ m/^%global\s+goipath\s+/ ) {
            my $goipathline = $_;
            chomp $goipathline;
            ( my $x, my $y, $goipath ) = split( /\s+/, $goipathline );
        }
        if ( $_ =~ m/^%global\s+goaltipaths\s+/ ) {
            $goaltipaths = $_;
        }
        if ( $_ =~ m/^Version:\s+/ ) {
            my $versionline = $_;
            chomp $versionline;
            ( my $x, $version ) = split( /\s+/, $versionline );
        }
    }

    close(SPEC);

    print "goipath: $goipath\n";
    if ($goaltipaths) {
        print "goaltipaths: $goaltipaths\n";
    }

    rename( $spec, $oldspec ) or die "Cannot move $spec to $oldspec";

    $cmd = "go2rpm $goipath";
    runcmd();

    rename( $spec, $newspec ) or die "Cannot move $spec to $newspec";

    $cmd = "git diff";
    runcmd();

    unless ( open( SPEC, ">$spec" ) ) {
        die "Cannot open $spec for writing";
    }

    unless ( open( NEWSPEC, "$newspec" ) ) {
        die "Cannot open $newspec for reading";
    }

    unless ( open( OLDSPEC, "$oldspec" ) ) {
        die "Cannot open $oldspec for reading";
    }

    my $header    = 1;
    my $body      = 0;
    my $changelog = 0;

    foreach (<OLDSPEC>) {
        if ( $header eq 1 ) {
            print SPEC $_;
        }
        if ( $_ =~ m/^# https:\/\/$goipath/ ) {
            $header = 0;
        }
    }

    foreach (<NEWSPEC>) {
        if ( $body eq 1 ) {
            if ( $_ =~ m/^Version:\s+/ ) {
                $_ =~ s/\d+/0/g;
            }
            print SPEC $_;
        }
        if ( $_ =~ m/^%gometa/ && $goaltipaths ) {
            print SPEC "\n$goaltipaths";
        }
        if ( $_ =~ m/^# https:\/\/$goipath/ ) {
            $body = 1;
        }
        if ( $_ =~ m/^%changelog/ ) {
            $body = 0;
        }
    }

    seek OLDSPEC, 0, 0;

    foreach (<OLDSPEC>) {
        if ( $changelog eq 1 ) {
            print SPEC $_;
        }
        if ( $_ =~ m/^%changelog/ ) {
            $changelog = 1;
        }
    }

    close(OLDSPEC);
    close(NEWSPEC);
    close(SPEC);

    $cmd =
"rpmdev-bumpspec -V -c \"- Update to version $version (#)\" -n $version $spec";
    runcmd();

}
