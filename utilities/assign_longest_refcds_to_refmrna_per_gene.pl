#!/usr/bin/env perl

use strict;
use warnings;

use lib ($ENV{EUK_MODULES});
use Fasta_reader;

my $MAX_UTR_LENGTH = 250;

my $usage = "usage: $0 refseq.cds refseq.mrna\n\n";

my $refseq_cds = $ARGV[0] or die $usage;
my $refseq_mrna = $ARGV[1] or die $usage;

main: {

    my %gene_to_CDS = &get_gene_to_seqs($refseq_cds);
    my %gene_to_mRNA = &get_gene_to_seqs($refseq_mrna);

    foreach my $gene (keys %gene_to_CDS) {

        unless (exists $gene_to_mRNA{$gene}) { 
            print STDERR "-warning, no mRNA for cds of gene: $gene\n";
            next; 
        }
        
        my @CDSs = reverse sort { $a->{length} <=> $b->{length} } @{$gene_to_CDS{$gene}};
        my @mRNAs = reverse sort { $a->{length} <=> $b->{length} } @{$gene_to_mRNA{$gene}};


        my $selected_cds = undef;
        my $selected_mRNA = undef;
        
        foreach my $cds (@CDSs) {

            foreach my $mRNA (@mRNAs) {

                my $idx = index($mRNA->{seq}, $cds->{seq});

                if ($idx >= 0) {
                    
                    $selected_cds = $cds;
                    $selected_mRNA = $mRNA;
                    last;
                }
                
                
            }
            last if $selected_mRNA;
        }

        if ($selected_cds) {

            my $mRNA_acc = $selected_mRNA->{acc};
            my $mRNA_seq = $selected_mRNA->{seq};

            my $cds_seq = $selected_cds->{seq};

            my $cds_start_idx = index($mRNA_seq, $cds_seq);

            my $cds_len = $selected_cds->{length};
            my $cds_end_idx = $cds_start_idx + $cds_len -1;

            # make coords 1-based
            $cds_start_idx++;
            $cds_end_idx++;

            $mRNA_acc =~ s/\W/_/g;
            
            my $mrna_len = length($mRNA_seq);
            if ($mrna_len - $cds_end_idx > $MAX_UTR_LENGTH) {
                $mRNA_seq = substr($mRNA_seq, 0, $cds_end_idx + $MAX_UTR_LENGTH);
                print STDERR "\t-trimming 3'utr of $gene\n";
            }
            if ($cds_start_idx > $MAX_UTR_LENGTH) {
                my $delta = $cds_start_idx - $MAX_UTR_LENGTH;
                $mRNA_seq = substr($mRNA_seq, $delta);
                
                $cds_start_idx -= $delta;
                $cds_end_idx -= $delta;
                print STDERR "\t-trimming 5' utr of $gene\n";
            }
            
            my $new_cds_seq = substr($mRNA_seq, $cds_start_idx-1, $cds_end_idx -$cds_start_idx + 1);
            if ($new_cds_seq ne $cds_seq) {
                die "Error, new cds sequence doesnt match original cds sequence:\nnew:\n$new_cds_seq\norig:\n$cds_seq\n\n";
            }
            
            #print ">$gene $cds_start_idx-$cds_end_idx\n$new_cds_seq\n";

            $mRNA_seq = uc $mRNA_seq;
            
            print ">$gene-$mRNA_acc|CDS:$cds_start_idx-$cds_end_idx|length:$cds_len|\n$mRNA_seq\n";
        }
        else {
            print STDERR "-warning: no mapping between CDS and mRNA sequences for gene: $gene\n";
        }
    }
            
            
    exit(0);


}

####
sub get_gene_to_seqs {
    my ($file) = @_;

    my %gene_to_seqs;
    
    my $fasta_reader = new Fasta_reader($file);

    while (my $seq_obj = $fasta_reader->next()) {

        my $sequence = $seq_obj->get_sequence();
        my $acc = $seq_obj->get_accession();

        my $header = $seq_obj->get_header();

        # example header:
        # >lcl|NC_003070.9_cds_NP_001318899.1_2 [gene=ARV1] [locus_tag=AT1G01020] [db_xref=Araport:AT1G01020,TAIR:AT1G01020,GeneID:839569] [protein=ARV1 family protein] [protein_id=NP_001318899.1] [location=complement(join(6915..7069,7157..7232,7384..7450,7564..7649,7762..7835,7942..7987,8236..8325,8417..8464,8571..8666))]

        my $gene_id;
        if ($header =~ /\[locus_tag=([^\]]+)\]/) {
            $gene_id = $1;
        }
        elsif ($header =~ /\[gene=([^\]]+)\]/) {
            $gene_id = $1;
        }

        if ($gene_id) {
            
            push (@{$gene_to_seqs{$gene_id}}, { seq => lc $sequence,
                                                acc => $acc,
                                                length => length($sequence),
                  } );
        }
        else {
            print STDERR "-warning, no tag in the header for: $header\n";
        }
    }
    return(%gene_to_seqs);
}


