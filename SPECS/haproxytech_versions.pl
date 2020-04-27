#! /usr/bin/perl -wT

use strict;
use warnings;

my @packages = ( 'client-native', 'config-parser', 'dataplaneapi', 'models' );
my %packageversions;

foreach my $package (@packages) {
    print $package . "\n";
    my $spec = "golang-github-haproxytech-" . $package . ".spec";
    unless ( open( SPEC, $spec ) ) {
        die "Cannot open " . $spec . ": " . $! . "\n";
    }

    foreach my $line (<SPEC>) {
        if ( $line =~ m/^Version:\s+/ ) {
            chomp $line;
            my $version = $line;
            $version =~ s/^Version:\s+//g;
            print $version . "\n";
            $packageversions{$package} = $version;
        }
    }
    close(SPEC);
}

foreach my $package (@packages) {
    print $package . "\n";
    my $spec = "golang-github-haproxytech-" . $package . ".spec";
    my $tmp  = "golang-github-haproxytech-" . $package . ".spec.tmp";
    unless ( open( IN, $spec ) ) {
        die "Cannot open " . $spec . " for reading: " . $! . "\n";
    }
    unless ( open( OUT, '>', $tmp ) ) {
        die "Cannot open " . $tmp . " for writing: " . $! . "\n";
    }

    foreach my $line (<IN>) {
        if ( $line =~
            m/^BuildRequires:  golang\(github\.com\/haproxytech\/.*\/v2.*\)$/ )
        {
            chomp $line;

            #print $line . "\n";
            my ( $gh, $hap, $reqpkg, $v2, $x ) = split( /\//, $line );

            #print $reqpkg . "\n";
            $line =~ s/\/haproxytech\/$reqpkg\/v2/\/haproxytech\/$reqpkg/;
            print OUT $line . " >= " . $packageversions{$reqpkg} . "\n";
        }
        else {
            print OUT $line;
        }
    }

    close(OUT);
    close(IN);

    unless ( unlink($spec) ) {
        die "Cannot remove " . $spec . ": " . $! . "\n";
    }
    unless ( rename( $tmp, $spec ) ) {
        die "Cannot move " . $tmp . " to " . $spec . ": " . $! . "\n";
    }

}
