#!/usr/bin/perl

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

use strict;
use warnings;

sub program_info
{
    my $info = "Converts a CSV (comma-separated values) formatted table into a " . 
               "MD (markdown) formatted equivalent.\r\n\r\n" .
               "The CSV-formatted lines is expected to come from STDIN. The " .
               "MD-formatted output is sent to STDOUT.\r\n\r\n" .
               "If comma is used as a delimiter, both command lines are valid:\r\n" .
               "\tcat input.csv | ./csv2md.pl > output.md\r\n" .
               "\tcat input.csv | ./csv2md.pl ',' > output.md\r\n\r\n" .
               "If semi-colon is used, then this should be specified instead:\r\n" .
               "\tcat input.csv | ./csv2md.pl ';' > output.md\r\n";
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
            print STDERR "Invalid delimiter! You must use comma or semicolon!\r\n";
            exit 1;
        }
    }
}
# More than one argument...
elsif ($nr_of_arguments > 1)
{
    print STDERR "Invalid arguments list!\r\n\r\n";
    print STDERR program_info();
    exit 1;
}

my $is_header_row = 1;
my $line;
foreach $line (<STDIN>)
{
    $line =~ tr/\r//d;
    $line =~ tr/\n//d;
    local $_ = $line;
    eval("s/$delimiter/|/g");
    print "|" . "$_" . "|\r\n";
    if ($is_header_row)
    {
        my $nr_of_delimiters = () = $line =~ /$delimiter/g;
        my $nr_of_columns = $nr_of_delimiters + 1;
        print "|", "---|" x $nr_of_columns, "\r\n";
    }
    $is_header_row = 0;
}