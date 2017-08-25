#!/usr/bin/env perl

use strict;
use warnings;

use Cwd;
use FindBin;


my @ref_files = qw(

    complete/m_musculus/input_files/mouse.ref_transcripts.fasta.wRand

    complete/d_melanogaster/input_files/dmel.ref_transcripts.fasta.wRand

    complete/a_thaliana/input_files/athal.ref_transcripts.fasta.wRand

    complete/s_pombe/input_files/spombe.ref_transcripts.fasta.wRand

    fragments/m_musculus/input_files/mouse.fragmented_transcripts.fasta.wRand

    fragments/d_melanogaster/input_files/dmel.fragmented_transcripts.fasta.wRand

    fragments/a_thaliana/input_files/athal.fragmented_transcripts.fasta.wRand

    fragments/s_pombe/input_files/spombe.fragmented_transcripts.fasta.wRand


);



################################
# experiments:
#     - turn off start-refinement
#     - turn off start-refinement and consider all orfs
#     - turn off start-refinement and consider all orfs and disable long orf auto-select
################################



my $PROJ_BASEDIR = "$FindBin::Bin/..";


sub process_cmd {
    my ($cmd) = @_;

    my $ret = system($cmd);
    if ($ret) {
        die "Error, CMD: $cmd died with ret $ret";
    }

    return;
}


sub get_transdecoder_cmd {
    my ($fasta_file, $start_refinement_off, $consider_all_orfs) = @_;

    my $wRand = "";
    if ($fasta_file =~ /wRand$/) {
        $wRand = "wRand";
    }
    
    my @pts = split(/\//, $fasta_file);
    pop @pts;
    pop @pts;
    push (@pts, "output_files_wRand", "TransDecoder");
    
    my $outdir = join("/", @pts);

    my $params = "";
    if ($start_refinement_off) {
        $params .= " --no_refine_starts ";
        $outdir .= "-noRS";
    }
    if ($consider_all_orfs) {
        $params .= " --all_good_orfs";
        $outdir .= "-AGO";
    }

                
    if (! -d $outdir) {
        &process_cmd("mkdir -p $outdir");
    }
    
    return("cd $outdir && /home/unix/bhaas/GITHUB/TransDecoder/TransDecoder.LongOrfs -t $fasta_file && /home/unix/bhaas/GITHUB/TransDecoder/TransDecoder.Predict -t $fasta_file $params ");
    
}




main: {

    foreach my $ref_file (@ref_files) {

        my $full_path = "$PROJ_BASEDIR/$ref_file";
        
        print &get_transdecoder_cmd($full_path, 1) . "\n";  # noRS
        print &get_transdecoder_cmd($full_path, 1, 1) . "\n"; # noRS AGO
    
                
        
    }

    exit(0);
}



    
