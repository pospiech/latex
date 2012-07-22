#!/usr/bin/perl

# Prints content if input files 
# in the current file and save under a new name

use strict;
use warnings;

my $arg = shift(@ARGV);
my $parsefile;
my $outputfile;

if (defined($arg)) { $parsefile = $arg;  $arg = shift; }
if (defined($arg)) { $outputfile = $arg;  $arg = shift; }

open PARSEFILE, "<$parsefile" or die "file >$parsefile< can not be opended\n";
open OUTPUTFILE, ">$outputfile" or die "file >$outputfile< can not be saved\n";

# format current date

my ($mday, $mon, $year) = (localtime(time))[3, 4, 5];
$mon  += 1;
$year += 1900;
my $strCurrDate = sprintf("%02d/%02d/%02d", $year, $mon, $mday);

while (my $line = <PARSEFILE>) {
  # if replace <*date*> by string
  $line =~ s/<\*date\*>/$strCurrDate/;
  $_ = $line;
  # if string \input{*} is found 
  if ( m/\\input\{preamble\/(.*?)\}/ ) {
    # save arg #1 of regex as inputfile
	my $inputfile = "preamble/$1";
	# open input file
	print $inputfile."\n";
    open IN, "<$inputfile" or die "file not found\n";
	# print whole text in that file to output
	while (<IN>) {
		chomp;
		print OUTPUTFILE "$_\n";
	}
	# close it
    close IN;
	# print text to Outputfile
    
  } else {
    print OUTPUTFILE $_;
  }
}
close PARSEFILE;
close OUTPUTFILE;
exit 0;
