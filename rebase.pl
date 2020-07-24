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
    my $group;
    my $sources      = "";
    my $reqs         = "";
    my $reqsblock    = 0;
    my $hasbuild     = 0;
    my $build        = "";
    my $buildblock   = 0;
    my $install      = "";
    my $installblock = 0;
    my $files        = "";
    my $filesblock   = 0;
    my $goprep       = "";
    my $goprepblock  = 0;

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
        if ( $_ =~ m/^Group:\s+/ ) {
            $group = $_;
        }
        if ( $_ =~ m/^Source\d+:\s+/ ) {
            $sources = $sources . $_;
        }
        if ( $_ =~ m/^%build/ ) {
            $hasbuild   = 1;
            $buildblock = 1;
        }
        if ( $_ =~ m/^%install/ ) {
            $buildblock = 0;
        }
        if ( $hasbuild eq 1 && $buildblock eq 1 ) {
            $build = $build . $_;
        }
        if ( $_ =~ m/^%install/ ) {
            $installblock = 1;
        }
        if ( $_ =~ m/^%if\s+/ ) {
            $installblock = 0;
        }
        if ( $installblock eq 1 ) {
            $install = $install . $_;
        }
        if ( $_ =~ m/^%files/ ) {
            $filesblock = 1;
        }
        if ( $_ =~ m/^%gopkgfiles/ ) {
            $filesblock = 0;
        }
        if ( $hasbuild eq 1 && $filesblock eq 1 ) {
            $files = $files . $_;
        }
        if ( $goprepblock eq 1 ) {
            $goprep = $goprep . $_;
        }
        if ( $_ =~ m/^%goprep/ ) {
            $goprepblock = 1;
        }
        if ( $_ =~ m/^$/ ) {
            $goprepblock = 0;
        }
        if ( $_ =~ m/^Source\d+:\s+/ ) {
            $reqsblock = 1;
        }
        if ( $_ =~ m/^%description/ || $_ =~ m/^%if\s+/ ) {
            $reqsblock = 0;
        }
        if (   $reqsblock eq 1
            && $_ !~ m/^BuildRequires:  golang/
            && $_ !~ /^Source\d+:\s+/ )
        {
            $reqs = $reqs . $_;
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

    $buildblock   = 0;
    $installblock = 0;
    $filesblock   = 0;
    $reqsblock    = 0;

    foreach (<NEWSPEC>) {
        if ( $_ =~ m/^BuildRequires:\s+golang/ ) {
            $reqsblock = 1;
        }
        if ( $_ =~ /^$/ && $reqsblock eq 1 && $reqs ) {
            chomp $reqs;
            $_         = "$reqs";
            $reqsblock = 0;
        }
        if ( $_ =~ m/^%build/ && $hasbuild eq 1 ) {
            print SPEC "$build";
        }
        if ( $_ =~ m/^%install/ ) {
            print SPEC "$install";
        }
        if ( $_ =~ m/^%files/ && $hasbuild eq 1 ) {
            print SPEC "$files";
        }
        if ( $body eq 1 && $changelog eq 0 ) {
            if ( $_ =~ m/^Version:\s+/ ) {
                $_ =~ s/\d+/0/g;
            }
            if ( $_ =~ m/^Source\d+:\s+/ ) {
                $_ = "";
            }
            if ( $_ =~ m/^%build/ && $buildblock eq 0 ) {
                $buildblock = 1;
            }
            if ( $_ =~ m/^%install/ && $buildblock eq 1 ) {
                $buildblock = 0;
            }
            if ( $buildblock eq 1 ) {
                $_ = "";
            }
            if ( $_ =~ m/^%install/ && $installblock eq 0 ) {
                $installblock = 1;
            }
            if ( $_ =~ m/^%if\s+/ && $installblock eq 1 ) {
                $installblock = 0;
            }
            if ( $installblock eq 1 ) {
                $_ = "";
            }
            if ( $_ =~ m/^%files/ && $filesblock eq 0 ) {
                $filesblock = 1;
            }
            if ( $_ =~ m/^%gopkgfiles/ && $filesblock eq 1 ) {
                $filesblock = 0;
            }
            if ( $filesblock eq 1 ) {
                $_ = "";
            }
            print SPEC $_;
        }
        if ( $_ =~ m/^%gometa/ && $goaltipaths ) {
            print SPEC "\n$goaltipaths";
        }
        if ( $_ =~ m/^Summary:\s+/ && $group ) {
            print SPEC "\n$group";
        }
        if ( $_ =~ m/^URL:\s+/ && $reqsblock eq 0 && $sources ) {
            print SPEC "$sources";
        }
        if ( $_ =~ m/^%goprep/ ) {
            chomp $goprep;
            print SPEC "$goprep";
        }
        if ( $_ =~ m/^# https:\/\/$goipath/ ) {
            $body = 1;
        }
        if ( $_ =~ m/^%changelog/ ) {
            $changelog = 1;
        }
    }

    $changelog = 0;

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
