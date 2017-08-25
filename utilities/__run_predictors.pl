#!/usr/bin/env perl

use strict;
use warnings;

use Cwd;
use FindBin;


#qw (fragments/m_musculus/input_files/mmus-all-fragments.fasta
#                    fragments/d_melanogaster/input_files/dmel-all-fragments.fasta
#                    fragments/a_thaliana/input_files/a_thaliana_ann-fragments.fasta
#                    fragments/s_pombe/input_files/spombe-all-fragments.fasta






my @ref_files =  qw(


    complete/m_musculus/input_files/mouse.ref_transcripts.fasta
    complete/m_musculus/input_files/mouse.ref_transcripts.fasta.wRand
        
    complete/d_melanogaster/input_files/dmel.ref_transcripts.fasta
    complete/d_melanogaster/input_files/dmel.ref_transcripts.fasta.wRand

    complete/a_thaliana/input_files/athal.ref_transcripts.fasta
    complete/a_thaliana/input_files/athal.ref_transcripts.fasta.wRand

    complete/s_pombe/input_files/spombe.ref_transcripts.fasta
    complete/s_pombe/input_files/spombe.ref_transcripts.fasta.wRand


    fragments/m_musculus/input_files/mouse.fragmented_transcripts.fasta
    fragments/m_musculus/input_files/mouse.fragmented_transcripts.fasta.wRand

    fragments/d_melanogaster/input_files/dmel.fragmented_transcripts.fasta
    fragments/d_melanogaster/input_files/dmel.fragmented_transcripts.fasta.wRand

    fragments/a_thaliana/input_files/athal.fragmented_transcripts.fasta
    fragments/a_thaliana/input_files/athal.fragmented_transcripts.fasta.wRand

    fragments/s_pombe/input_files/spombe.fragmented_transcripts.fasta
    fragments/s_pombe/input_files/spombe.fragmented_transcripts.fasta.wRand

 
);

my $PROJ_BASEDIR = "$FindBin::Bin/..";



sub process_cmd {
    my ($cmd) = @_;

    my $ret = system($cmd);
    if ($ret) {
        die "Error, CMD: $cmd died with ret $ret";
    }

    return;
}



sub get_genemark_cmd { 
    my ($fasta_file, $SS_flag) = @_;

    my $wRand = "";
    if ($fasta_file =~ /wRand$/) {
        $wRand = "_wRand";
    }
    
    my @pts = split(/\//, $fasta_file);
    pop @pts;
    pop @pts;
    push (@pts, "output_files$wRand", "GeneMarkS-T");

    my $outdir = join("/", @pts);
    

    my $gmst_SS_param = "";
    if ($SS_flag) {
        $outdir .= "-SS";
        $gmst_SS_param = " --strand direct ";
    }
    
    if (! -d $outdir) {
        &process_cmd("mkdir -p $outdir");
    }
    
    
    
    return("cd $outdir && /seq/RNASEQ/TOOLS/GeneMarkS-T/gmst.pl --format GFF $gmst_SS_param $fasta_file");
    
}

sub get_prodigal_cmd {
    my ($fasta_file) = @_;

    my $wRand = "";
    if ($fasta_file =~ /wRand$/) {
        $wRand = "_wRand";
    }
    
    my @pts = split(/\//, $fasta_file);
    pop @pts;
    pop @pts;
    push (@pts, "output_files$wRand", "Prodigal");

    my $outdir = join("/", @pts);

    if (! -d $outdir) {
        &process_cmd("mkdir -p $outdir");
    }
    
    return("cd $outdir && /seq/RNASEQ/TOOLS/prodigal/Prodigal-2.6.3/prodigal -f gff -o prodigal.out -g 1 -n < $fasta_file");
    
}

sub get_transdecoder_cmd {
    my ($fasta_file, $SS_flag) = @_;

    my $wRand = "";
    if ($fasta_file =~ /wRand$/) {
        $wRand = "_wRand";
    }
    
    my @pts = split(/\//, $fasta_file);
    pop @pts;
    pop @pts;
    push (@pts, "output_files$wRand", "TransDecoder");
    
    my $outdir = join("/", @pts);

    my $transdecoder_SS_param = "";
    if ($SS_flag) {
        $outdir .= "-SS";
        $transdecoder_SS_param = " -S ";
    }
    
    if (! -d $outdir) {
        &process_cmd("mkdir -p $outdir");
    }
    
    return("cd $outdir && /home/unix/bhaas/GITHUB/TransDecoder/TransDecoder.LongOrfs -t $fasta_file $transdecoder_SS_param && /home/unix/bhaas/GITHUB/TransDecoder/TransDecoder.Predict -t $fasta_file");
    
}




main: {

    foreach my $ref_file (@ref_files) {

        my $full_path = "$PROJ_BASEDIR/$ref_file";
        
        print &get_genemark_cmd($full_path) . "\n";
        print &get_genemark_cmd($full_path, 1) . "\n";
        
        
        print &get_prodigal_cmd($full_path) . "\n";

        
        print &get_transdecoder_cmd($full_path) . "\n";
        print &get_transdecoder_cmd($full_path, 1) . "\n";
        
        
        
    }

    exit(0);
}



    
