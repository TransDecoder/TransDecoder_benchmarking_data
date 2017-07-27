#!/usr/bin/env perl

use strict;
use warnings;

use Cwd;
use FindBin;

my @ref_files = qw (fragments/m_musculus/input_files/mmus-all-fragments.fasta
                    fragments/d_melanogaster/input_files/dmel-all-fragments.fasta
                    fragments/a_thaliana/input_files/a_thaliana_ann-fragments.fasta
                    fragments/s_pombe/input_files/spombe-all-fragments.fasta
                    complete/m_musculus/input_files/mmus-all.fasta
                    complete/d_melanogaster/input_files/dmel-all.fasta
                    complete/a_thaliana/input_files/a_thaliana_ann.fna
                    complete/s_pombe/input_files/spombe-all.fasta,
                    ./fragments/Marks_a_thaliana/input_files/a_thaliana.trimmed_ann.fna
 
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

    my @pts = split(/\//, $fasta_file);
    pop @pts;
    pop @pts;
    push (@pts, "output_files", "GeneMarkS-T");

    my $outdir = join("/", @pts);
    

    my $gmst_SS_param = "";
    if ($SS_flag) {
        $outdir .= "-SS";
        $gmst_SS_param = " --strand direct ";
    }
    
    if (! -d) {
        &process_cmd("mkdir $outdir");
    }
    
    
    
    return("cd $outdir && /seq/RNASEQ/TOOLS/GeneMarkS-T/gmst.pl --format GFF $gmst_SS_param $fasta_file");
    
}

sub get_prodigal_cmd {
    my ($fasta_file) = @_;
    
    my @pts = split(/\//, $fasta_file);
    pop @pts;
    pop @pts;
    push (@pts, "output_files", "Prodigal");

    my $outdir = join("/", @pts);

    if (! -d $outdir) {
        &process_cmd("mkdir $outdir");
    }
    
    return("cd $outdir && /seq/RNASEQ/TOOLS/prodigal/Prodigal-2.6.3/prodigal -f gff -o prodigal.out < $fasta_file");

}

sub get_transdecoder_cmd {
    my ($fasta_file, $SS_flag) = @_;
    
    my @pts = split(/\//, $fasta_file);
    pop @pts;
    pop @pts;
    push (@pts, "output_files", "TransDecoder");

    my $outdir = join("/", @pts);

    my $transdecoder_SS_param = "";
    if ($SS_flag) {
        $outdir .= "-SS";
        $transdecoder_SS_param = " -S ";
    }
    
    if (! -d $outdir) {
        &process_cmd("mkdir $outdir");
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



    
