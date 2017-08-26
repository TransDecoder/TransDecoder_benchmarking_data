#!/usr/bin/env perl

use strict;
use warnings;

use lib ($ENV{EUK_MODULES});
use Fasta_reader;
use Nuc_translator;

my $usage = "usage: $0 ref_transcripts.fasta\n\n";

my $ref_trans_fa = $ARGV[0] or die $usage;



main: {

    my $count_failures = 0;
    
    my $fasta_reader = new Fasta_reader($ref_trans_fa);

    while (my $seq_obj = $fasta_reader->next()) {

        my $acc = $seq_obj->get_accession();
        my $sequence = $seq_obj->get_sequence();

        if ($acc =~ /CDS:(\d+)-(\d+)/) {
            my $cds_start = $1;
            my $cds_end = $2;

            my $cds_seq = substr($sequence, $cds_start-1, $cds_end - $cds_start + 1);

            my $prot = translate_sequence($cds_seq, 1);

            my $stop = chop($prot);
            my $start = substr($prot, 0, 1);

            if ($start eq "M" && $stop eq "*" && $prot !~ /\*/) {
                # validates
                print ">$acc\n$sequence\n";
            }
            else {
                print STDERR "Warning, $acc fails validation\n";
                $count_failures++;
            }
        }
        else {
            die "Error, cannot decode acc name: $acc";
        }
    }


    print STDERR "\n\n\t$count_failures sequences skipped due to failing start/stop requirements.\n\n";

    exit(0);
}


          
        
