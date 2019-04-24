#!/bin/zsh
montreal-forced-aligner/bin/mfa_generate_dictionary montreal-forced-aligner/pretrained_models/mandarin_pinyin_g2p.zip sample_data sample_dict.txt
echo '\nGenerate dictionary successfully\n'
montreal-forced-aligner/bin/mfa_align sample_data sample1/czech_dictionary_Bible.txt czech output_sample