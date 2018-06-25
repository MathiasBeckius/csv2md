#!/usr/bin/perl

#
# Converts a CSV (comma-separated values) formatted table into a
# MD (markdown) formatted equivalent.
#
# The CSV-formatted lines is expected to come from STDIN. The MD-formatted
# output is sent to STDOUT.
#
# If comma is used as a delimiter, both command lines are valid:
#     cat input.csv | ./csv2md.pl > output.md
#     cat input.csv | ./csv2md.pl ',' > output.md
#
# If semi-colon is used, then this should be specified instead:
#     cat input.csv | ./csv2md.pl ';' > output.md
#

use strict;
use warnings;

sub program_info
{
    my $info = "Converts a CSV (comma-separated values) formatted table into a " . 
               "MD (markdown) formatted equivalent.\n\n" .
               "The CSV-formatted lines is expected to come from STDIN. The " .
               "MD-formatted output is sent to STDOUT.\n\n" .
               "If comma is used as a delimiter, both command lines are valid:\n" .
               "\tcat input.csv | ./csv2md.pl > output.md\n" .
               "\tcat input.csv | ./csv2md.pl ',' > output.md\n\n" .
               "If semi-colon is used, then this should be specified instead:\n" .
               "\tcat input.csv | ./csv2md.pl ';' > output.md\n";
    return $info;
}

# Standard delimiter
my $delimiter = ',';

my $nr_of_arguments = scalar(@ARGV);
# Single argument?
if ($nr_of_arguments == 1)
{
    my $argument = lc $ARGV[0];
    if ($argument eq '--help')
    {
        print program_info();
        exit 1;
    }
    else
    {
        # Assume it is delimiter
        $delimiter = $argument;
        if ($delimiter ne ";" && $delimiter ne ",")
        {
            print "Invalid delimiter! You must use comma or semicolon!\n";
            exit 1;
        }
    }
}
# More than one argument...
elsif ($nr_of_arguments > 1)
{
    print "Invalid arguments list!\n\n";
    print program_info();
    exit 1;
}

my $is_header_row = 1;
my $line;
my $row;

#my $foobar = "Hello,\nworld!";
#print "$foobar\n\n";
#$foobar =~ tr/\n//d;
#$foobar =~ tr/,//d;
#print "$foobar\n";

foreach $line (<STDIN>)
{
    $line =~ tr/\r//d;
    $line =~ tr/\n//d;
    #local $_ = $line;
    #s/;/|/g;
    #s/{$delimiter}/|/g;
    #$row = $_;
    #print "|" . "$row" . "|\n";
    if ($is_header_row)
    {
        my $nr_of_columns = ($line =~ tr/;//) + 1;
        print "|", "---|" x $nr_of_columns, "\n";
    }
    $is_header_row = 0;
}


#is_header_row = True
#for line in sys.stdin:
#    line = line.replace('\r', '').replace('\n', '')
##    print('|' + line.replace(delimiter, '|') + '|')
#   if is_header_row:
#        print('|' + '---|' * (line.count(delimiter) + 1))
#    is_header_row = False